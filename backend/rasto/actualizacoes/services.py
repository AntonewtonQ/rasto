"""Actualização mensal (HU21): métricas da fase pré-preenchidas com o mês anterior; publicar envia aos investidores
com acesso; publicada não se edita, corrige-se."""

from datetime import date

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from rasto.acessos.models import PedidoAcesso
from rasto.auditoria.services import registar
from rasto.nucleo.email import enfileirar
from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.formatos import MESES
from rasto.nucleo.models import EmailSaida
from rasto.startups.models import MembroStartup, Startup

from .models import METRICAS_POR_FASE, METRICAS_SEM_FASE, Actualizacao

A = Actualizacao.Estado


def nome_mes(d: date) -> str:
    return f"{MESES[d.month - 1]} de {d.year}"


def mes_anterior(hoje: date | None = None) -> date:
    hoje = hoje or timezone.localdate()
    return date(hoje.year - (hoje.month == 1), 12 if hoje.month == 1 else hoje.month - 1, 1)


def _exigir_membro(utilizador, startup):
    if not MembroStartup.objects.filter(utilizador=utilizador, startup=startup).exists():
        raise ErroDominio("Só a equipa da startup publica actualizações.")


def ultima_publicada(startup: Startup) -> Actualizacao | None:
    return startup.actualizacoes.filter(estado=A.PUBLICADA).order_by("-periodo", "-publicada_em").first()


def modelo(startup: Startup) -> list[dict]:
    """Métricas sugeridas para a fase, com o valor da última actualização publicada (para a variação)."""
    base = METRICAS_POR_FASE.get(startup.fase.codigo if startup.fase else "", METRICAS_SEM_FASE)
    anterior = ultima_publicada(startup)
    ant = anterior.metricas if anterior else {}
    codigos = [c for c, _, _ in base] + [c for c in ant if c not in {c for c, _, _ in base}]
    rotulos = {c: (r, u) for fase in METRICAS_POR_FASE.values() for c, r, u in fase}
    return [{"codigo": c, "rotulo": rotulos.get(c, (c, "n"))[0], "unidade": rotulos.get(c, (c, "n"))[1],
             "anterior": ant.get(c)} for c in codigos]


def destinatarios(startup: Startup) -> list[str]:
    return list(PedidoAcesso.objects.filter(startup=startup, estado=PedidoAcesso.Estado.ACEITE)
                .values_list("investidor__utilizador__email", flat=True).distinct())


def _limpar_metricas(metricas: dict) -> dict:
    limpo = {}
    for c, v in (metricas or {}).items():
        if v in (None, ""):
            continue
        try:
            n = float(str(v).replace(" ", "").replace(",", "."))
        except ValueError as exc:
            raise ErroDominio(f"O valor de «{c}» tem de ser um número.") from exc
        if n < 0:
            raise ErroDominio("Os valores não podem ser negativos.")
        limpo[str(c)[:40]] = int(n) if n.is_integer() else round(n, 2)
    return limpo


@transaction.atomic
def guardar_rascunho(*, utilizador, startup: Startup, periodo: date, metricas: dict, destaques: str = "",
                     pedidos_ajuda: str = "", corrige: Actualizacao | None = None) -> Actualizacao:
    _exigir_membro(utilizador, startup)
    periodo = periodo.replace(day=1)
    if periodo > timezone.localdate().replace(day=1):
        raise ErroDominio("Não é possível publicar sobre um mês que ainda não começou.")
    if corrige is not None:
        if corrige.startup_id != startup.id or corrige.estado != A.PUBLICADA:
            raise ErroDominio("Só se corrigem actualizações publicadas desta startup.")
        periodo = corrige.periodo
    elif startup.actualizacoes.filter(estado=A.PUBLICADA, periodo=periodo, corrige__isnull=True).exists():
        raise ErroDominio(f"Já publicou a actualização de {nome_mes(periodo)}. Para mudar algo, publique uma correcção.")
    if len(destaques) > 600 or len(pedidos_ajuda) > 300:
        raise ErroDominio("Destaques até 600 caracteres e pedidos de ajuda até 300.")
    r = startup.actualizacoes.filter(estado=A.RASCUNHO).first() or Actualizacao(startup=startup)
    r.periodo, r.metricas, r.destaques, r.pedidos_ajuda, r.corrige = (
        periodo, _limpar_metricas(metricas), destaques.strip(), pedidos_ajuda.strip(), corrige)
    r.save()
    return r


