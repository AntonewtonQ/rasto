"""Fluxo do Sprint 1 de ponta a ponta pela API JSON (especificação de interface, secção 8), com CSRF activo
como no navegador: registo da entidade → verificação → turma → convite → aceitação → validação."""

import re

import pytest
from allauth.mfa.models import Authenticator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from rasto.nucleo.models import EmailSaida

from .conftest import PALAVRA, PDF

pytestmark = pytest.mark.django_db


class Navegador:
    """Cliente com CSRF obrigatório, como o frontend: lê o cookie csrftoken e envia X-CSRFToken."""

    def __init__(self):
        self.c = Client(enforce_csrf_checks=True)
        self.c.get("/api/v1/csrf")

    def _h(self):
        return {"HTTP_X_CSRFTOKEN": self.c.cookies["csrftoken"].value}

    def get(self, url):
        return self.c.get(url)

    def post(self, url, dados=None, **kw):
        if "ficheiro" in (dados or {}):
            return self.c.post(url, dados, **self._h())
        return self.c.post(url, dados or {}, content_type="application/json", **self._h(), **kw)

    def entrar(self, email):
        r = self.post("/_allauth/browser/v1/auth/login", {"email": email, "password": PALAVRA})
        self.c.get("/api/v1/csrf")  # o token muda ao entrar
        return r

    def sair(self):
        r = self.c.delete("/_allauth/browser/v1/auth/session", **self._h())
        self.c.get("/api/v1/csrf")
        return r


