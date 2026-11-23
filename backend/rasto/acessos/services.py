"""Pedido de acesso consentido (base de UX 5.6; RF23–RF25). Nada da camada 2 sai sem a startup aceitar."""

from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone

from rasto.auditoria.services import registar
from rasto.compatibilidade.services import explicar
from rasto.investidores.models import Investidor
from rasto.nucleo.email import enfileirar
from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.formatos import fmt_data, fmt_data_extenso
from rasto.nucleo.parametros import prazo
from rasto.startups.models import MembroStartup, Startup

from .models import PedidoAcesso

P = PedidoAcesso.Estado


def _foto(p: PedidoAcesso) -> dict:
    return {"estado": p.estado, "motivo": p.motivo_recusa}


def tem_acesso(investidor: Investidor | None, startup: Startup) -> bool:
    """Camada 2: pedido aceite e não revogado."""
    return bool(investidor) and PedidoAcesso.objects.filter(investidor=investidor, startup=startup, estado=P.ACEITE).exists()


def bloqueado_ate(investidor: Investidor, startup: Startup):
    """Depois de recusa ou expiração, novo pedido só ao fim de 90 dias (RF25)."""
    p = (PedidoAcesso.objects.filter(investidor=investidor, startup=startup, estado__in=[P.RECUSADO, P.EXPIRADO],
                                     novo_pedido_a_partir_de__gt=timezone.localdate()).order_by("-novo_pedido_a_partir_de").first())
    return p.novo_pedido_a_partir_de if p else None


def _avisar_equipa(startup: Startup, assunto: str, modelo: str, contexto: dict):
    for m in MembroStartup.objects.filter(startup=startup).select_related("utilizador"):
        enfileirar(para=m.utilizador.email, assunto=assunto, modelo=modelo, contexto={**contexto, "site": settings.SITE_URL})


@transaction.atomic
def pedir_acesso(*, investidor: Investidor, startup: Startup, nota: str, origem: str = "perfil",
                 posicao: int | None = None, request=None) -> PedidoAcesso:
    if investidor.estado_conta != Investidor.EstadoConta.APROVADA:
        raise ErroDominio("A sua conta de investidor não está activa.")
    if startup.estado != Startup.Estado.PUBLICADO:
        raise ErroDominio("Esta startup não tem o perfil publicado.")
    if not investidor.mandato.minimo_completo:
        raise ErroDominio("Defina primeiro o mandato mínimo (sectores e fase).")
    nota = nota.strip()
    if not nota:
        raise ErroDominio("Escreva uma nota curta: ajuda a startup a decidir.")
    if len(nota) > 300:
        raise ErroDominio("A nota tem no máximo 300 caracteres.")
    if tem_acesso(investidor, startup):
        raise ErroDominio("Já tem acesso a esta startup.")
    ate = bloqueado_ate(investidor, startup)
    if ate:
        raise ErroDominio(f"Pode voltar a pedir a partir de {fmt_data(ate)}.")
    e = explicar(startup, investidor.mandato)
    try:
        with transaction.atomic():
            p = PedidoAcesso.objects.create(
                investidor=investidor, startup=startup, nota=nota, pontuacao=e.total, decomposicao=e.criterios,
                config_versao=e.versao, origem=origem if origem in ("sugestao", "perfil") else "perfil", posicao_lista=posicao,
                expira_em=timezone.now() + timedelta(days=prazo("pedido_acesso_dias")))
    except IntegrityError as exc:
        raise ErroDominio("Já pediu acesso a esta startup. O pedido está pendente.") from exc
    registar(actor=investidor.utilizador, accao="acesso_pedido", objecto=p, depois=_foto(p), request=request)
    u = investidor.utilizador
    _avisar_equipa(startup, f"{u.nome or u.email} quer conhecer a {startup.nome}", "emails/pedido_acesso.txt",
                   {"p": p, "inv": investidor, "startup": startup, "validade": fmt_data_extenso(p.expira_em)})
    return p


def lembrar_pedido(p: PedidoAcesso):
    u = p.investidor.utilizador
    _avisar_equipa(p.startup, f"Lembrete: {u.nome or u.email} aguarda resposta", "emails/pedido_acesso.txt",
                   {"p": p, "inv": p.investidor, "startup": p.startup, "validade": fmt_data_extenso(p.expira_em),
                    "lembrete": True})


def _exigir_equipa(utilizador, startup: Startup):
    if not MembroStartup.objects.filter(utilizador=utilizador, startup=startup).exists():
        raise ErroDominio("Este pedido não é dirigido à sua startup.")


