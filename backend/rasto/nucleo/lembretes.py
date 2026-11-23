"""Lembretes por e-mail (base de UX 5.0; base técnica, Sprint 4).

Cada regra devolve os objectos que precisam de lembrete agora. O envio é idempotente: `LembreteEnviado` guarda
(regra, objecto, referência) e a referência muda quando o prazo muda (ex.: convite reenviado), para que um prazo
novo tenha o seu próprio lembrete. O comando `enviar_lembretes` corre no contentor cron.
"""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone

from .models import LembreteEnviado


@dataclass
class Regra:
    nome: str
    candidatos: Callable[[], list]  # objectos a lembrar agora
    referencia: Callable[[object], str]  # muda quando o prazo muda
    enviar: Callable[[object], None]  # enfileira o(s) e-mail(s)


def _registar(regra: str, obj, referencia: str) -> bool:
    """True se for a primeira vez (o lembrete deve ser enviado)."""
    try:
        with transaction.atomic():
            LembreteEnviado.objects.create(regra=regra, objecto_tipo=obj._meta.label_lower, objecto_id=str(obj.pk),
                                           referencia=referencia)
        return True
    except IntegrityError:
        return False


# --- Convites de turma: lembrete ao 7.º dia ----------------------------------------------------------------------


def _convites_a_lembrar():
    from rasto.turmas.models import Convite

    dias = int(settings.PRAZOS_DEFEITO.get("lembrete_convite_dias", 7))
    agora = timezone.now()
    # 7 dias depois do envio (ou do último reenvio) e ainda com prazo a correr.
    return list(Convite.objects.select_related("turma__organizacao", "enviado_por")
                .filter(estado=Convite.Estado.PENDENTE, expira_em__gt=agora,
                        actualizado_em__lte=agora - timedelta(days=dias)))


def _enviar_convite(c):
    from rasto.turmas.services import lembrar_convite

    lembrar_convite(c)


# --- Pedidos de validação de sinais: lembrete à entidade aos 7 dias -------------------------------------------------


def _validacoes_a_lembrar():
    from rasto.sinais.models import Sinal

    dias = int(settings.PRAZOS_DEFEITO.get("lembrete_validacao_dias", 7))
    agora = timezone.now()
    return list(Sinal.objects.select_related("validador", "startup")
                .filter(estado=Sinal.Estado.PENDENTE, expira_em__gt=agora, pedido_em__lte=agora - timedelta(days=dias)))


def _enviar_validacao(s):
    from rasto.sinais.services import lembrar_validacao

    lembrar_validacao(s)


# --- Pedidos de acesso: lembrete à equipa da startup ao 3.º e ao 10.º dia (base de UX 5.6) ----------------------------


def _pedidos_a_lembrar(dias: int):
    def candidatos():
        from rasto.acessos.models import PedidoAcesso

        agora = timezone.now()
        return list(PedidoAcesso.objects.select_related("investidor__utilizador", "startup")
                    .filter(estado=PedidoAcesso.Estado.PENDENTE, expira_em__gt=agora,
                            criado_em__lte=agora - timedelta(days=dias)))
    return candidatos


def _enviar_pedido(p):
    from rasto.acessos.services import lembrar_pedido

    lembrar_pedido(p)


# --- Pipeline: relação parada há 21 dias (RF30); actualização do mês anterior em falta (RF31) -------------------------


def _relacoes_paradas():
    from rasto.pipeline.services import candidatas_a_lembrete

    return candidatas_a_lembrete()


def _enviar_parada(r):
    from rasto.pipeline.services import lembrar_parada

    lembrar_parada(r)


def _ref_parada(r):
    from rasto.pipeline.services import ultima_actividade

    return ultima_actividade(r).isoformat()  # nova paragem depois de actividade = novo lembrete


def _por_actualizar():
    from rasto.actualizacoes.services import startups_por_actualizar

    return startups_por_actualizar()


def _enviar_actualizacao(s):
    from rasto.actualizacoes.services import lembrar_actualizacao

    lembrar_actualizacao(s)


def _ref_actualizacao(_s):
    from rasto.actualizacoes.services import mes_anterior

    return mes_anterior().isoformat()


REGRAS = [
    Regra("convite_7_dias", _convites_a_lembrar, lambda c: c.expira_em.isoformat(), _enviar_convite),
    Regra("validacao_7_dias", _validacoes_a_lembrar, lambda s: s.expira_em.isoformat(), _enviar_validacao),
    Regra("pedido_acesso_3_dias", _pedidos_a_lembrar(3), lambda p: "3", _enviar_pedido),
    Regra("pedido_acesso_10_dias", _pedidos_a_lembrar(10), lambda p: "10", _enviar_pedido),
    Regra("relacao_parada", _relacoes_paradas, _ref_parada, _enviar_parada),
    Regra("actualizacao_mensal", _por_actualizar, _ref_actualizacao, _enviar_actualizacao),
]


def enviar_lembretes() -> dict[str, int]:
    contagem = {}
    for r in REGRAS:
        n = 0
        for obj in r.candidatos():
            # Registo e e-mail na mesma transacção: ou ficam os dois, ou nenhum.
            with transaction.atomic():
                if _registar(r.nome, obj, r.referencia(obj)):
                    r.enviar(obj)
                    n += 1
        contagem[r.nome] = n
    return contagem
