from datetime import date

import pytest
from django.db import IntegrityError, transaction

from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.sinais import services
from rasto.sinais.models import Sinal
from rasto.sinais.selectors import pendentes_da_entidade

from .conftest import TODOS_CUMPREM, membro, nova_entidade, submeter

pytestmark = pytest.mark.django_db


def _sinal(st):
    return Sinal.objects.get(startup=st.startup, turma=st.turma)


def test_validar_guarda_a_frase_exacta_autor_e_data(startup_aceite):
    _u, st, _ = startup_aceite
    gestora = membro(st.turma.organizacao)
    s = services.validar_sinal(utilizador=gestora, sinal=_sinal(st))
    assert s.estado == "validado" and s.validado_por == gestora and s.validado_em
    assert s.frase_validada == "Kitanda Fresca participou no Programa de Aceleração 2026 · Turma 3 (Mar.–Jun. 2026)."


def test_lote_recusa_marcos(startup_aceite):
    _u, st, _ = startup_aceite
    marco = Sinal.objects.create(startup=st.startup, tipo="marco", descricao="MVP lançado", data_facto=date(2026, 3, 1),
                                 validador=st.turma.organizacao, estado="pendente")
    with pytest.raises(ErroDominio, match="um a um"):
        services.validar_em_lote(utilizador=membro(st.turma.organizacao), sinais=[_sinal(st), marco])


def test_recusa_exige_motivo(startup_aceite):
    _u, st, _ = startup_aceite
    with pytest.raises(ErroDominio, match="motivo"):
        services.recusar_sinal(utilizador=membro(st.turma.organizacao), sinal=_sinal(st), motivo="  ")
    s = services.recusar_sinal(utilizador=membro(st.turma.organizacao), sinal=_sinal(st), motivo="Não concluiu o programa")
    assert s.estado == "recusado" and s.motivo == "Não concluiu o programa"


def test_retirar_so_validados_e_com_motivo(startup_aceite):
    _u, st, _ = startup_aceite
    g = membro(st.turma.organizacao)
    with pytest.raises(TransicaoInvalida):
        services.retirar_validacao(utilizador=g, sinal=_sinal(st), motivo="x")
    services.validar_sinal(utilizador=g, sinal=_sinal(st))
    with pytest.raises(ErroDominio, match="motivo"):
        services.retirar_validacao(utilizador=g, sinal=_sinal(st), motivo="")
    assert services.retirar_validacao(utilizador=g, sinal=_sinal(st), motivo="Erro na lista").estado == "retirado"


def test_outra_entidade_nao_valida_nem_ve(startup_aceite, admin):
    _u, st, _ = startup_aceite
    u2, org2 = nova_entidade(email="outra@x.test", nif="987654321")
    submeter(u2, org2)
    from rasto.organizacoes.services import decidir_verificacao

    decidir_verificacao(admin=admin, organizacao=org2, decisao="verificar", criterios=TODOS_CUMPREM)
    with pytest.raises(ErroDominio, match="não está atribuído"):
        services.validar_sinal(utilizador=u2, sinal=_sinal(st))
    assert pendentes_da_entidade(u2).count() == 0


def test_entidade_suspensa_nao_valida(startup_aceite, admin):
    from rasto.organizacoes.services import decidir_verificacao

    _u, st, _ = startup_aceite
    decidir_verificacao(admin=admin, organizacao=st.turma.organizacao, decisao="suspender", motivo="x")
    with pytest.raises(ErroDominio, match="bloqueadas"):
        services.validar_sinal(utilizador=membro(st.turma.organizacao), sinal=_sinal(st))


def test_base_de_dados_recusa_validado_sem_autor(startup_aceite):
    _u, st, _ = startup_aceite
    with pytest.raises(IntegrityError), transaction.atomic():
        Sinal.objects.filter(pk=_sinal(st).pk).update(estado="validado")
