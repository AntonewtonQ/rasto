from django.core.management.base import BaseCommand, CommandError

from rasto.auditoria.services import verificar_cadeia


class Command(BaseCommand):
    help = "Recalcula a cadeia de hash do registo de auditoria e falha se algum registo tiver sido alterado."

    def add_arguments(self, parser):
        parser.add_argument("--silencioso", action="store_true")

    def handle(self, *args, silencioso=False, **opts):
        r = verificar_cadeia()
        if not r.valido:
            raise CommandError(f"Cadeia de auditoria inválida no registo {r.primeiro_erro_id}.")
        if not silencioso:
            self.stdout.write(f"Cadeia de auditoria válida ({r.registos} registos).")
