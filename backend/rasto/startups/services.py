"""Startup: registo próprio, equipa e pedido do selo de aceleração (fluxo definido pelo autor a 04/11/2026:
a startup cria conta, convida a equipa e pede à aceleradora que lhe atribua o selo)."""

import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.utils import timezone

from rasto.auditoria.services import registar
from rasto.contas.models import Papel, Utilizador, registar_consentimento
from rasto.nucleo.email import enfileirar
from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.formatos import fmt_data_extenso
from rasto.nucleo.parametros import prazo
from rasto.organizacoes.models import Organizacao
from rasto.sinais.models import Sinal
from rasto.turmas.models import Turma

from .models import ConviteMembroStartup, MembroStartup, Startup

F = MembroStartup.Funcao


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


@transaction.atomic
def registar_startup(*, email: str, palavra_passe: str, nome: str, nome_startup: str, request=None) -> tuple[Utilizador, Startup]:
    email = email.strip().lower()
    if Utilizador.objects.filter(email__iexact=email).exists():
        raise ErroDominio("Já existe uma conta com este e-mail. Entre com essa conta ou use outro e-mail.")
    u = Utilizador.objects.create_user(email, palavra_passe, nome=nome.strip(), papel_id=Papel.STARTUP)
    registar_consentimento(u)
    s = Startup.objects.create(nome=nome_startup.strip())
    MembroStartup.objects.create(utilizador=u, startup=s, funcao=F.FUNDADOR)
    registar(actor=u, accao="startup_registada", objecto=s, depois={"nome": s.nome}, request=request)
    return u, s


# --- Equipa ----------------------------------------------------------------------------------------------------------


def _exigir_fundador(utilizador, startup: Startup):
    if not MembroStartup.objects.filter(utilizador=utilizador, startup=startup, funcao=F.FUNDADOR).exists():
        raise ErroDominio("Só os fundadores podem gerir a equipa da startup.")


@transaction.atomic
def convidar_membro(*, utilizador, startup: Startup, email: str) -> tuple[ConviteMembroStartup, str]:
    _exigir_fundador(utilizador, startup)
    email = email.strip().lower()
    validate_email(email)
    if Utilizador.objects.filter(email__iexact=email).exists():
        raise ErroDominio("Já existe uma conta com este e-mail. Cada conta tem um só papel: use outro e-mail.")
    token = secrets.token_urlsafe(32)
    try:
        with transaction.atomic():
            c = ConviteMembroStartup.objects.create(startup=startup, email=email, token_hash=_hash(token),
                                                    expira_em=timezone.now() + timedelta(days=prazo("convite_dias")),
                                                    enviado_por=utilizador)
    except IntegrityError as exc:
        raise ErroDominio(f"{email} já tem um convite pendente.") from exc
    enfileirar(para=email, assunto=f"{utilizador.nome or utilizador.email} convidou-o para a equipa da {startup.nome} na Rasto",
               modelo="emails/convite_equipa_startup.txt",
               contexto={"s": startup, "de": utilizador, "url": f"{settings.SITE_URL}/equipa/{token}/",
                         "validade": fmt_data_extenso(c.expira_em)}, objecto=c)
    registar(actor=utilizador, accao="membro_startup_convidado", objecto=startup, depois={"email": email})
    return c, token


def obter_convite_membro(token: str) -> ConviteMembroStartup | None:
    c = ConviteMembroStartup.objects.select_related("startup", "enviado_por").filter(token_hash=_hash(token)).first()
    if c and c.estado == c.Estado.PENDENTE and c.expira_em <= timezone.now():
        c.estado = c.Estado.EXPIRADO
        c.save(update_fields=["estado", "actualizado_em"])
    return c


def aceitar_convite_membro(*, token: str, nome: str, palavra_passe: str, consentiu: bool) -> Utilizador:
    c = obter_convite_membro(token)  # fora da transacção: uma expiração detectada fica gravada
    if c is None:
        raise ErroDominio("Este convite não existe.")
    if c.estado != c.Estado.PENDENTE:
        raise TransicaoInvalida("Este convite já não está disponível.")
    if not consentiu:
        raise ErroDominio("Para criar a conta, aceite o aviso de privacidade.")
    with transaction.atomic():
        c = ConviteMembroStartup.objects.select_for_update().get(pk=c.pk)
        if c.estado != c.Estado.PENDENTE:
            raise TransicaoInvalida("Este convite já não está disponível.")
        u = Utilizador.objects.create_user(c.email, palavra_passe, nome=nome.strip(), papel_id=Papel.STARTUP)
        registar_consentimento(u)
        MembroStartup.objects.create(utilizador=u, startup=c.startup, funcao=F.MEMBRO)
        c.estado = c.Estado.ACEITE
        c.aceite_em = timezone.now()
        c.save(update_fields=["estado", "aceite_em", "actualizado_em"])
        registar(actor=u, accao="membro_startup_entrou", objecto=c.startup, depois={"email": u.email})
    return u


