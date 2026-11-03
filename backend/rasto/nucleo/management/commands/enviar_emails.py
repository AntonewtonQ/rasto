from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from rasto.nucleo.models import EmailSaida

MAX_TENTATIVAS = 3


class Command(BaseCommand):
    help = "Envia os e-mails pendentes da fila. Depois de 3 falhas marca «erro» e propaga ao convite."

    def handle(self, *args, **opts):
        enviados = erros = 0
        with transaction.atomic():
            fila = list(EmailSaida.objects.select_for_update(skip_locked=True)
                        .filter(estado=EmailSaida.Estado.PENDENTE).order_by("criado_em")[:100])
            for e in fila:
                e.tentativas += 1
                try:
                    send_mail(e.assunto, e.corpo, None, [e.destinatario], fail_silently=False)
                except Exception as exc:  # erro do servidor de e-mail: tenta de novo até ao limite
                    e.erro = str(exc)[:500]
                    if e.tentativas >= MAX_TENTATIVAS:
                        e.estado = EmailSaida.Estado.ERRO
                        self._propagar_erro(e)
                        erros += 1
                else:
                    e.estado = EmailSaida.Estado.ENVIADO
                    e.enviado_em = timezone.now()
                    enviados += 1
                e.save()
        self.stdout.write(f"E-mails enviados: {enviados}; com erro: {erros}.")

    def _propagar_erro(self, e: EmailSaida):
        if e.objecto_tipo == "turmas.convite" and e.objecto_id:
            from rasto.turmas.models import Convite

            Convite.objects.filter(pk=e.objecto_id, estado=Convite.Estado.PENDENTE).update(
                estado=Convite.Estado.ERRO_ENVIO)
