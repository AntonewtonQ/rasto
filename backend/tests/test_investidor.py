"""Sprint 2 (parte 1): investidor, mandato, sugestões explicadas e pedido de acesso consentido (RF20–RF25)."""

from datetime import date, timedelta

import pytest
from django.utils import timezone

from rasto.acessos import services as acessos
from rasto.acessos.models import PedidoAcesso
from rasto.auditoria.models import RegistoAuditoria
from rasto.catalogo.models import ItemCatalogo, TaxaCambio
from rasto.compatibilidade.services import explicar, sugestoes
from rasto.investidores import services as inv_services
from rasto.nucleo.erros import ErroDominio
from rasto.nucleo.models import EmailSaida
from rasto.startups import services as st_services

from .conftest import PALAVRA
from .test_api_fluxo import Navegador

pytestmark = pytest.mark.django_db


def cat(tipo, codigo):
    return ItemCatalogo.objects.get(tipo=tipo, codigo=codigo)


def startup_publicada(email="ana@kitanda.test", nome="Kitanda", sector="agritech", fase="seed", provincia="LUA",
                      valor=200_000, moeda="USD"):
    u, s = st_services.registar_startup(email=email, palavra_passe=PALAVRA, nome="Ana", nome_startup=nome)
    st_services.actualizar_perfil(utilizador=u, startup=s, dados={
        "sector": cat("sector", sector), "fase": cat("fase", fase), "provincia": cat("geografia", provincia),
        "cidade": "Luanda", "resumo": "Liga pequenos produtores a compradores.", "contacto_fundador": "ana@kitanda.test"})
    st_services.definir_ronda(utilizador=u, startup=s, valor_alvo=valor, moeda=moeda, data_inicio=date(2026, 10, 1))
    st_services.publicar(utilizador=u, startup=s)
    s.refresh_from_db()
    return u, s


def investidor(email="rui@fundo.test", sectores=("agritech",), fases=("seed",), geografias=(), cheque=(20_000, 60_000)):
    u, inv = inv_services.registar_investidor(email=email, palavra_passe=PALAVRA, nome="Rui", tipo="anjo")
    inv_services.guardar_mandato(utilizador=u, sectores=[cat("sector", c).id for c in sectores],
                                 fases=[cat("fase", c).id for c in fases],
                                 geografias=[cat("geografia", c).id for c in geografias],
                                 cheque_min=cheque[0], cheque_max=cheque[1], moeda_cheque="USD")
    inv.refresh_from_db()
    return u, inv


def test_publicar_exige_os_obrigatorios():
    u, s = st_services.registar_startup(email="b@b.test", palavra_passe=PALAVRA, nome="B", nome_startup="Beta")
    assert set(st_services.em_falta_para_publicar(s)) >= {"sector", "fase", "província e cidade", "resumo", "ronda"}
    with pytest.raises(ErroDominio):
        st_services.publicar(utilizador=u, startup=s)


def test_compatibilidade_explicada_e_ordenada():
    startup_publicada()
    startup_publicada(email="c@c.test", nome="Fintechx", sector="fintech")
    _, inv = investidor()
    lista = sugestoes(inv.mandato)
    assert [s.nome for s, _ in lista] == ["Kitanda"]
    e = lista[0][1]
    assert e.total >= 60 and e.classificacao == "compativel"
    assert {c["chave"] for c in e.criterios} == {"sector", "fase", "cheque", "geografia", "risco"}
    assert all(c["frase"] for c in e.criterios)
    assert "não a qualidade" in e.como_dict()["aviso"]


def test_ronda_em_kz_precisa_de_taxa():
    _, s = startup_publicada(valor=180_000_000, moeda="AOA")
    _, inv = investidor()
    TaxaCambio.objects.all().delete()
    cheque = next(c for c in explicar(s, inv.mandato).criterios if c["chave"] == "cheque")
    assert cheque["estado"] == "sem_dados"
    TaxaCambio.objects.create(data=date(2026, 11, 1), aoa_por_usd=900)
    cheque = next(c for c in explicar(s, inv.mandato).criterios if c["chave"] == "cheque")
    assert cheque["estado"] in ("total", "parcial")


def test_pedido_aceite_abre_camada_2_e_revogar_fecha():
    fu, s = startup_publicada()
    _, inv = investidor()
    p = acessos.pedir_acesso(investidor=inv, startup=s, nota="Invisto em agritech em Luanda.")
    assert p.pontuacao is not None and p.decomposicao and p.config_versao == 1
    assert EmailSaida.objects.filter(destinatario=fu.email).exists()
    with pytest.raises(ErroDominio):
        acessos.pedir_acesso(investidor=inv, startup=s, nota="outra vez")
    assert not acessos.tem_acesso(inv, s)
    acessos.aceitar(utilizador=fu, pedido=p)
    assert acessos.tem_acesso(inv, s)
    acessos.revogar(utilizador=fu, pedido=p)
    assert not acessos.tem_acesso(inv, s)


