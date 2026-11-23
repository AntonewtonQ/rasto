import pytest
from django.core.management import call_command

from rasto.acessos.models import PedidoAcesso
from rasto.actualizacoes.models import Actualizacao
from rasto.pipeline import services as pl
from rasto.pipeline.models import Relacao
from rasto.startups.models import Startup


@pytest.mark.django_db
def test_dados_de_demonstracao_criam_os_cenarios_das_tarefas():
    call_command("semear_demo")
    assert Startup.objects.filter(estado="publicado").count() == 2
    assert PedidoAcesso.objects.filter(estado="pendente").count() == 1
    mbote = Startup.objects.get(nome="Mbote Pagamentos")
    assert Relacao.objects.filter(startup=mbote, lado="startup").count() == 4
    assert pl.indicadores(mbote)["paradas"] == 1
    assert Actualizacao.objects.filter(estado="publicada").count() == 1
    assert Startup.objects.get(nome="Zola Logística").sinais.filter(estado="pendente").exists()
