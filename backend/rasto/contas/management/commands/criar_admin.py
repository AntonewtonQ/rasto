import getpass

from django.core.management.base import BaseCommand, CommandError

from rasto.contas.models import Papel, Utilizador


class Command(BaseCommand):
    help = "Cria uma conta de administração da plataforma (a 2FA é pedida na primeira entrada)."

    def add_arguments(self, parser):
        parser.add_argument("email")
        parser.add_argument("--nome", default="")

    def handle(self, email, nome="", **opts):
        if Utilizador.objects.filter(email__iexact=email).exists():
            raise CommandError("Já existe uma conta com este e-mail.")
        p1 = getpass.getpass("Palavra-passe (12+ caracteres): ")
        if p1 != getpass.getpass("Repetir: ") or len(p1) < 12:
            raise CommandError("As palavras-passe não coincidem ou têm menos de 12 caracteres.")
        Utilizador.objects.create_user(email, p1, nome=nome, papel_id=Papel.ADMIN, is_staff=True)
        self.stdout.write("Conta de administração criada.")
