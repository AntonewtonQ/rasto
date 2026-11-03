from django.conf import settings
from django.db import transaction
from django.utils import timezone

from rasto.auditoria.services import registar
from rasto.nucleo.email import enfileirar
from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.formatos import fmt_data, fmt_data_extenso
from rasto.organizacoes.services import organizacao_do_utilizador
from rasto.turmas.services import frase_validacao

from .models import Sinal

S = Sinal.Estado


def _foto(s: Sinal) -> dict:
    return {"estado": s.estado, "motivo": s.motivo, "frase_validada": s.frase_validada}


def frase_do_sinal(sinal: Sinal) -> str:
    """O que a entidade vai confirmar, palavra por palavra."""
    if sinal.tipo == Sinal.Tipo.PARTICIPACAO and sinal.turma_id:
        return frase_validacao(sinal.turma, sinal.startup.nome)
    data = f" ({fmt_data(sinal.data_facto)})" if sinal.data_facto else ""
    return f"{sinal.startup.nome}: {sinal.descricao}{data}."


def _exigir_validador(utilizador, sinal: Sinal):
    org = organizacao_do_utilizador(utilizador)
    if org is None or sinal.validador_id != org.id:
        raise ErroDominio("Este sinal não está atribuído à sua entidade.")
    if not org.pode_convidar_e_validar:
        raise ErroDominio("A entidade não está verificada: as validações estão bloqueadas.")
    if not sinal.startup.turmas.filter(turma__organizacao=org).exists():
        raise ErroDominio("Só pode validar sinais de startups das suas turmas.")
    return org


@transaction.atomic
def validar_sinal(*, utilizador, sinal: Sinal, request=None) -> Sinal:
    sinal = Sinal.objects.select_for_update(of=("self",)).select_related("startup", "turma", "validador").get(pk=sinal.pk)
    _exigir_validador(utilizador, sinal)
    if sinal.estado != S.PENDENTE:
        raise TransicaoInvalida("Só é possível validar sinais pendentes de validação.")
    antes = _foto(sinal)
    sinal.frase_validada = frase_do_sinal(sinal)
    sinal.estado = S.VALIDADO
    sinal.validado_em = timezone.now()
    sinal.validado_por = utilizador
    sinal.motivo = ""
    sinal.save()
    registar(actor=utilizador, accao="sinal_validado", objecto=sinal, antes=antes, depois=_foto(sinal), request=request)
    return sinal


@transaction.atomic
def validar_em_lote(*, utilizador, sinais: list[Sinal], request=None) -> list[Sinal]:
    """Só participações entram em lote; os marcos validam-se um a um (base de UX 3.1)."""
    if any(s.tipo != Sinal.Tipo.PARTICIPACAO for s in sinais):
        raise ErroDominio("Marcos validam-se um a um. Retire os marcos da selecção.")
    return [validar_sinal(utilizador=utilizador, sinal=s, request=request) for s in sinais]


@transaction.atomic
def recusar_sinal(*, utilizador, sinal: Sinal, motivo: str, request=None) -> Sinal:
    sinal = Sinal.objects.select_for_update(of=("self",)).select_related("startup").get(pk=sinal.pk)
    _exigir_validador(utilizador, sinal)
    if sinal.estado != S.PENDENTE:
        raise TransicaoInvalida("Só é possível recusar sinais pendentes de validação.")
    if not motivo.strip():
        raise ErroDominio("Erro: indique o motivo da recusa. A startup vai lê-lo; o investidor não.")
    antes = _foto(sinal)
    sinal.estado = S.RECUSADO
    sinal.motivo = motivo.strip()
    sinal.save()
    registar(actor=utilizador, accao="sinal_recusado", objecto=sinal, antes=antes, depois=_foto(sinal), request=request)
    return sinal


@transaction.atomic
def retirar_validacao(*, utilizador, sinal: Sinal, motivo: str, request=None) -> Sinal:
    sinal = Sinal.objects.select_for_update(of=("self",)).select_related("startup").get(pk=sinal.pk)
    org = organizacao_do_utilizador(utilizador)
    if org is None or sinal.validador_id != org.id:
        raise ErroDominio("Este sinal não está atribuído à sua entidade.")
    if sinal.estado != S.VALIDADO:
        raise TransicaoInvalida("Só é possível retirar validações em vigor.")
    if not motivo.strip():
        raise ErroDominio("Erro: indique o motivo para retirar a validação.")
    antes = _foto(sinal)
    sinal.estado = S.RETIRADO
    sinal.motivo = motivo.strip()
    sinal.save()
    registar(actor=utilizador, accao="validacao_retirada", objecto=sinal, antes=antes, depois=_foto(sinal),
             request=request)
    return sinal


def expirar_pedidos_validacao() -> int:
    n = 0
    for s in Sinal.objects.filter(estado=S.PENDENTE, expira_em__lte=timezone.now()):
        with transaction.atomic():
            antes = _foto(s)
            s.estado = S.EXPIRADO
            s.save(update_fields=["estado", "actualizado_em"])
            registar(actor=None, accao="pedido_validacao_expirado", objecto=s, antes=antes, depois=_foto(s))
        n += 1
    return n


def lembrar_validacao(sinal: Sinal):
    """Lembrete à entidade aos 7 dias de um pedido de validação ainda pendente (base de UX 5.0)."""
    org = sinal.validador
    if org is None:
        return
    for m in org.membros.select_related("utilizador"):
        enfileirar(para=m.utilizador.email, assunto=f"Lembrete: {sinal.startup.nome} espera a vossa confirmação",
                   modelo="emails/lembrete_validacao.txt",
                   contexto={"s": sinal, "frase": frase_do_sinal(sinal), "validade": fmt_data_extenso(sinal.expira_em),
                             "site": settings.SITE_URL})
    registar(actor=None, accao="lembrete_validacao", objecto=sinal)