@transaction.atomic
def cancelar_convite_membro(*, utilizador, convite: ConviteMembroStartup) -> None:
    _exigir_fundador(utilizador, convite.startup)
    if convite.estado != convite.Estado.PENDENTE:
        raise TransicaoInvalida("Só é possível cancelar convites pendentes.")
    convite.estado = convite.Estado.CANCELADO
    convite.save(update_fields=["estado", "actualizado_em"])
    registar(actor=utilizador, accao="convite_membro_startup_cancelado", objecto=convite.startup, depois={"email": convite.email})


@transaction.atomic
def retirar_membro(*, utilizador, startup: Startup, membro: MembroStartup) -> None:
    """O membro perde o acesso e a conta fica desactivada (uma conta, um papel); o nome fica na auditoria."""
    _exigir_fundador(utilizador, startup)
    if membro.utilizador_id == utilizador.id:
        raise ErroDominio("Não pode retirar-se a si próprio.")
    if membro.funcao == F.FUNDADOR and startup.membros.filter(funcao=F.FUNDADOR).count() <= 1:
        raise ErroDominio("A startup tem de ter sempre um fundador.")
    u = membro.utilizador
    membro.delete()
    u.is_active = False
    u.save(update_fields=["is_active"])
    registar(actor=utilizador, accao="membro_startup_retirado", objecto=startup, depois={"email": u.email})


# --- Pedido do selo de aceleração --------------------------------------------------------------------------------------


def turmas_para_pedido():
    """Turmas a que uma startup pode pedir o selo: de entidades verificadas, já criadas (não em rascunho)."""
    return (Turma.objects.select_related("organizacao")
            .filter(organizacao__estado_verificacao=Organizacao.Estado.VERIFICADA, estado__in=["activa", "encerrada"])
            .order_by("organizacao__nome_publico", "organizacao__nome_legal", "-inicio"))


@transaction.atomic
def pedir_selo(*, utilizador, startup: Startup, turma: Turma, nota: str = "", request=None) -> Sinal:
    """Cria o sinal de participação «pendente de validação» e avisa a equipa da entidade. A entidade confirma (com a
    frase exacta à vista) ou recusa com motivo. Ao confirmar, a startup fica ligada à turma."""
    if not MembroStartup.objects.filter(utilizador=utilizador, startup=startup).exists():
        raise ErroDominio("Só a equipa da startup pode pedir o selo.")
    if turma.organizacao.estado_verificacao != Organizacao.Estado.VERIFICADA or turma.estado == Turma.Estado.RASCUNHO:
        raise ErroDominio("Esta turma não está disponível para pedidos.")
    existente = Sinal.objects.filter(startup=startup, turma=turma, tipo=Sinal.Tipo.PARTICIPACAO).first()
    if existente:
        if existente.estado == Sinal.Estado.PENDENTE:
            raise ErroDominio("Já pediu o selo desta turma. Aguarde a resposta da entidade.")
        if existente.estado == Sinal.Estado.VALIDADO:
            raise ErroDominio("A startup já tem o selo desta turma.")
        if existente.estado == Sinal.Estado.RECUSADO:
            raise ErroDominio("A entidade recusou este pedido. Fale directamente com a entidade antes de pedir de novo.")
        existente.delete()  # expirado ou retirado: pode pedir outra vez
    agora = timezone.now()
    s = Sinal.objects.create(
        startup=startup, turma=turma, tipo=Sinal.Tipo.PARTICIPACAO, validador=turma.organizacao,
        descricao=f"Participou no {turma.programa} {turma.edicao} ({turma.periodo})", data_facto=turma.fim,
        estado=Sinal.Estado.PENDENTE, evidencia=nota.strip()[:300], pedido_em=agora,
        expira_em=agora + timedelta(days=prazo("validacao_sinal_dias")),
    )
    registar(actor=utilizador, accao="selo_pedido", objecto=s, depois={"turma": str(turma.id), "estado": s.estado},
             request=request)
    for m in turma.organizacao.membros.select_related("utilizador"):
        enfileirar(para=m.utilizador.email, assunto=f"{startup.nome} pede o selo de participação na turma {turma}",
                   modelo="emails/pedido_selo.txt",
                   contexto={"s": s, "t": turma, "startup": startup, "nota": s.evidencia,
                             "site": settings.SITE_URL, "validade": fmt_data_extenso(s.expira_em)})
    return s


@transaction.atomic
def cancelar_pedido_selo(*, utilizador, sinal: Sinal) -> None:
    if not MembroStartup.objects.filter(utilizador=utilizador, startup=sinal.startup).exists():
        raise ErroDominio("Este pedido não é da sua startup.")
    if sinal.estado != Sinal.Estado.PENDENTE or sinal.tipo != Sinal.Tipo.PARTICIPACAO:
        raise TransicaoInvalida("Só é possível cancelar pedidos pendentes.")
    registar(actor=utilizador, accao="selo_pedido_cancelado", objecto=sinal, antes={"estado": sinal.estado})
    sinal.delete()


# --- Perfil, ronda, documentos e publicação (S-01, S-02) ------------------------------------------------------------


def _exigir_membro(utilizador, startup: Startup):
    if not MembroStartup.objects.filter(utilizador=utilizador, startup=startup).exists():
        raise ErroDominio("Só a equipa da startup pode alterar o perfil.")


