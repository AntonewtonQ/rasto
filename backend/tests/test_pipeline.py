"""Sprint 2 (parte 2): pipeline com indicadores (RF26–RF30) e actualizações periódicas (RF31)."""

from datetime import date, timedelta

import pytest
from django.db import DatabaseError, IntegrityError, transaction
from django.utils import timezone

from rasto.acessos import services as acessos
from rasto.actualizacoes import services as act
from rasto.actualizacoes.models import Actualizacao
from rasto.catalogo.models import TaxaCambio
from rasto.nucleo.erros import Conflito, ErroDominio, TransicaoInvalida
from rasto.nucleo.lembretes import enviar_lembretes
from rasto.nucleo.models import EmailSaida
from rasto.pipeline import services as pl
from rasto.pipeline.models import MovimentoEtapa, Relacao

from .test_api_fluxo import Navegador
from .test_investidor import investidor, startup_publicada

pytestmark = pytest.mark.django_db


@pytest.fixture
def aceite():
    fu, s = startup_publicada(valor=80_000, moeda="USD")
    iu, inv = investidor()
    p = acessos.pedir_acesso(investidor=inv, startup=s, nota="Olá")
    acessos.aceitar(utilizador=fu, pedido=p)
    return fu, s, iu, inv


def test_aceitar_poe_a_relacao_nos_dois_pipelines_em_contactado(aceite):
    fu, s, iu, inv = aceite
    lado_s = pl.relacoes_do_utilizador(fu).get()
    lado_i = pl.relacoes_do_utilizador(iu).get()
    assert (lado_s.lado, lado_s.etapa, lado_i.lado, lado_i.etapa) == ("startup", 2, "investidor", 2)
    assert lado_s.pk != lado_i.pk  # cada lado tem o seu: o outro nunca sabe a etapa


def test_mover_exige_valor_no_soft_commit_e_detecta_conflito(aceite):
    fu, s, *_ = aceite
    r = pl.relacoes_do_utilizador(fu).get()
    with pytest.raises(ErroDominio, match="valor indicativo"):
        pl.mover(utilizador=fu, relacao=r, etapa=5, versao=r.versao)
    v = r.versao
    r = pl.mover(utilizador=fu, relacao=r, etapa=5, versao=v, valor=10_000, moeda="USD")
    assert r.etapa == 5 and r.versao == v + 1
    with pytest.raises(Conflito):
        pl.mover(utilizador=fu, relacao=r, etapa=6, versao=v)
    assert MovimentoEtapa.objects.filter(relacao=r).count() == 2


def test_perdida_exige_motivo_e_desfazer_mantem_a_etapa(aceite):
    fu, *_ = aceite
    r = pl.relacoes_do_utilizador(fu).get()
    with pytest.raises(ErroDominio):
        pl.marcar_perdida(utilizador=fu, relacao=r, motivo="")
    r = pl.marcar_perdida(utilizador=fu, relacao=r, motivo="sem_resposta", nota="Não respondeu")
    with pytest.raises(TransicaoInvalida):
        pl.mover(utilizador=fu, relacao=r, etapa=3)
    r = pl.desfazer_perda(utilizador=fu, relacao=r)
    assert r.perdida_em is None and r.etapa == 2


def test_restricoes_da_base_de_dados(aceite):
    _, s, *_ = aceite
    with pytest.raises(IntegrityError), transaction.atomic():
        Relacao.objects.create(lado="startup", startup=s, etapa=5)  # sem contraparte nem valor
    with pytest.raises(IntegrityError), transaction.atomic():
        Relacao.objects.create(lado="startup", startup=s, contacto_externo="X", etapa=8)


def test_outro_utilizador_nao_mexe_na_relacao(aceite):
    fu, s, iu, _ = aceite
    r_s = pl.relacoes_do_utilizador(fu).get()
    with pytest.raises(ErroDominio):
        pl.mover(utilizador=iu, relacao=r_s, etapa=3)


def test_indicadores_do_exemplo_da_hu19(aceite):
    """Soft commits de Kz 18 400 000 e USD 10 000 numa ronda de USD 80 000 com taxa 920 → 37,5%."""
    fu, s, *_ = aceite
    TaxaCambio.objects.all().delete()
    TaxaCambio.objects.create(data=date(2026, 11, 1), aoa_por_usd=920)
    r = pl.relacoes_do_utilizador(fu).get()
    pl.mover(utilizador=fu, relacao=r, etapa=5, valor=10_000, moeda="USD")
    e = pl.adicionar_externo(utilizador=fu, startup=s, nome="Grupo Kalandula")
    pl.mover(utilizador=fu, relacao=e, etapa=5, valor=18_400_000, moeda="AOA")
    pl.adicionar_externo(utilizador=fu, startup=s, nome="Fundo Teste")
    i = pl.indicadores(s)
    assert i["comprometido"]["pct"] == 37.5 and i["comprometido"]["valor"] == 30_000
    assert i["conversao"] is not None and i["conversao"][0]["chegaram"] == 3
    assert i["dias_ate_soft_commit"] is not None
    TaxaCambio.objects.all().delete()
    assert pl.indicadores(s)["comprometido"]["pct"] is None  # sem taxa não se mostra um valor subestimado