def _bloquear_90(p: PedidoAcesso):
    p.novo_pedido_a_partir_de = timezone.localdate() + timedelta(days=prazo("novo_pedido_dias"))


@transaction.atomic
def aceitar(*, utilizador, pedido: PedidoAcesso, request=None) -> PedidoAcesso:
    _exigir_equipa(utilizador, pedido.startup)
    if pedido.estado != P.PENDENTE:
        raise TransicaoInvalida("Só é possível aceitar pedidos pendentes.")
    if pedido.expira_em <= timezone.now():
        raise TransicaoInvalida("Este pedido já expirou.")
    antes = _foto(pedido)
    pedido.estado, pedido.decidido_em = P.ACEITE, timezone.now()
    pedido.save()
    registar(actor=utilizador, accao="acesso_aceite", objecto=pedido, antes=antes, depois=_foto(pedido), request=request)
    enfileirar(para=pedido.investidor.utilizador.email, assunto=f"A {pedido.startup.nome} aceitou o seu pedido",
               modelo="emails/acesso_decidido.txt", contexto={"p": pedido, "site": settings.SITE_URL})
    return pedido


@transaction.atomic
def recusar(*, utilizador, pedido: PedidoAcesso, motivo: str = "", partilhar: bool = False, request=None) -> PedidoAcesso:
    _exigir_equipa(utilizador, pedido.startup)
    if pedido.estado != P.PENDENTE:
        raise TransicaoInvalida("Só é possível recusar pedidos pendentes.")
    if motivo and motivo not in PedidoAcesso.Motivo.values:
        raise ErroDominio("Motivo desconhecido.")
    antes = _foto(pedido)
    pedido.estado, pedido.decidido_em = P.RECUSADO, timezone.now()
    pedido.motivo_recusa = motivo
    pedido.motivo_partilhado = bool(partilhar and motivo and motivo != PedidoAcesso.Motivo.SEM_MOTIVO)
    _bloquear_90(pedido)
    pedido.save()
    registar(actor=utilizador, accao="acesso_recusado", objecto=pedido, antes=antes, depois=_foto(pedido), request=request)
    enfileirar(para=pedido.investidor.utilizador.email, assunto=f"A {pedido.startup.nome} não aceitou o pedido desta vez",
               modelo="emails/acesso_decidido.txt", contexto={"p": pedido, "site": settings.SITE_URL,
                                                              "novo": fmt_data(pedido.novo_pedido_a_partir_de)})
    return pedido


@transaction.atomic
def revogar(*, utilizador, pedido: PedidoAcesso, request=None) -> PedidoAcesso:
    _exigir_equipa(utilizador, pedido.startup)
    if pedido.estado != P.ACEITE:
        raise TransicaoInvalida("Só é possível retirar acessos concedidos.")
    antes = _foto(pedido)
    pedido.estado, pedido.revogado_em = P.REVOGADO, timezone.now()
    pedido.save()
    registar(actor=utilizador, accao="acesso_revogado", objecto=pedido, antes=antes, depois=_foto(pedido), request=request)
    return pedido


@transaction.atomic
def retirar(*, investidor: Investidor, pedido: PedidoAcesso) -> PedidoAcesso:
    if pedido.investidor_id != investidor.id:
        raise ErroDominio("Este pedido não é seu.")
    if pedido.estado != P.PENDENTE:
        raise TransicaoInvalida("Só é possível retirar pedidos pendentes.")
    antes = _foto(pedido)
    pedido.estado = P.RETIRADO
    pedido.save()
    registar(actor=investidor.utilizador, accao="acesso_retirado_pelo_investidor", objecto=pedido, antes=antes, depois=_foto(pedido))
    return pedido


def expirar_pedidos() -> int:
    n = 0
    for p in PedidoAcesso.objects.filter(estado=P.PENDENTE, expira_em__lte=timezone.now()):
        with transaction.atomic():
            antes = _foto(p)
            p.estado = P.EXPIRADO
            _bloquear_90(p)
            p.save()
            registar(actor=None, accao="acesso_expirado", objecto=p, antes=antes, depois=_foto(p))
        n += 1
    return n


@transaction.atomic
def registar_abertura_documento(*, investidor: Investidor, documento, request=None):
    """Cada abertura de documento pela camada 2 fica na auditoria (base técnica 7.3)."""
    registar(actor=investidor.utilizador, accao="documento_aberto", objecto=documento.startup,
             depois={"documento": str(documento.id), "titulo": documento.titulo}, request=request)
