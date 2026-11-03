import uuid

from django.conf import settings
from django.db import models


class ModeloBase(models.Model):
    """Chave UUID (ADR-13) e datas de criação e alteração, comuns a todos os modelos de domínio."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    actualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EmailSaida(ModeloBase):
    """Fila de e-mails (ADR-07): gravada na mesma transacção da acção; enviada pelo comando enviar_emails."""

    class Estado(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ENVIADO = "enviado", "Enviado"
        ERRO = "erro", "Erro de envio"

    destinatario = models.EmailField()
    assunto = models.CharField(max_length=200)
    corpo = models.TextField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDENTE)
    tentativas = models.PositiveSmallIntegerField(default=0)
    erro = models.TextField(blank=True)
    enviado_em = models.DateTimeField(null=True, blank=True)
    # Objecto que originou o e-mail (ex.: convite), para propagar o estado de entrega.
    objecto_tipo = models.CharField(max_length=40, blank=True)
    objecto_id = models.UUIDField(null=True, blank=True)

    class Meta:
        verbose_name = "e-mail de saída"
        verbose_name_plural = "e-mails de saída"
        indexes = [models.Index(fields=["estado", "criado_em"])]


class Parametro(models.Model):
    """Prazos e outros valores que a administração muda sem programar (D-05)."""

    chave = models.CharField(max_length=60, primary_key=True)
    valor = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200, blank=True)
    alterado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    alterado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "parâmetro"

    def __str__(self) -> str:
        return f"{self.chave} = {self.valor}"


class LembreteEnviado(models.Model):
    """Garante que cada lembrete sai uma só vez por prazo (ver rasto/nucleo/lembretes.py)."""

    regra = models.CharField(max_length=40)
    objecto_tipo = models.CharField(max_length=40)
    objecto_id = models.CharField(max_length=64)
    referencia = models.CharField(max_length=64)
    enviado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "lembrete enviado"
        verbose_name_plural = "lembretes enviados"
        constraints = [models.UniqueConstraint(fields=["regra", "objecto_id", "referencia"], name="lembrete_unico")]