def test_conversao_so_com_tres_relacoes(aceite):
    _, s, *_ = aceite
    assert pl.indicadores(s)["conversao"] is None


def test_relacao_parada_tem_lembrete_e_adiar_suspende(aceite):
    fu, s, iu, _ = aceite
    antigo = timezone.now() - timedelta(days=22)
    Relacao.objects.update(criado_em=antigo)
    MovimentoEtapa.objects.update(criado_em=antigo)
    r = enviar_lembretes()
    assert r["relacao_parada"] == 2  # um lembrete por lado
    assert enviar_lembretes()["relacao_parada"] == 0
    rel = pl.relacoes_do_utilizador(fu).get()
    pl.adiar_lembrete(utilizador=fu, relacao=rel)
    assert not pl.esta_parada(pl.relacoes_do_utilizador(fu).get())
    pl.registar_interaccao(utilizador=iu, relacao=pl.relacoes_do_utilizador(iu).get(), tipo="contacto", texto="Ligou")
    assert not pl.esta_parada(pl.relacoes_do_utilizador(iu).get())


def test_actualizacao_publicada_nao_muda_e_vai_para_quem_tem_acesso(aceite):
    fu, s, iu, _ = aceite
    periodo = act.mes_anterior()
    a = act.guardar_rascunho(utilizador=fu, startup=s, periodo=periodo, metricas={"receita_mensal": "1 200 000"},
                             destaques="Primeiro cliente em Benguela.")
    a = act.publicar(utilizador=fu, actualizacao=a)
    assert EmailSaida.objects.filter(destinatario=iu.email, objecto_id=a.id).exists()
    with pytest.raises(DatabaseError), transaction.atomic():
        Actualizacao.objects.filter(pk=a.pk).update(destaques="mudado")
    with pytest.raises(ErroDominio, match="correcção"):
        act.guardar_rascunho(utilizador=fu, startup=s, periodo=periodo, metricas={})
    c = act.guardar_rascunho(utilizador=fu, startup=s, periodo=periodo, metricas={"receita_mensal": 1_100_000}, corrige=a)
    act.publicar(utilizador=fu, actualizacao=c)
    modelo = {m["codigo"]: m for m in act.modelo(s)}
    assert modelo["receita_mensal"]["anterior"] == 1_100_000


def test_lembrete_mensal_da_actualizacao(aceite, settings):
    _, s, *_ = aceite
    from rasto.startups.models import Startup

    Startup.objects.filter(pk=s.pk).update(publicado_em=timezone.now() - timedelta(days=60))
    settings.PRAZOS_DEFEITO = {**settings.PRAZOS_DEFEITO, "lembrete_actualizacao_dia": 1}
    assert enviar_lembretes()["actualizacao_mensal"] == 1
    assert enviar_lembretes()["actualizacao_mensal"] == 0


def test_api_pipeline_e_actualizacoes(aceite):
    fu, s, iu, _ = aceite
    f = Navegador()
    f.entrar(fu.email)
    q = f.get("/api/v1/startup/pipeline").json()
    assert len(q["relacoes"]) == 1 and len(q["etapas"]) == 7
    rid = q["relacoes"][0]["id"]
    r = f.post(f"/api/v1/pipeline/{rid}/mover", {"etapa": 3, "versao": q["relacoes"][0]["versao"]})
    assert r.status_code == 200 and r.json()["etapa_nome"] == "Reunião"
    assert f.post(f"/api/v1/pipeline/{rid}/mover", {"etapa": 4, "versao": 1}).status_code == 409
    assert f.post("/api/v1/startup/pipeline", {"nome": "Ana Externa", "organizacao": "Clube de anjos"}).status_code == 201

    i = Navegador()
    i.entrar(iu.email)
    assert i.get(f"/api/v1/pipeline/{rid}").status_code == 404  # a relação do lado da startup não é do investidor
    assert len(i.get("/api/v1/investidor/pipeline").json()["relacoes"]) == 1

    r = f.c.put("/api/v1/startup/actualizacoes", {"periodo": act.mes_anterior().isoformat(), "metricas": {"clientes_pagantes": "12"},
                                                  "destaques": "Novo contrato."}, content_type="application/json", **f._h())
    assert r.status_code == 200, r.content
    assert f.post("/api/v1/startup/actualizacoes").status_code == 201
    perfil = i.get(f"/api/v1/startups/{s.id}").json()["perfil"]
    assert perfil["actualizacoes"][0]["destaques"] == "Novo contrato."
