import pytest
from django.core.management import call_command

from rasto.acessos.models import PedidoAcesso
from rasto.startups.models import Startup


@pytest.mark.django_db
def test_dados_de_demonstracao_criam_os_cenarios_das_tarefas():
    call_command("semear_demo")
    assert Startup.objects.filter(estado="publicado").count() == 2
    assert PedidoAcesso.objects.filter(estado="pendente").count() == 1
