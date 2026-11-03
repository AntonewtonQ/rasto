import re
from datetime import timedelta

import pytest
from django.utils import timezone

from rasto.nucleo.lembretes import enviar_lembretes
from rasto.nucleo.models import EmailSaida
from rasto.sinais.models import Sinal
from rasto.turmas import services
from rasto.turmas.models import Convite, hash_token

from .conftest import membro

pytestmark = pytest.mark.django_db


def _envelhecer_convite(c, dias=8):
    Convite.objects.filter(pk=c.pk).update(actualizado_em=timezone.now() - timedelta(days=dias))


def test_convite_por_email_tem_lembrete_ao_7o_dia_com_ligacao_nova(turma):
    enviados, _ = services.enviar_convites(utilizador=membro(turma.organizacao), turma=turma, texto="l@startup.test")
    c = enviados[0]
    hash_antigo = c.token_hash
    assert enviar_lembretes()["convite_7_dias"] == 0  # ainda não passaram 7 dias
    _envelhecer_convite(c)
    assert enviar_lembretes()["convite_7_dias"] == 1
    lembrete = EmailSaida.objects.filter(destinatario="l@startup.test", assunto__startswith="Lembrete").get()
    token = re.search(r"/convite/(\S+)/", lembrete.corpo).group(1)
    c.refresh_from_db()
    assert c.token_hash == hash_token(token) != hash_antigo  # a ligação antiga deixa de valer
    assert services.obter_convite(token).pk == c.pk


def test_lembrete_e_enviado_uma_so_vez(turma):
    enviados, _ = services.enviar_convites(utilizador=membro(turma.organizacao), turma=turma, texto="u@startup.test")
    _envelhecer_convite(enviados[0])
    enviar_lembretes()
    _envelhecer_convite(enviados[0])
    assert enviar_lembretes()["convite_7_dias"] == 0


def test_convite_por_ligacao_avisa_a_entidade(turma):
    c, _url, _ = services.gerar_ligacao_convite(utilizador=membro(turma.organizacao), turma=turma, email="w@startup.test")
    hash_antigo = c.token_hash
    _envelhecer_convite(c)
    enviar_lembretes()
    c.refresh_from_db()
    assert c.token_hash == hash_antigo  # a ligação partilhada no WhatsApp continua a valer
    assert EmailSaida.objects.filter(destinatario=membro(turma.organizacao).email,
                                     assunto__contains="w@startup.test").exists()
    assert not EmailSaida.objects.filter(destinatario="w@startup.test", assunto__startswith="Lembrete").exists()


def test_reenvio_cria_prazo_novo_e_lembrete_novo(turma):
    enviados, _ = services.enviar_convites(utilizador=membro(turma.organizacao), turma=turma, texto="r@startup.test")
    c = enviados[0]
    _envelhecer_convite(c)
    enviar_lembretes()
    Convite.objects.filter(pk=c.pk).update(estado=Convite.Estado.EXPIRADO)
    c.refresh_from_db()
    services.reenviar_convite(utilizador=membro(turma.organizacao), convite=c)
    _envelhecer_convite(c)
    assert enviar_lembretes()["convite_7_dias"] == 1


def test_validacao_pendente_tem_lembrete_a_entidade(startup_aceite):
    _u, st, _ = startup_aceite
    s = Sinal.objects.get(startup=st.startup)
    Sinal.objects.filter(pk=s.pk).update(pedido_em=timezone.now() - timedelta(days=8))
    assert enviar_lembretes()["validacao_7_dias"] == 1
    corpo = EmailSaida.objects.get(assunto__contains="espera a vossa confirmação").corpo
    assert "Kitanda Fresca participou no Programa de Aceleração" in corpo
    assert enviar_lembretes()["validacao_7_dias"] == 0