def ronda_aberta(startup: Startup):
    from .models import Ronda

    return Ronda.objects.filter(startup=startup, estado=Ronda.Estado.ABERTA).first()


def em_falta_para_publicar(startup: Startup) -> list[str]:
    """Os 6 obrigatórios da especificação (S-01): nome, sector, fase, cidade, resumo e ronda."""
    falta = []
    if not startup.nome.strip():
        falta.append("nome")
    if startup.sector_id is None:
        falta.append("sector")
    if startup.fase_id is None:
        falta.append("fase")
    if startup.provincia_id is None or not startup.cidade.strip():
        falta.append("província e cidade")
    if not startup.resumo.strip():
        falta.append("resumo")
    if ronda_aberta(startup) is None:
        falta.append("ronda")
    return falta


def completude(startup: Startup) -> int:
    """Especificação de interface S-01: 6 obrigatórios valem 60%; selo validado 10%; marco 10%; documentos 10%;
    contacto 10% (as métricas da fase entram com as actualizações periódicas)."""
    total = 10 * (6 - len(em_falta_para_publicar(startup)))
    if startup.sinais.filter(estado="validado").exists():
        total += 10
    if startup.sinais.filter(tipo="marco").exists():
        total += 10
    if startup.documentos.exists():
        total += 10
    if startup.contacto_fundador.strip():
        total += 10
    return min(total, 100)


CAMPOS_PERFIL = ("nome", "sector", "fase", "provincia", "cidade", "resumo", "contacto_fundador")


@transaction.atomic
def actualizar_perfil(*, utilizador, startup: Startup, dados: dict) -> Startup:
    _exigir_membro(utilizador, startup)
    antes = {c: str(getattr(startup, f"{c}_id", None) or getattr(startup, c, "")) for c in CAMPOS_PERFIL}
    for campo in CAMPOS_PERFIL:
        if campo in dados:
            setattr(startup, campo, dados[campo])
    if startup.estado == Startup.Estado.PUBLICADO and em_falta_para_publicar(startup):
        raise ErroDominio("Um perfil publicado tem de manter os campos obrigatórios: " + ", ".join(em_falta_para_publicar(startup)) + ".")
    startup.save()
    registar(actor=utilizador, accao="perfil_actualizado", objecto=startup, antes=antes,
             depois={c: str(getattr(startup, f"{c}_id", None) or getattr(startup, c, "")) for c in CAMPOS_PERFIL})
    return startup


@transaction.atomic
def definir_ronda(*, utilizador, startup: Startup, valor_alvo: int, moeda: str, data_inicio) -> "object":
    from .models import Ronda

    _exigir_membro(utilizador, startup)
    if valor_alvo <= 0:
        raise ErroDominio("O valor da ronda tem de ser maior do que zero.")
    r = ronda_aberta(startup) or Ronda(startup=startup)
    r.valor_alvo, r.moeda, r.data_inicio = valor_alvo, moeda, data_inicio
    r.save()
    registar(actor=utilizador, accao="ronda_definida", objecto=startup, depois={"valor": valor_alvo, "moeda": moeda})
    return r


@transaction.atomic
def adicionar_documento(*, utilizador, startup: Startup, titulo: str, url: str):
    from .models import DocumentoLigacao

    _exigir_membro(utilizador, startup)
    if not url.lower().startswith("https://"):
        raise ErroDominio("A ligação tem de começar por https://.")
    d = DocumentoLigacao.objects.create(startup=startup, titulo=titulo.strip()[:120], url=url.strip())
    registar(actor=utilizador, accao="documento_adicionado", objecto=startup, depois={"titulo": d.titulo})
    return d


@transaction.atomic
def remover_documento(*, utilizador, documento) -> None:
    _exigir_membro(utilizador, documento.startup)
    registar(actor=utilizador, accao="documento_removido", objecto=documento.startup, antes={"titulo": documento.titulo})
    documento.delete()


@transaction.atomic
def publicar(*, utilizador, startup: Startup) -> Startup:
    _exigir_membro(utilizador, startup)
    falta = em_falta_para_publicar(startup)
    if falta:
        raise ErroDominio("Para publicar, falta: " + ", ".join(falta) + ".")
    startup.estado = Startup.Estado.PUBLICADO
    startup.publicado_em = startup.publicado_em or timezone.now()
    startup.save(update_fields=["estado", "publicado_em", "actualizado_em"])
    registar(actor=utilizador, accao="perfil_publicado", objecto=startup)
    return startup


@transaction.atomic
def despublicar(*, utilizador, startup: Startup) -> Startup:
    """Ao despublicar, os pedidos pendentes expiram de imediato (base de UX 5.6)."""
    _exigir_membro(utilizador, startup)
    startup.estado = Startup.Estado.DESPUBLICADO
    startup.save(update_fields=["estado", "actualizado_em"])
    startup.pedidos_acesso.filter(estado="pendente").update(estado="expirado")
    registar(actor=utilizador, accao="perfil_despublicado", objecto=startup)
    return startup
