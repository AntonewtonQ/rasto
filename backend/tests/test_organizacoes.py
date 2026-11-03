import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.models import EmailSaida
from rasto.organizacoes import services
from rasto.organizacoes.models import Organizacao
from rasto.sinais.services import validar_sinal

from .conftest import PDF, TODOS_CUMPREM, nova_entidade, submeter

pytestmark = pytest.mark.django_db
E = Organizacao.Estado


def test_registo_cria_conta_entidade_em_rascunho_com_consentimento():
    u, org = nova_entidade()
    assert u.papel_id == "entidade" and org.estado_verificacao == E.RASCUNHO
    assert u.consentimentos.filter(finalidade="conta").exists()


def test_email_repetido_e_recusado():
    nova_entidade()
    with pytest.raises(ErroDominio, match="Já existe uma conta"):
        nova_entidade(nif="5417832020")


def test_submeter_exige_comprovativo():
    u, org = nova_entidade()
    with pytest.raises(ErroDominio, match="comprovativo"):
        services.submeter_entidade(utilizador=u, organizacao=org, dados={
            "responsavel_nome": "T", "responsavel_email": u.email, "descricao_programa": "x"})


@pytest.mark.parametrize("nome,conteudo,erro", [
    ("grande.pdf", b"%PDF" + b"0" * (2 * 1024 * 1024 + 1), "2 MB"),
    ("falso.pdf", b"MZ\x90\x00 executavel", "PDF, JPEG ou PNG"),
])
def test_comprovativo_invalido_e_recusado(nome, conteudo, erro):
    u, org = nova_entidade()
    with pytest.raises(ErroDominio, match=erro):
        services.adicionar_comprovativo(utilizador=u, organizacao=org, descricao="x",
                                        ficheiro=SimpleUploadedFile(nome, conteudo))


def test_submeter_notifica_a_administracao_e_define_prazo(admin):
    u, org = nova_entidade()
    submeter(u, org)
    assert org.estado_verificacao == E.SUBMETIDA and org.prazo_resposta is not None
    assert EmailSaida.objects.filter(destinatario=admin.email).exists()


def test_verificar_exige_os_4_criterios(admin):
    u, org = nova_entidade()
    submeter(u, org)
    criterios = {**TODOS_CUMPREM, "programa_realizado": {"estado": "falta", "nota": ""}}
    with pytest.raises(ErroDominio, match="Programa realizado"):
        services.decidir_verificacao(admin=admin, organizacao=org, decisao="verificar", criterios=criterios)
    services.decidir_verificacao(admin=admin, organizacao=org, decisao="verificar", criterios=TODOS_CUMPREM)
    org.refresh_from_db()
    assert org.estado_verificacao == E.VERIFICADA and org.verificada_por == admin


def test_pedido_de_informacao_envia_o_que_falta_e_a_entidade_responde_sem_recomecar(admin):
    u, org = nova_entidade()
    submeter(u, org)
    criterios = {**TODOS_CUMPREM, "presenca_publica": {"estado": "falta", "nota": "Indique o site ou as redes."}}
    services.decidir_verificacao(admin=admin, organizacao=org, decisao="pedir_info", criterios=criterios)
    org.refresh_from_db()
    assert org.estado_verificacao == E.PEDIDO_INFO and "Indique o site" in org.motivo
    services.adicionar_comprovativo(utilizador=u, organizacao=org, descricao="Outro",
                                    ficheiro=SimpleUploadedFile("site.pdf", PDF))
    services.submeter_entidade(utilizador=u, organizacao=org)
    org.refresh_from_db()
    assert org.estado_verificacao == E.EM_ANALISE


def test_recusar_exige_motivo_e_nao_entidade_nao_decide(admin):
    u, org = nova_entidade()
    submeter(u, org)
    with pytest.raises(ErroDominio, match="motivo"):
        services.decidir_verificacao(admin=admin, organizacao=org, decisao="recusar")
    with pytest.raises(ErroDominio, match="administração"):
        services.decidir_verificacao(admin=u, organizacao=org, decisao="recusar", motivo="x")


def test_transicao_proibida(admin):
    u, org = nova_entidade()  # rascunho
    with pytest.raises(TransicaoInvalida):
        services.decidir_verificacao(admin=admin, organizacao=org, decisao="verificar", criterios=TODOS_CUMPREM)
    with pytest.raises(TransicaoInvalida):
        services.decidir_verificacao(admin=admin, organizacao=org, decisao="suspender", motivo="x")


def test_suspensao_poe_aviso_nos_sinais_validados(admin, startup_aceite):
    _u, st, _t = startup_aceite
    org = st.turma.organizacao
    sinal = st.startup.sinais.get()
    validar_sinal(utilizador=org.membros.first().utilizador, sinal=sinal)
    services.decidir_verificacao(admin=admin, organizacao=org, decisao="suspender", motivo="Denúncia em análise")
    sinal.refresh_from_db()
    assert sinal.estado == "validado" and sinal.estado_visivel == "validado_com_aviso"


def test_pedido_de_informacao_expira_aos_14_dias(admin):
    from datetime import timedelta

    from django.utils import timezone

    u, org = nova_entidade()
    submeter(u, org)
    criterios = {**TODOS_CUMPREM, "responsavel": {"estado": "falta", "nota": "E-mail institucional."}}
    services.decidir_verificacao(admin=admin, organizacao=org, decisao="pedir_info", criterios=criterios)
    assert services.expirar_pedidos_informacao(hoje=timezone.localdate() + timedelta(days=15)) == 1
    org.refresh_from_db()
    assert org.estado_verificacao == E.EXPIRADA
