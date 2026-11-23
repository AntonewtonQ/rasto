"""Regras do pipeline (RF26–RF30). Cada lado só vê e mexe nas suas relações; o outro lado nunca sabe a etapa."""

from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from rasto.auditoria.services import registar
from rasto.catalogo.models import taxa_actual
from rasto.nucleo.email import enfileirar
from rasto.nucleo.erros import Conflito, ErroDominio, TransicaoInvalida
from rasto.nucleo.formatos import fmt_dinheiro
from rasto.nucleo.parametros import prazo
from rasto.startups.models import MembroStartup, Startup

from .models import FECHADO, MOTIVOS_PERDA, NOME_ETAPA, SOFT_COMMIT, Interaccao, MovimentoEtapa, Relacao

R = Relacao.Lado


# --- Âmbito ------------------------------------------------------------------------------------------------------------

def relacoes_do_utilizador(utilizador):
    """Startup: as do lado startup da sua startup. Investidor: as do seu lado. Mais ninguém."""
    if utilizador.papel_id == "startup":
        return Relacao.objects.filter(lado=R.STARTUP, startup__membros__utilizador=utilizador)
    if utilizador.papel_id == "investidor":
        return Relacao.objects.filter(lado=R.INVESTIDOR, investidor__utilizador=utilizador)
    return Relacao.objects.none()


def _exigir_dono(utilizador, r: Relacao):
    if not relacoes_do_utilizador(utilizador).filter(pk=r.pk).exists():
        raise ErroDominio("Esta relação não é sua.")


def _verificar_versao(r: Relacao, versao: int | None):
    if versao is not None and int(versao) != r.versao:
        raise Conflito("Outra pessoa da equipa mudou esta relação entretanto. Mostramos a versão mais recente.")


def _foto(r: Relacao) -> dict:
    return {"etapa": r.etapa, "perdida": bool(r.perdida_em), "valor": r.valor_indicativo, "moeda": r.moeda}


# --- Criação -----------------------------------------------------------------------------------------------------------

def criar_de_pedido(pedido, autor) -> None:
    """Pedido aceite: a relação entra nos dois pipelines em Contactado (HU16). Se já existia (ex.: acesso
    revogado e pedido de novo), mantém o histórico e volta a Contactado só se estava antes disso."""
    from rasto.startups.services import ronda_aberta

    ronda = ronda_aberta(pedido.startup)
    for lado in (R.STARTUP, R.INVESTIDOR):
        r, nova = Relacao.objects.get_or_create(lado=lado, startup=pedido.startup, investidor=pedido.investidor,
                                                defaults={"etapa": 2, "ronda": ronda, "pedido": pedido})
        if nova:
            MovimentoEtapa.objects.create(relacao=r, etapa_de=None, etapa_para=2, autor=autor)
        else:
            r.pedido = pedido
            r.ronda = r.ronda or ronda
            if r.etapa < 2 and not r.perdida_em:
                MovimentoEtapa.objects.create(relacao=r, etapa_de=r.etapa, etapa_para=2, autor=autor)
                r.etapa = 2
            r.versao += 1
            r.save()


@transaction.atomic
def adicionar_externo(*, utilizador, startup: Startup, nome: str, organizacao: str = "") -> Relacao:
    """HU18: investidor de fora da plataforma, em Identificado, só no pipeline da startup."""
    from rasto.startups.services import ronda_aberta

    if not MembroStartup.objects.filter(utilizador=utilizador, startup=startup).exists():
        raise ErroDominio("Só a equipa da startup adiciona investidores ao pipeline.")
    nome = nome.strip()
    if not nome:
        raise ErroDominio("Indique o nome do investidor.")
    contacto = f"{nome} · {organizacao.strip()}" if organizacao.strip() else nome
    r = Relacao.objects.create(lado=R.STARTUP, startup=startup, contacto_externo=contacto[:160], etapa=1,
                               ronda=ronda_aberta(startup))
    MovimentoEtapa.objects.create(relacao=r, etapa_de=None, etapa_para=1, autor=utilizador)
    registar(actor=utilizador, accao="relacao_externa_adicionada", objecto=r, depois=_foto(r))
    return r


# --- Acções ------------------------------------------------------------------------------------------------------------

