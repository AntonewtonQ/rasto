from datetime import date

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from rasto.contas.models import Papel, Utilizador
from rasto.organizacoes import services as org_services
from rasto.organizacoes.models import CRITERIOS, MembroOrganizacao, Organizacao
from rasto.turmas import services as turma_services

PALAVRA = "uma-palavra-passe-longa"
TODOS_CUMPREM = {c: {"estado": "cumpre", "nota": "ok"} for c, _, _ in CRITERIOS}
PDF = b"%PDF-1.4 comprovativo de teste"


@pytest.fixture(autouse=True)
def _sem_axes(settings):
    settings.AXES_ENABLED = False
    settings.STORAGES = {**settings.STORAGES, "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}


@pytest.fixture(autouse=True)
def _media(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path / "media"


def criar_utilizador(email, papel, **kw):
    return Utilizador.objects.create_user(email, PALAVRA, papel_id=papel, **kw)


@pytest.fixture
def admin(db):
    return criar_utilizador("admin@rasto.test", Papel.ADMIN, nome="Administração", is_staff=True)


def nova_entidade(email="teresa@acelera.test", nome_legal="Aceleradora Exemplo, Lda", nif="5417832019"):
    u, org = org_services.registar_entidade(email=email, palavra_passe=PALAVRA, nome="Teresa Domingos",
                                            tipo="aceleradora", nome_legal=nome_legal, nif=nif)
    return u, org


def submeter(u, org):
    org_services.adicionar_comprovativo(utilizador=u, organizacao=org, descricao="Certidão",
                                        ficheiro=SimpleUploadedFile("certidao.pdf", PDF, "application/pdf"))
    org_services.submeter_entidade(utilizador=u, organizacao=org, dados={
        "responsavel_nome": "Teresa Domingos", "responsavel_email": u.email,
        "descricao_programa": "Programa de Aceleração 2025, 12 startups"})
    org.refresh_from_db()
    return org


@pytest.fixture
def entidade_verificada(db, admin):
    u, org = nova_entidade()
    submeter(u, org)
    org_services.decidir_verificacao(admin=admin, organizacao=org, decisao="verificar", criterios=TODOS_CUMPREM)
    org.refresh_from_db()
    return u, org


@pytest.fixture
def turma(entidade_verificada):
    u, org = entidade_verificada
    return turma_services.criar_turma(utilizador=u, organizacao=org, programa="Programa de Aceleração",
                                      edicao="2026 · Turma 3", inicio=date(2026, 3, 2), fim=date(2026, 6, 26))


@pytest.fixture
def startup_aceite(turma):
    """Convite por ligação aceite por uma startup nova; devolve (utilizador, startup_turma, token)."""
    u_ent = turma.organizacao.membros.first().utilizador
    _c, url, _m = turma_services.gerar_ligacao_convite(utilizador=u_ent, turma=turma, email="nadia@kitanda.test")
    token = url.rstrip("/").rsplit("/", 1)[-1]
    u, st = turma_services.aceitar_convite_nova_conta(token=token, nome="Nádia Kiala", nome_startup="Kitanda Fresca",
                                                      palavra_passe=PALAVRA, consentiu=True)
    return u, st, token


def membro(org):
    return MembroOrganizacao.objects.filter(organizacao=org).first().utilizador


__all__ = ["Organizacao", "PALAVRA", "TODOS_CUMPREM", "criar_utilizador", "nova_entidade", "submeter", "membro"]
