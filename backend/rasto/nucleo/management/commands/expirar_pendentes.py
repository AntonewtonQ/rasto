from django.core.management.base import BaseCommand

from rasto.acessos.services import expirar_pedidos
from rasto.organizacoes.services import expirar_pedidos_informacao
from rasto.sinais.services import expirar_pedidos_validacao
from rasto.turmas.services import expirar_convites


class Command(BaseCommand):
    help = "Expira convites (14 dias), pedidos de informação (14 dias) e pedidos de validação (30 dias)."

    def handle(self, *args, **opts):
        c = expirar_convites()
        p = expirar_pedidos_informacao()
        s = expirar_pedidos_validacao()
        a = expirar_pedidos()
        self.stdout.write(f"Expirados: {c} convites, {p} pedidos de informação, {s} pedidos de validação, "
                          f"{a} pedidos de acesso.")