@transaction.atomic
def mover(*, utilizador, relacao: Relacao, etapa: int, versao: int | None = None, valor: int | None = None,
          moeda: str | None = None) -> Relacao:
    r = Relacao.objects.select_for_update().get(pk=relacao.pk)
    _exigir_dono(utilizador, r)
    _verificar_versao(r, versao)
    if r.perdida_em:
        raise TransicaoInvalida("Esta relação está marcada como perdida. Desfaça primeiro.")
    if etapa not in NOME_ETAPA:
        raise ErroDominio("Etapa desconhecida.")
    if valor is not None:
        if valor <= 0:
            raise ErroDominio("O valor tem de ser maior do que zero.")
        if moeda not in ("AOA", "USD"):
            raise ErroDominio("Escolha a moeda (Kz ou USD).")
        r.valor_indicativo, r.moeda = valor, moeda
    if etapa >= SOFT_COMMIT and r.valor_indicativo is None:
        raise ErroDominio(f"Para {NOME_ETAPA[etapa]}, indique o valor indicativo e a moeda.")
    if etapa == r.etapa and valor is None:
        return r
    antes = _foto(r)
    if etapa != r.etapa:
        MovimentoEtapa.objects.create(relacao=r, etapa_de=r.etapa, etapa_para=etapa, autor=utilizador)
    r.etapa = etapa
    r.lembrete_adiado_ate = None
    r.versao += 1
    r.save()
    registar(actor=utilizador, accao="relacao_movida", objecto=r, antes=antes, depois=_foto(r))
    return r


@transaction.atomic
def marcar_perdida(*, utilizador, relacao: Relacao, motivo: str, nota: str = "", versao: int | None = None) -> Relacao:
    r = Relacao.objects.select_for_update().get(pk=relacao.pk)
    _exigir_dono(utilizador, r)
    _verificar_versao(r, versao)
    if r.perdida_em:
        raise TransicaoInvalida("Já está marcada como perdida.")
    if motivo not in dict(MOTIVOS_PERDA[r.lado]):
        raise ErroDominio("Escolha o motivo.")
    antes = _foto(r)
    r.perdida_em, r.motivo_perda, r.nota_perda_privada = timezone.now(), motivo, nota.strip()[:300]
    r.versao += 1
    r.save()
    registar(actor=utilizador, accao="relacao_perdida", objecto=r, antes=antes, depois=_foto(r))
    return r


@transaction.atomic
def desfazer_perda(*, utilizador, relacao: Relacao) -> Relacao:
    r = Relacao.objects.select_for_update().get(pk=relacao.pk)
    _exigir_dono(utilizador, r)
    if not r.perdida_em:
        raise TransicaoInvalida("Esta relação não está perdida.")
    antes = _foto(r)
    r.perdida_em, r.motivo_perda, r.nota_perda_privada = None, "", ""
    r.versao += 1
    r.save()
    registar(actor=utilizador, accao="relacao_perda_desfeita", objecto=r, antes=antes, depois=_foto(r))
    return r


@transaction.atomic
def registar_interaccao(*, utilizador, relacao: Relacao, tipo: str, texto: str = "", ocorreu_em=None) -> Interaccao:
    _exigir_dono(utilizador, relacao)
    if tipo not in Interaccao.Tipo.values:
        raise ErroDominio("Tipo de registo desconhecido.")
    quando = ocorreu_em or timezone.now()
    if quando > timezone.now() + timedelta(days=1) and tipo != Interaccao.Tipo.REUNIAO:
        raise ErroDominio("Só reuniões podem ter data futura.")
    i = Interaccao.objects.create(relacao=relacao, tipo=tipo, texto=texto.strip()[:600], ocorreu_em=quando, autor=utilizador)
    Relacao.objects.filter(pk=relacao.pk).update(lembrete_adiado_ate=None)
    return i


@transaction.atomic
def adiar_lembrete(*, utilizador, relacao: Relacao, dias: int = 7) -> Relacao:
    _exigir_dono(utilizador, relacao)
    relacao.lembrete_adiado_ate = timezone.now() + timedelta(days=dias)
    relacao.save(update_fields=["lembrete_adiado_ate", "actualizado_em"])
    return relacao


# --- Leitura e indicadores (base técnica 6.1) ------------------------------------------------------------------------

def ultima_actividade(r: Relacao):
    datas = [r.criado_em, getattr(r, "ult_mov", None), getattr(r, "ult_int", None)]
    if not hasattr(r, "ult_mov"):
        datas += [r.movimentos.aggregate(m=Max("criado_em"))["m"], r.interaccoes.aggregate(m=Max("ocorreu_em"))["m"]]
    agora = timezone.now()
    return max(d for d in datas if d is not None and d <= agora + timedelta(days=1))


def com_actividade(qs):
    return qs.annotate(ult_mov=Max("movimentos__criado_em"), ult_int=Max("interaccoes__ocorreu_em"))


