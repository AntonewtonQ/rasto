from django.core.management.base import BaseCommand

from rasto.nucleo.lembretes import enviar_lembretes


class Command(BaseCommand):
    help = "Enfileira os lembretes por e-mail que estão devidos (convites e pedidos de validação aos 7 dias)."

    def handle(self, *args, **opts):
        contagem = enviar_lembretes()
        self.stdout.write("Lembretes: " + ", ".join(f"{k} {v}" for k, v in contagem.items()) + ".")
