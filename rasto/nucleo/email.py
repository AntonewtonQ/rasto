from django.template.loader import render_to_string

from .models import EmailSaida


def enfileirar(*, para: str, assunto: str, modelo: str, contexto: dict, objecto=None) -> EmailSaida:
    """Grava o e-mail na fila. Chamar dentro da mesma transacção da acção que o origina."""
    corpo = render_to_string(modelo, contexto)
    return EmailSaida.objects.create(
        destinatario=para,
        assunto=assunto,
        corpo=corpo,
        objecto_tipo=objecto._meta.label_lower if objecto is not None else "",
        objecto_id=objecto.pk if objecto is not None else None,
    )