def esta_parada(r: Relacao, dias: int | None = None) -> bool:
    dias = dias or prazo("relacao_parada_dias")
    agora = timezone.now()
    if r.perdida_em or r.etapa >= FECHADO or (r.lembrete_adiado_ate and r.lembrete_adiado_ate > agora):
        return False
    return ultima_actividade(r) < agora - timedelta(days=dias)


def paradas(qs) -> list[Relacao]:
    return [r for r in com_actividade(qs.filter(perdida_em__isnull=True, etapa__lt=FECHADO)) if esta_parada(r)]


def _converter(valor: int, de: str, para: str, taxa: Decimal | None) -> Decimal | None:
    if de == para:
        return Decimal(valor)
    if taxa is None:
        return None
    return Decimal(valor) / taxa if (de, para) == ("AOA", "USD") else Decimal(valor) * taxa


def indicadores(startup: Startup) -> dict:
    """Conversão por etapa (|R| ≥ 3), tempo até ao 1.º soft commit, % da ronda comprometida e relações paradas."""
    from rasto.startups.services import ronda_aberta

    ronda = ronda_aberta(startup)
    todas = Relacao.objects.filter(lado=R.STARTUP, startup=startup)
    rel = list(todas.filter(ronda=ronda)) if ronda else []
    etapa_max = {r.id: m for r, m in ((r, r.movimentos.aggregate(m=Max("etapa_para"))["m"] or r.etapa) for r in rel)}
    conversao = None
    if len(rel) >= 3:
        conversao = []
        for n in range(1, 7):
            chegaram = sum(1 for v in etapa_max.values() if v >= n)
            passaram = sum(1 for v in etapa_max.values() if v >= n + 1)
            conversao.append({"etapa": n, "nome": NOME_ETAPA[n], "chegaram": chegaram, "passaram": passaram,
                              "pct": round(100 * passaram / chegaram, 1) if chegaram else None})
    tempo = None
    if ronda:
        primeiro = MovimentoEtapa.objects.filter(relacao__in=rel, etapa_para__gte=SOFT_COMMIT).order_by("criado_em").first()
        if primeiro:
            tempo = max(0, (timezone.localdate(primeiro.criado_em) - ronda.data_inicio).days)
    comprometido = None
    if ronda:
        t = taxa_actual()
        taxa = t.aoa_por_usd if t else None
        soma, sem_conversao = Decimal(0), 0
        for r in rel:
            if r.etapa >= SOFT_COMMIT and not r.perdida_em and r.valor_indicativo:
                v = _converter(r.valor_indicativo, r.moeda, ronda.moeda, taxa)
                if v is None:
                    sem_conversao += 1
                else:
                    soma += v
        comprometido = {"valor": int(soma), "moeda": ronda.moeda, "alvo": ronda.valor_alvo,
                        "texto": fmt_dinheiro(int(soma), ronda.moeda),
                        "pct": None if sem_conversao else round(float(soma) * 100 / ronda.valor_alvo, 1),
                        "sem_conversao": sem_conversao, "taxa_data": t.data if t else None}
    return {"ronda": bool(ronda), "activas": todas.filter(perdida_em__isnull=True).count(), "conversao": conversao,
            "dias_ate_soft_commit": tempo, "comprometido": comprometido, "paradas": len(paradas(todas)),
            "perdidas": todas.filter(perdida_em__isnull=False).count()}


# --- Lembrete de relação parada (RF30) --------------------------------------------------------------------------------

def destinatarios(r: Relacao) -> list[str]:
    if r.lado == R.STARTUP:
        return list(MembroStartup.objects.filter(startup=r.startup).values_list("utilizador__email", flat=True))
    return [r.investidor.utilizador.email]


def lembrar_parada(r: Relacao):
    outro = r.startup.nome if r.lado == R.INVESTIDOR else (
        r.contacto_externo or (r.investidor.utilizador.nome or r.investidor.utilizador.email))
    caminho = "/s/investidores" if r.lado == R.STARTUP else "/i/pipeline"
    for email in destinatarios(r):
        enfileirar(para=email, assunto=f"Lembrete: a relação com {outro} está parada", modelo="emails/relacao_parada.txt",
                   contexto={"outro": outro, "etapa": NOME_ETAPA[r.etapa], "dias": prazo("relacao_parada_dias"),
                             "ligacao": f"{settings.SITE_URL}{caminho}"}, objecto=r)


def candidatas_a_lembrete() -> list[Relacao]:
    return paradas(Relacao.objects.select_related("startup", "investidor__utilizador"))
