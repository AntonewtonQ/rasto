"""Fluxo definido pelo autor (04/11/2026): a startup cria conta, convida a equipa e pede à aceleradora o selo."""

from datetime import date

import pytest

from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.models import EmailSaida
from rasto.sinais import services as sinais
from rasto.sinais.models import Sinal
from rasto.sinais.selectors import pendentes_da_entidade
from rasto.startups import services
from rasto.startups.models import MembroStartup
from rasto.turmas import services as turmas
from rasto.turmas.models import StartupTurma

from .conftest import PALAVRA, TODOS_CUMPREM, criar_utilizador, membro, nova_entidade, submeter

pytestmark = pytest.mark.django_db


@pytest.fixture
def fundadora(db):
    return services.registar_startup(email="nadia@kitanda.test", palavra_passe=PALAVRA, nome="Nádia Kiala",
                                     nome_startup="Kitanda Fresca")


def test_registo_proprio_cria_conta_startup_e_fundadora(fundadora):
    u, s = fundadora
    assert u.papel_id == "startup" and u.consentimentos.exists()
    assert MembroStartup.objects.get(utilizador=u).funcao == "fundador" and s.estado == "rascunho"


def test_equipa_da_startup(fundadora):
    u, s = fundadora
    _c, token = services.convidar_membro(utilizador=u, startup=s, email="joao@kitanda.test")
    joao = services.aceitar_convite_membro(token=token, nome="João", palavra_passe=PALAVRA, consentiu=True)
    assert MembroStartup.objects.get(utilizador=joao).funcao == "membro"
    with pytest.raises(TransicaoInvalida):
        services.aceitar_convite_membro(token=token, nome="X", palavra_passe=PALAVRA, consentiu=True)
    with pytest.raises(ErroDominio, match="fundadores"):
        services.convidar_membro(utilizador=joao, startup=s, email="outro@kitanda.test")
    with pytest.raises(ErroDominio, match="si próprio"):
        services.retirar_membro(utilizador=u, startup=s, membro=MembroStartup.objects.get(utilizador=u))
    services.retirar_membro(utilizador=u, startup=s, membro=MembroStartup.objects.get(utilizador=joao))
    joao.refresh_from_db()
    assert not joao.is_active


def test_pedido_de_selo_e_confirmacao_ligam_a_startup_a_turma(fundadora, turma):
    u, s = fundadora
    gestora = membro(turma.organizacao)
    pedido = services.pedir_selo(utilizador=u, startup=s, turma=turma, nota="Turma de Março, mentora Ana")
    assert pedido.estado == "pendente" and pedido.validador == turma.organizacao and pedido.evidencia
    assert EmailSaida.objects.filter(destinatario=gestora.email, assunto__contains="pede o selo").exists()
    assert list(pendentes_da_entidade(gestora)) == [pedido]
    with pytest.raises(ErroDominio, match="Já pediu"):
        services.pedir_selo(utilizador=u, startup=s, turma=turma)
    sinais.validar_sinal(utilizador=gestora, sinal=pedido)
    pedido.refresh_from_db()
    assert pedido.estado == "validado"
    assert pedido.frase_validada == "Kitanda Fresca participou no Programa de Aceleração 2026 · Turma 3 (Mar.–Jun. 2026)."
    assert StartupTurma.objects.filter(startup=s, turma=turma).exists()
    assert EmailSaida.objects.filter(destinatario=u.email, assunto__contains="confirmou o selo").exists()
    with pytest.raises(ErroDominio, match="já tem o selo"):
        services.pedir_selo(utilizador=u, startup=s, turma=turma)


def test_recusa_avisa_a_startup_e_impede_novo_pedido(fundadora, turma):
    u, s = fundadora
    pedido = services.pedir_selo(utilizador=u, startup=s, turma=turma)
    sinais.recusar_sinal(utilizador=membro(turma.organizacao), sinal=pedido, motivo="Não consta da lista da turma.")
    assert EmailSaida.objects.filter(destinatario=u.email, assunto__contains="não confirmou").exists()
    with pytest.raises(ErroDominio, match="recusou"):
        services.pedir_selo(utilizador=u, startup=s, turma=turma)


def test_startup_pode_cancelar_o_pedido_e_pedir_outra_vez(fundadora, turma):
    u, s = fundadora
    pedido = services.pedir_selo(utilizador=u, startup=s, turma=turma)
    services.cancelar_pedido_selo(utilizador=u, sinal=pedido)
    assert not Sinal.objects.filter(pk=pedido.pk).exists()
    assert services.pedir_selo(utilizador=u, startup=s, turma=turma).estado == "pendente"


def test_turmas_em_rascunho_ou_de_entidades_por_verificar_nao_aceitam_pedidos(fundadora):
    u, s = fundadora
    ue, org = nova_entidade(email="nova@acelera.test", nif="111111111")
    rascunho = turmas.criar_turma(utilizador=ue, organizacao=org, programa="P", edicao="1",
                                  inicio=date(2026, 1, 1), fim=date(2026, 2, 1))
    assert rascunho not in services.turmas_para_pedido()
    with pytest.raises(ErroDominio, match="não está disponível"):
        services.pedir_selo(utilizador=u, startup=s, turma=rascunho)


def test_outra_entidade_nao_ve_nem_valida_o_pedido(fundadora, turma, admin):
    u, s = fundadora
    pedido = services.pedir_selo(utilizador=u, startup=s, turma=turma)
    u2, org2 = nova_entidade(email="outra@acelera.test", nif="222222222")
    submeter(u2, org2)
    from rasto.organizacoes.services import decidir_verificacao

    decidir_verificacao(admin=admin, organizacao=org2, decisao="verificar", criterios=TODOS_CUMPREM)
    assert pendentes_da_entidade(u2).count() == 0
    with pytest.raises(ErroDominio):
        sinais.validar_sinal(utilizador=u2, sinal=pedido)


def test_so_a_equipa_da_startup_pede_ou_cancela(fundadora, turma):
    u, s = fundadora
    estranho = criar_utilizador("estranho@x.test", "startup")
    with pytest.raises(ErroDominio, match="equipa da startup"):
        services.pedir_selo(utilizador=estranho, startup=s, turma=turma)
    pedido = services.pedir_selo(utilizador=u, startup=s, turma=turma)
    with pytest.raises(ErroDominio, match="não é da sua startup"):
        services.cancelar_pedido_selo(utilizador=estranho, sinal=pedido)


def test_api_registo_e_pedido(client, turma):
    r = client.post("/api/v1/registo/startup", {"nome": "Ana", "nome_startup": "Mbote", "email": "ana@mbote.test",
                                               "palavra_passe": PALAVRA, "consentimento": True}, content_type="application/json")
    assert r.status_code == 201
    d = client.get("/api/v1/startup/selos").json()
    escolha = next(t for e in d["entidades"] for t in e["turmas"] if t["id"] == str(turma.id))
    assert escolha["ja_pedido"] is False
    r = client.post("/api/v1/startup/selos", {"turma": str(turma.id), "nota": "Turma 3"}, content_type="application/json")
    assert r.status_code == 201 and r.json()["estado"] == "pendente"
