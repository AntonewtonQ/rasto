from datetime import date, timedelta

import pytest
from django.utils import timezone

from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.models import EmailSaida
from rasto.sinais.models import Sinal
from rasto.turmas import services
from rasto.turmas.models import Convite, Turma, hash_token

from .conftest import PALAVRA, criar_utilizador, membro, nova_entidade

pytestmark = pytest.mark.django_db
C = Convite.Estado


def test_frase_de_validacao():
    t = Turma(programa="Programa de Aceleração", edicao="2026 · Turma 3", inicio=date(2026, 3, 2), fim=date(2026, 6, 26))
    assert services.frase_validacao(t, "Kitanda Fresca") == \
        "Kitanda Fresca participou no Programa de Aceleração 2026 · Turma 3 (Mar.–Jun. 2026)."


def test_entidade_por_verificar_cria_turma_em_rascunho_mas_nao_convida():
    u, org = nova_entidade()
    t = services.criar_turma(utilizador=u, organizacao=org, programa="P", edicao="1",
                             inicio=date(2026, 1, 1), fim=date(2026, 2, 1))
    assert t.estado == Turma.Estado.RASCUNHO
    with pytest.raises(ErroDominio, match="verificada"):
        services.enviar_convites(utilizador=u, turma=t, texto="a@a.test")


def test_fim_antes_do_inicio_e_recusado(entidade_verificada):
    u, org = entidade_verificada
    with pytest.raises(ErroDominio, match="é antes do início"):
        services.criar_turma(utilizador=u, organizacao=org, programa="P", edicao="1",
                             inicio=date(2026, 3, 2), fim=date(2026, 2, 26))


def test_validacao_por_linha(turma):
    criar_utilizador("ja@startup.test", "startup")
    criar_utilizador("anjo@fundo.test", "investidor")
    services.enviar_convites(utilizador=membro(turma.organizacao), turma=turma, texto="convidado@x.test")
    linhas = services.validar_lista_emails(turma=turma, texto=(
        "nova@startup.test\nnao-e-email\nja@startup.test\nconvidado@x.test\nNOVA@startup.test\nanjo@fundo.test"))
    assert [linha.situacao for linha in linhas] == ["novo", "invalido", "startup_existente", "ja_convidado",
                                                    "repetido", "outro_papel"]
    assert sum(linha.enviavel for linha in linhas) == 2


def test_linhas_invalidas_nao_bloqueiam_as_validas(turma):
    enviados, _ = services.enviar_convites(utilizador=membro(turma.organizacao), turma=turma,
                                           texto="a@a.test\nlixo\nb@b.test")
    assert len(enviados) == 2
    assert EmailSaida.objects.filter(destinatario__in=["a@a.test", "b@b.test"]).count() == 2


def test_token_guardado_so_como_hash(turma):
    c, url, mensagem = services.gerar_ligacao_convite(utilizador=membro(turma.organizacao), turma=turma, email="z@z.test")
    token = url.rstrip("/").rsplit("/", 1)[-1]
    assert token not in c.token_hash and c.token_hash == hash_token(token)
    assert url in mensagem and "Aceite até" in mensagem


def test_aceitar_cria_conta_startup_turma_e_sinal_pendente(startup_aceite):
    u, st, _ = startup_aceite
    assert u.papel_id == "startup" and u.consentimentos.exists()
    sinal = Sinal.objects.get(startup=st.startup, turma=st.turma)
    assert sinal.estado == Sinal.Estado.PENDENTE and sinal.tipo == "participacao"
    assert sinal.validador == st.turma.organizacao
    assert st.convite.estado == C.ACEITE


def test_convite_so_se_usa_uma_vez(startup_aceite):
    _u, _st, token = startup_aceite
    with pytest.raises(TransicaoInvalida, match="já foi aceite"):
        services.aceitar_convite_nova_conta(token=token, nome="X", nome_startup="Y", palavra_passe=PALAVRA, consentiu=True)


def test_convite_expirado_e_recusado(turma):
    c, url, _ = services.gerar_ligacao_convite(utilizador=membro(turma.organizacao), turma=turma, email="e@e.test")
    Convite.objects.filter(pk=c.pk).update(expira_em=timezone.now() - timedelta(minutes=1))
    token = url.rstrip("/").rsplit("/", 1)[-1]
    with pytest.raises(TransicaoInvalida, match="expirou"):
        services.aceitar_convite_nova_conta(token=token, nome="X", nome_startup="Y", palavra_passe=PALAVRA, consentiu=True)
    c.refresh_from_db()
    assert c.estado == C.EXPIRADO


def test_sem_consentimento_nao_cria_conta(turma):
    _c, url, _ = services.gerar_ligacao_convite(utilizador=membro(turma.organizacao), turma=turma, email="s@s.test")
    with pytest.raises(ErroDominio, match="privacidade"):
        services.aceitar_convite_nova_conta(token=url.rstrip("/").rsplit("/", 1)[-1], nome="X", nome_startup="Y",
                                            palavra_passe=PALAVRA, consentiu=False)


def test_startup_existente_junta_se_a_outra_turma(startup_aceite):
    u, st, _ = startup_aceite
    org = st.turma.organizacao
    t2 = services.criar_turma(utilizador=membro(org), organizacao=org, programa="Programa de Incubação",
                              edicao="2026", inicio=date(2026, 7, 1), fim=date(2026, 10, 30))
    _c, url, _ = services.gerar_ligacao_convite(utilizador=membro(org), turma=t2, email=u.email)
    services.aceitar_convite_conta_existente(token=url.rstrip("/").rsplit("/", 1)[-1], utilizador=u)
    assert st.startup.turmas.count() == 2 and st.startup.sinais.count() == 2


def test_conta_de_outro_papel_nao_aceita_convite(turma):
    investidor = criar_utilizador("i@i.test", "investidor")
    _c, url, _ = services.gerar_ligacao_convite(utilizador=membro(turma.organizacao), turma=turma, email="q@q.test")
    with pytest.raises(ErroDominio, match="conta de startup"):
        services.aceitar_convite_conta_existente(token=url.rstrip("/").rsplit("/", 1)[-1], utilizador=investidor)


def test_reenviar_corrige_email_e_renova_prazo(turma):
    c, _url, _ = services.gerar_ligacao_convite(utilizador=membro(turma.organizacao), turma=turma, email="errado@x.test")
    Convite.objects.filter(pk=c.pk).update(estado=C.ERRO_ENVIO)
    c.refresh_from_db()
    antigo = c.token_hash
    services.reenviar_convite(utilizador=membro(turma.organizacao), convite=c, email="certo@x.test")
    c.refresh_from_db()
    assert c.estado == C.PENDENTE and c.email == "certo@x.test" and c.token_hash != antigo and c.reenvios == 1


def test_cancelar_e_transicoes_proibidas(startup_aceite):
    _u, st, _ = startup_aceite
    with pytest.raises(TransicaoInvalida):
        services.cancelar_convite(utilizador=membro(st.turma.organizacao), convite=st.convite)


def test_expiracao_em_lote(turma):
    c, _, _ = services.gerar_ligacao_convite(utilizador=membro(turma.organizacao), turma=turma, email="l@l.test")
    Convite.objects.filter(pk=c.pk).update(expira_em=timezone.now() - timedelta(days=1))
    assert services.expirar_convites() == 1
