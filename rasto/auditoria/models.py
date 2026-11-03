from django.conf import settings
from django.db import models


class RegistoAuditoria(models.Model):
    """Registo só de acréscimo (ADR-09). Cada linha guarda o hash da anterior; um trigger na base de dados
    recusa UPDATE e DELETE (migração 0002)."""

    id = models.BigAutoField(primary_key=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="+")
    actor_descricao = models.CharField(max_length=160, blank=True)
    accao = models.CharField(max_length=60)
    objecto_tipo = models.CharField(max_length=60)
    objecto_id = models.CharField(max_length=64)
    antes = models.JSONField(null=True, blank=True)
    depois = models.JSONField(null=True, blank=True)
    ip_truncado = models.CharField(max_length=45, blank=True)
    criado_em = models.DateTimeField()
    hash_anterior = models.CharField(max_length=64)
    hash = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "registo de auditoria"
        verbose_name_plural = "registos de auditoria"
        indexes = [models.Index(fields=["objecto_tipo", "objecto_id"])]
        ordering = ["id"]
