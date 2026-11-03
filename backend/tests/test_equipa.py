import pytest
from django.test import Client

from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.organizacoes import services
from rasto.organizacoes.models import MembroOrganizacao

from .conftest import PALAVRA, criar_utilizador

pytestmark = pytest.mark.django_db


def _convidar(entidade_verificada, email="colega@acelera.test"):
    u, org = entidade_verificada
    c, token = services.convidar_membro(utilizador=u, organizacao=org, email=email)
    return u, org, c, token


def test_colega_aceita_e_fica_membro_da_entidade(entidade_verificada):
    _u, org, _c, token = _convidar(entidade_verificada)
    novo = services.aceitar_convite_equipa(token=token, nome="Carlos", palavra_passe=PALAVRA, consentiu=True)
    assert novo.papel_id == "entidade" and novo.consentimentos.exists()
    m = MembroOrganizacao.objects.get(utilizador=novo)
    assert m.organizacao == org and m.funcao == "membro"


def test_convite_de_equipa_so_se_usa_uma_vez(entidade_verificada):
    _u, _org, _c, token = _convidar(entidade_verificada)
    services.aceitar_convite_equipa(token=token, nome="A", palavra_passe=PALAVRA, consentiu=True)
    with pytest.raises(TransicaoInvalida):
        services.aceitar_convite_equipa(token=token, nome="B", palavra_passe=PALAVRA, consentiu=True)


def test_so_o_responsavel_gere_a_equipa(entidade_verificada):
    _u, org, _c, token = _convidar(entidade_verificada)
    membro = services.aceitar_convite_equipa(token=token, nome="M", palavra_passe=PALAVRA, consentiu=True)
    with pytest.raises(ErroDominio, match="responsável"):
        services.convidar_membro(utilizador=membro, organizacao=org, email="outro@acelera.test")


def test_email_com_conta_ou_ja_convidado_e_recusado(entidade_verificada):
    u, org = entidade_verificada
    criar_utilizador("ja@existe.test", "startup")
    with pytest.raises(ErroDominio, match="Já existe uma conta"):
        services.convidar_membro(utilizador=u, organizacao=org, email="ja@existe.test")
    services.convidar_membro(utilizador=u, organizacao=org, email="duas@vezes.test")
    with pytest.raises(ErroDominio, match="pendente"):
        services.convidar_membro(utilizador=u, organizacao=org, email="duas@vezes.test")


def test_entidade_nunca_fica_sem_responsavel_e_membro_retirado_perde_acesso(entidade_verificada):
    u, org, _c, token = _convidar(entidade_verificada)
    novo = services.aceitar_convite_equipa(token=token, nome="M", palavra_passe=PALAVRA, consentiu=True)
    responsavel = MembroOrganizacao.objects.get(utilizador=u)
    with pytest.raises(ErroDominio, match="si próprio"):
        services.retirar_membro(utilizador=u, organizacao=org, membro=responsavel)
    services.retirar_membro(utilizador=u, organizacao=org, membro=MembroOrganizacao.objects.get(utilizador=novo))
    novo.refresh_from_db()
    assert not novo.is_active
    c = Client()
    assert c.login(email=novo.email, password=PALAVRA) is False


def test_api_da_equipa(entidade_verificada, client):
    u, org = entidade_verificada
    client.force_login(u)
    r = client.post("/api/v1/entidade/equipa", {"email": "api@acelera.test"}, content_type="application/json")
    assert r.status_code == 201
    d = client.get("/api/v1/entidade/equipa").json()
    assert d["sou_responsavel"] and d["convites"][0]["email"] == "api@acelera.test" and d["membros"][0]["eu"]
