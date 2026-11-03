"""Teste da matriz de permissões da API (base técnica 7.1, RNF05).

1. Papel: percorre todas as rotas de /api/v1/. Cada vista ou é `VistaPapel` (só os papéis declarados; 403 aos
   outros; 401 sem sessão) ou está na lista PUBLICAS, revista à mão. Uma rota nova sem regra faz o teste falhar.
2. Objecto: uma entidade não vê turmas, convites, sinais nem comprovativos de outra (404).
"""

import uuid

import pytest
from allauth.mfa.models import Authenticator
from django.urls import URLPattern, get_resolver, reverse

from rasto.api.permissoes import VistaPapel, VistaPublica

from .conftest import TODOS_CUMPREM, criar_utilizador, membro, nova_entidade, submeter

pytestmark = pytest.mark.django_db
PAPEIS = ["startup", "investidor", "entidade", "admin"]
PUBLICAS = {"api_csrf", "api_eu", "api_registo_entidade", "api_convite_publico", "api_convite_aceitar",
            "api_convite_recusar", "api_equipa_convite_publico", "api_equipa_convite_aceitar"}
AUTENTICADAS_SEM_PAPEL = {"api_esquema"}


def _rotas_api():
    resolver = get_resolver()
    for p in resolver.url_patterns:
        if getattr(p, "pattern", None) and str(p.pattern) == "api/v1/":
            for q in p.url_patterns:
                if isinstance(q, URLPattern):
                    yield q.name, q


def _url(nome, padrao):
    kw = {}
    for k, conv in padrao.pattern.converters.items():
        tipo = conv.__class__.__name__
        kw[k] = uuid.uuid4() if tipo == "UUIDConverter" else (999999 if tipo == "IntConverter" else "validar")
    return reverse(nome, kwargs=kw)


def _vista(p):
    return getattr(p.callback, "view_class", None)


def _entrar(client, papel):
    u = criar_utilizador(f"{papel}-{uuid.uuid4().hex[:6]}@t.test", papel)
    if papel == "admin":
        Authenticator.objects.create(user=u, type=Authenticator.Type.TOTP, data={"secret": "x"})
    client.force_login(u)
    return u


def test_todas_as_rotas_da_api_tem_regra():
    sem_regra = []
    for nome, p in _rotas_api():
        v = _vista(p)
        if nome in PUBLICAS:
            assert v and issubclass(v, VistaPublica), nome
        elif nome in AUTENTICADAS_SEM_PAPEL:
            continue
        elif not (v and issubclass(v, VistaPapel) and v.papeis):
            sem_regra.append(nome)
    assert not sem_regra, f"Rotas da API sem papéis declarados: {sem_regra}"


@pytest.mark.parametrize("papel", PAPEIS)
def test_cada_papel_so_usa_as_suas_rotas(client, papel):
    _entrar(client, papel)
    for nome, p in _rotas_api():
        v = _vista(p)
        if not (v and issubclass(v, VistaPapel)):
            continue
        metodo = "get" if hasattr(v, "get") else ("post" if hasattr(v, "post") else "delete")
        r = getattr(client, metodo)(_url(nome, p), content_type="application/json")
        if papel in v.papeis:
            assert r.status_code != 403, (nome, papel, r.status_code)
        else:
            assert r.status_code == 403, (nome, papel, r.status_code)
            assert r.json()["erro"]["codigo"] == "sem_permissao"


def test_sem_sessao_responde_401(client):
    for nome, p in _rotas_api():
        v = _vista(p)
        if v and issubclass(v, VistaPapel):
            metodo = "get" if hasattr(v, "get") else "post"
            r = getattr(client, metodo)(_url(nome, p), content_type="application/json")
            assert r.status_code == 401, (nome, r.status_code)


def test_administracao_sem_2fa_so_ve_a_configuracao_da_2fa(client):
    client.force_login(criar_utilizador("adm@t.test", "admin"))
    r = client.get(reverse("api_verificacoes"))
    assert r.status_code == 403 and r.json()["erro"]["codigo"] == "mfa_obrigatoria"
    assert client.get(reverse("api_eu")).status_code == 200


def test_entidade_nao_ve_objectos_de_outra(client, startup_aceite, admin):
    _u, st, _ = startup_aceite
    org = st.turma.organizacao
    u2, org2 = nova_entidade(email="outra@t.test", nif="999999999")
    submeter(u2, org2)
    from rasto.organizacoes.services import decidir_verificacao

    decidir_verificacao(admin=admin, organizacao=org2, decisao="verificar", criterios=TODOS_CUMPREM)
    client.force_login(u2)
    sinal = st.startup.sinais.get()
    comp = org.comprovativos.first()
    assert client.get(reverse("api_turma", args=[st.turma.pk])).status_code == 404
    assert client.post(reverse("api_convite_ligacao", args=[st.turma.pk]), {"email": "x@x.test"},
                       content_type="application/json").status_code == 404
    assert client.post(reverse("api_convite_cancelar", args=[st.convite.pk])).status_code == 404
    assert client.get(reverse("api_validacao", args=[sinal.pk])).status_code == 404
    assert client.post(reverse("api_decidir_validacao", args=[sinal.pk, "validar"])).status_code == 404
    assert client.post(reverse("api_validar_lote"), {"sinais": [str(sinal.pk)]},
                       content_type="application/json").status_code == 400
    assert client.get(reverse("api_comprovativo_ficheiro", args=[comp.pk])).status_code == 404
    client.force_login(membro(org))
    r = client.get(reverse("api_comprovativo_ficheiro", args=[comp.pk]))
    assert r.status_code == 200 and r["Content-Disposition"].startswith("attachment")


def test_escritas_exigem_csrf(startup_aceite):
    from django.test import Client

    _u, st, _ = startup_aceite
    c = Client(enforce_csrf_checks=True)
    c.force_login(membro(st.turma.organizacao))
    r = c.post(reverse("api_convite_ligacao", args=[st.turma.pk]), {"email": "y@y.test"}, content_type="application/json")
    assert r.status_code == 403 and "CSRF" in r.json()["erro"]["mensagem"]