@transaction.atomic
def publicar(*, utilizador, actualizacao: Actualizacao, request=None) -> Actualizacao:
    a = Actualizacao.objects.select_for_update().get(pk=actualizacao.pk)
    _exigir_membro(utilizador, a.startup)
    if a.estado != A.RASCUNHO:
        raise TransicaoInvalida("Esta actualização já foi publicada.")
    if not a.metricas and not a.destaques:
        raise ErroDominio("Indique pelo menos uma métrica ou um destaque.")
    a.estado, a.publicada_em, a.publicada_por = A.PUBLICADA, timezone.now(), utilizador
    a.save()
    registar(actor=utilizador, accao="actualizacao_publicada", objecto=a,
             depois={"periodo": a.periodo.isoformat(), "correccao": bool(a.corrige_id)}, request=request)
    titulo = (f"Correcção à actualização de {nome_mes(a.periodo)}" if a.corrige_id
              else f"Actualização de {nome_mes(a.periodo)}")
    for email in destinatarios(a.startup):
        enfileirar(para=email, assunto=f"{a.startup.nome}: {titulo.lower()}", modelo="emails/actualizacao.txt",
                   contexto={"a": a, "titulo": titulo, "metricas": metricas_legiveis(a),
                             "ligacao": f"{settings.SITE_URL}/i/startups/{a.startup_id}"}, objecto=a)
    return a


def metricas_legiveis(a: Actualizacao) -> list[dict]:
    rotulos = {c: (r, u) for fase in METRICAS_POR_FASE.values() for c, r, u in fase}
    return [{"codigo": c, "rotulo": rotulos.get(c, (c, "n"))[0], "unidade": rotulos.get(c, (c, "n"))[1], "valor": v}
            for c, v in a.metricas.items()]


def falhas_envio(a: Actualizacao) -> list[str]:
    """HU21: quem não recebeu o e-mail."""
    return list(EmailSaida.objects.filter(objecto_tipo="actualizacoes.actualizacao", objecto_id=a.id,
                                          estado=EmailSaida.Estado.ERRO).values_list("destinatario", flat=True))


def visiveis_para_investidor(startup: Startup):
    return startup.actualizacoes.filter(estado=A.PUBLICADA).order_by("-periodo", "-publicada_em")


# --- Lembrete mensal (actualizações periódicas) -----------------------------------------------------------------------

def startups_por_actualizar(hoje: date | None = None) -> list[Startup]:
    """A partir do dia N do mês, startups publicadas sem a actualização do mês anterior."""
    from rasto.nucleo.parametros import prazo

    hoje = hoje or timezone.localdate()
    if hoje.day < prazo("lembrete_actualizacao_dia"):
        return []
    periodo = mes_anterior(hoje)
    feitas = Actualizacao.objects.filter(estado=A.PUBLICADA, periodo=periodo).values_list("startup_id", flat=True)
    return list(Startup.objects.filter(estado=Startup.Estado.PUBLICADO, publicado_em__date__lt=hoje.replace(day=1))
                .exclude(id__in=feitas))


def lembrar_actualizacao(s: Startup):
    periodo = mes_anterior()
    n = len(destinatarios(s))
    for m in MembroStartup.objects.filter(startup=s).select_related("utilizador"):
        enfileirar(para=m.utilizador.email, assunto=f"Actualização de {nome_mes(periodo)} da {s.nome}",
                   modelo="emails/lembrete_actualizacao.txt",
                   contexto={"s": s, "mes": nome_mes(periodo), "n": n, "ligacao": f"{settings.SITE_URL}/s/actualizacoes"})