def test_recusa_bloqueia_90_dias_e_so_partilha_motivo_se_pedido():
    fu, s = startup_publicada()
    _, inv = investidor()
    p = acessos.pedir_acesso(investidor=inv, startup=s, nota="Olá")
    acessos.recusar(utilizador=fu, pedido=p, motivo="cheque", partilhar=False)
    p.refresh_from_db()
    assert p.motivo_recusa == "cheque" and not p.motivo_partilhado
    assert acessos.bloqueado_ate(inv, s) == timezone.localdate() + timedelta(days=90)
    with pytest.raises(ErroDominio, match="Pode voltar a pedir"):
        acessos.pedir_acesso(investidor=inv, startup=s, nota="Olá de novo")


def test_pedido_expira_e_so_a_equipa_decide():
    fu, s = startup_publicada()
    outra, _ = startup_publicada(email="z@z.test", nome="Zeta")
    _, inv = investidor()
    p = acessos.pedir_acesso(investidor=inv, startup=s, nota="Olá")
    with pytest.raises(ErroDominio):
        acessos.aceitar(utilizador=outra, pedido=p)
    PedidoAcesso.objects.filter(pk=p.pk).update(expira_em=timezone.now() - timedelta(minutes=1))
    assert acessos.expirar_pedidos() == 1
    p.refresh_from_db()
    assert p.estado == "expirado" and p.novo_pedido_a_partir_de


def test_api_investidor_de_ponta_a_ponta():
    fu, s = startup_publicada()
    doc = st_services.adicionar_documento(utilizador=fu, startup=s, titulo="Pitch", url="https://exemplo.org/pitch.pdf")

    i = Navegador()
    r = i.post("/api/v1/registo/investidor", {"nome": "Rui", "tipo": "anjo", "email": "rui@fundo.test",
                                             "palavra_passe": PALAVRA, "consentimento": True})
    assert r.status_code == 201, r.content
    catalogo = i.get("/api/v1/catalogo").json()
    sector = next(x["id"] for x in catalogo["sector"] if x["codigo"] == "agritech")
    fase = next(x["id"] for x in catalogo["fase"] if x["codigo"] == "seed")
    assert i.get("/api/v1/investidor/sugestoes").json()["mandato_incompleto"] is True
    r = i.c.put("/api/v1/investidor/mandato", {"sectores": [sector], "fases": [fase], "cheque_min": 20000,
                                               "cheque_max": 60000, "moeda_cheque": "USD"},
                content_type="application/json", **i._h())
    assert r.status_code == 200 and r.json()["compativeis"] == 1

    sug = i.get("/api/v1/investidor/sugestoes").json()
    assert sug["sugestoes"][0]["startup"]["id"] == str(s.id)
    perfil = i.get(f"/api/v1/startups/{s.id}").json()
    assert perfil["perfil"]["camada"] == 1 and "contacto_fundador" not in perfil["perfil"]
    assert i.get(f"/api/v1/startups/{s.id}/documentos/{doc.id}/abrir").status_code == 404

    r = i.post(f"/api/v1/startups/{s.id}/pedir-acesso", {"nota": "Agritech é o meu foco.", "origem": "sugestao", "posicao": 1})
    assert r.status_code == 201, r.content

    f = Navegador()
    f.entrar(fu.email)
    rec = f.get("/api/v1/startup/pedidos-acesso").json()
    assert len(rec["pendentes"]) == 1 and rec["pendentes"][0]["encaixe"]["total"] >= 60
    pid = rec["pendentes"][0]["id"]
    assert f.post(f"/api/v1/startup/pedidos-acesso/{pid}/aceitar").status_code == 200

    perfil = i.get(f"/api/v1/startups/{s.id}").json()["perfil"]
    assert perfil["camada"] == 2 and perfil["contacto_fundador"]
    assert "url" not in perfil["documentos"][0]
    r = i.get(f"/api/v1/startups/{s.id}/documentos/{doc.id}/abrir")
    assert r.status_code == 302 and r["Location"] == doc.url and r["Referrer-Policy"] == "no-referrer"
    assert RegistoAuditoria.objects.filter(accao="documento_aberto").exists()


def test_startup_nao_publicada_nao_aparece_ao_investidor():
    u, s = st_services.registar_startup(email="b@b.test", palavra_passe=PALAVRA, nome="B", nome_startup="Beta")
    investidor()
    i = Navegador()
    i.entrar("rui@fundo.test")
    assert i.get(f"/api/v1/startups/{s.id}").status_code == 404
    assert i.post(f"/api/v1/startups/{s.id}/pedir-acesso", {"nota": "x"}).status_code in (400, 409)


def test_lembretes_do_pedido_ao_3o_e_10o_dia():
    from rasto.nucleo.lembretes import enviar_lembretes

    fu, s = startup_publicada()
    _, inv = investidor()
    p = acessos.pedir_acesso(investidor=inv, startup=s, nota="Olá")
    assert enviar_lembretes()["pedido_acesso_3_dias"] == 0
    PedidoAcesso.objects.filter(pk=p.pk).update(criado_em=timezone.now() - timedelta(days=4))
    assert enviar_lembretes()["pedido_acesso_3_dias"] == 1
    assert enviar_lembretes()["pedido_acesso_3_dias"] == 0  # idempotente
    PedidoAcesso.objects.filter(pk=p.pk).update(criado_em=timezone.now() - timedelta(days=11))
    r = enviar_lembretes()
    assert r["pedido_acesso_10_dias"] == 1 and r["pedido_acesso_3_dias"] == 0
    assert EmailSaida.objects.filter(destinatario=fu.email, assunto__startswith="Lembrete").count() == 2