def test_fluxo_completo(admin):
    n = Navegador()
    # 1. Registo da entidade (3 passos)
    r = n.post("/api/v1/registo/entidade", {
        "tipo": "aceleradora", "nome_legal": "Acelera Exemplo, Lda", "nif": "5417832019", "site": "https://acelera.example",
        "cidade": "Luanda", "nome": "Teresa Domingos", "email": "teresa@acelera.test", "palavra_passe": PALAVRA,
        "consentimento": True})
    assert r.status_code == 201, r.content
    n.c.get("/api/v1/csrf")
    assert n.get("/api/v1/eu").json()["organizacao"]["estado_verificacao"] == "rascunho"
    r = n.post("/api/v1/entidade/comprovativos", {"descricao": "Certidão", "ficheiro": SimpleUploadedFile("c.pdf", PDF)})
    assert r.status_code == 201, r.content
    r = n.post("/api/v1/entidade/submeter", {"nome_publico": "Acelera Exemplo", "responsavel_nome": "Teresa Domingos",
                                             "responsavel_email": "teresa@acelera.test",
                                             "descricao_programa": "Programa 2025, 10 startups"})
    assert r.status_code == 200 and r.json()["estado_verificacao"] == "submetida"
    org_id = r.json()["id"]

    # 2. Turma em rascunho; convites bloqueados
    r = n.post("/api/v1/turmas", {"programa": "Programa de Aceleração", "edicao": "2026 · Turma 3",
                                  "inicio": "02/03/2026", "fim": "26/06/2026"})
    assert r.status_code == 201 and r.json()["estado"] == "rascunho"
    turma_id = r.json()["id"]
    r = n.post(f"/api/v1/turmas/{turma_id}/convites", {"texto": "x@x.test"})
    assert r.status_code == 400 and "verificada" in r.json()["erro"]["mensagem"]

    # 3. A administração verifica (sessão com 2FA)
    adm = Navegador()
    Authenticator.objects.create(user=admin, type=Authenticator.Type.TOTP, data={"secret": "x"})
    adm.c.force_login(admin)
    adm.c.get("/api/v1/csrf")
    assert adm.get("/api/v1/admin/verificacoes").json()["contagens"]["por_decidir"] == 1
    assert adm.post(f"/api/v1/admin/verificacoes/{org_id}/abrir").json()["organizacao"]["estado_verificacao"] == "em_analise"
    criterios = {c: {"estado": "cumpre", "nota": "ok"} for c in
                 ("existencia_legal", "presenca_publica", "responsavel", "programa_realizado")}
    falta = {**criterios, "presenca_publica": {"estado": "falta", "nota": ""}}
    r = adm.post(f"/api/v1/admin/verificacoes/{org_id}/decisao", {"decisao": "verificar", "criterios": falta})
    assert r.status_code == 400 and "Presença pública" in r.json()["erro"]["mensagem"]
    r = adm.post(f"/api/v1/admin/verificacoes/{org_id}/decisao", {"decisao": "verificar", "criterios": criterios})
    assert r.status_code == 200 and r.json()["organizacao"]["estado_verificacao"] == "verificada"

    # 4. Convites: verificar linha a linha, enviar e criar ligação
    r = n.post(f"/api/v1/turmas/{turma_id}/convites/verificar", {"texto": "nadia@kitanda.test\nmau-email"})
    assert r.json()["enviaveis"] == 1 and r.json()["linhas"][1]["situacao"] == "invalido"
    r = n.post(f"/api/v1/turmas/{turma_id}/convites", {"texto": "nadia@kitanda.test\nmau-email"})
    assert r.status_code == 201 and len(r.json()["enviados"]) == 1
    token = re.search(r"/convite/(\S+)/", EmailSaida.objects.get(destinatario="nadia@kitanda.test").corpo).group(1)
    r = n.post(f"/api/v1/turmas/{turma_id}/convites/ligacao", {"email": "outra@startup.test"})
    assert r.status_code == 201 and r.json()["ligacao"] in r.json()["mensagem"]
    assert n.sair().status_code in (200, 401)

    # 5. A startup aceita e cria conta
    s = Navegador()
    r = s.get(f"/api/v1/convites/publico/{token}")
    assert r.json()["estado"] == "pendente" and r.json()["organizacao"]["nome"] == "Acelera Exemplo"
    r = s.post(f"/api/v1/convites/publico/{token}/aceitar", {"nome": "Nádia Kiala", "nome_startup": "Kitanda Fresca",
                                                             "palavra_passe": PALAVRA, "consentimento": True})
    assert r.status_code == 201, r.content
    s.c.get("/api/v1/csrf")
    inicio = s.get("/api/v1/startup/inicio").json()
    assert inicio["sinais"][0]["estado"] == "pendente"
    assert Navegador().get(f"/api/v1/convites/publico/{token}").json()["estado"] == "aceite"

    # 6. A entidade entra pelo allauth headless e valida em lote
    n2 = Navegador()
    assert n2.entrar("teresa@acelera.test").status_code == 200
    pend = n2.get("/api/v1/validacoes").json()["sinais"]
    assert pend[0]["frase"] == "Kitanda Fresca participou no Programa de Aceleração 2026 · Turma 3 (Mar.–Jun. 2026)."
    r = n2.post("/api/v1/validacoes/lote", {"sinais": [pend[0]["id"]]})
    assert r.status_code == 200 and r.json()["validados"][0]["estado"] == "validado"

    # 7. A startup vê o selo com quem e quando
    sinal = s.get("/api/v1/startup/inicio").json()["sinais"][0]
    assert sinal["estado"] == "validado" and sinal["validador"]["nome"] == "Acelera Exemplo" and sinal["validado_em"]


def test_entrada_errada_e_recuperacao_nao_revelam_contas(admin):
    n = Navegador()
    r = n.post("/_allauth/browser/v1/auth/login", {"email": admin.email, "password": "errada-mas-longa"})
    assert r.status_code == 400
    a = n.post("/_allauth/browser/v1/auth/password/request", {"email": admin.email})
    b = n.post("/_allauth/browser/v1/auth/password/request", {"email": "nao-existe@t.test"})
    assert a.status_code == b.status_code


def test_conflito_de_estado_responde_409(startup_aceite):
    _u, st, token = startup_aceite
    n = Navegador()
    r = n.post(f"/api/v1/convites/publico/{token}/aceitar", {"nome": "X", "nome_startup": "Y",
                                                             "palavra_passe": PALAVRA, "consentimento": True})
    assert r.status_code == 409 and r.json()["erro"]["codigo"] == "transicao_invalida"


def test_cabecalhos_de_seguranca(client):
    r = client.get("/api/v1/eu")
    assert r["X-Frame-Options"] == "DENY" and r["X-Content-Type-Options"] == "nosniff"
    assert "default-src 'self'" in r["Content-Security-Policy"]
