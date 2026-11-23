import pytest
from hypothesis import given
from hypothesis import strategies as st

from rasto.compatibilidade.dominio import (
    Configuracao,
    Estado,
    Mandato,
    PerfilStartup,
    pontuar,
)

CFG = Configuracao(versao=1, peso_sector=40, peso_fase=25, peso_cheque=25, peso_geografia=10, peso_risco=0)
PRE_SEED, SEED = 2, 3
AGRI = "agritech"


def startup(**kw):
    base = dict(sector=AGRI, fase_ordem=PRE_SEED, ronda_usd=80_000, provincia="LUA")
    return PerfilStartup(**{**base, **kw})


def mandato(**kw):
    base = dict(
        sectores=frozenset({AGRI}),
        fases_ordem=frozenset({PRE_SEED}),
        cheque_min_usd=5_000,
        cheque_max_usd=100_000,
        geografias=frozenset({"LUA"}),
    )
    # 5 000 ≤ α·V = 8 000 e 100 000 ≥ V = 80 000: o cheque cobre toda a parcela típica
    return Mandato(**{**base, **kw})


def pontos(r, chave):
    return next(c for c in r.criterios if c.chave == chave)


def test_encaixe_total_da_100():
    r = pontuar(startup(), mandato(), CFG)
    assert r.total == 100 and r.classificacao == "compativel"


def test_pesos_que_nao_somam_100_sao_recusados():
    with pytest.raises(ValueError, match="soma actual: 95"):
        Configuracao(versao=2, peso_sector=40, peso_fase=25, peso_cheque=20, peso_geografia=10, peso_risco=0)


def test_fase_adjacente_vale_metade_arredondada_para_cima():
    r = pontuar(startup(fase_ordem=SEED), mandato(), CFG)
    assert pontos(r, "fase").pontos == 13  # 25 × 0,5 = 12,5 → 13
    assert pontos(r, "fase").estado is Estado.PARCIAL


def test_cheque_parcial_exemplo_da_base_de_ux():
    r = pontuar(startup(), mandato(cheque_min_usd=10_000, cheque_max_usd=50_000), CFG)
    assert pontos(r, "cheque").pontos == 14  # 40 000 / 72 000 × 25
    assert pontos(r, "cheque").estado is Estado.PARCIAL


def test_cheque_minimo_acima_da_ronda_nao_encaixa():
    r = pontuar(startup(ronda_usd=50_000), mandato(cheque_min_usd=60_000, cheque_max_usd=200_000), CFG)
    assert pontos(r, "cheque").pontos == 0 and pontos(r, "cheque").estado is Estado.NENHUM


def test_ronda_em_falta_e_sem_dados_e_nao_sem_encaixe():
    r = pontuar(startup(ronda_usd=None), mandato(), CFG)
    c = pontos(r, "cheque")
    assert c.pontos == 0 and c.estado is Estado.SEM_DADOS


def test_mandato_sem_cheque_nem_geografia_nao_penaliza():
    r = pontuar(startup(), mandato(cheque_min_usd=None, cheque_max_usd=None, geografias=frozenset()), CFG)
    assert r.total == 100
    assert pontos(r, "cheque").estado is Estado.SEM_RESTRICAO


def test_angola_generica_cobre_qualquer_provincia():
    r = pontuar(startup(provincia="HUI"), mandato(geografias=frozenset({"AO"})), CFG)
    assert pontos(r, "geografia").pontos == 10


def test_sector_fora_nunca_e_compativel_mesmo_com_pontuacao_alta():
    cfg = Configuracao(
        versao=3, peso_sector=10, peso_fase=40, peso_cheque=40, peso_geografia=10, peso_risco=0
    )
    r = pontuar(startup(sector="fintech"), mandato(), cfg)
    assert r.total == 90 and r.classificacao == "parcial"


def test_risco_com_peso_zero_aparece_sem_pontos():
    r = pontuar(startup(), mandato(), CFG)
    assert pontos(r, "risco").estado is Estado.SEM_PESO and pontos(r, "risco").pontos == 0


def test_pesos_sao_lidos_da_configuracao():
    cfg = Configuracao(
        versao=4, peso_sector=25, peso_fase=25, peso_cheque=25, peso_geografia=25, peso_risco=0
    )
    r = pontuar(startup(provincia="BGO"), mandato(), cfg)
    assert r.total == 75 and r.versao_config == 4


@given(
    fase=st.integers(1, 5),
    ronda=st.one_of(st.none(), st.integers(1, 10_000_000)),
    cmax=st.one_of(st.none(), st.integers(1, 10_000_000)),
)
def test_decomposicao_soma_sempre_o_total_e_fica_entre_0_e_100(fase, ronda, cmax):
    r = pontuar(
        startup(fase_ordem=fase, ronda_usd=ronda), mandato(cheque_min_usd=None, cheque_max_usd=cmax), CFG
    )
    assert r.total == sum(c.pontos for c in r.criterios)
    assert 0 <= r.total <= 100
