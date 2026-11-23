from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models.lookups import Exact


class ConfiguracaoCompatibilidade(models.Model):
    """Pesos e limiares da compatibilidade, com versões (RF21, ADR-05). Só uma versão está activa; cada pedido de
    acesso guarda a versão que o pontuou. Alterar = criar uma versão nova (fica na auditoria)."""

    versao = models.PositiveIntegerField(unique=True)
    peso_sector = models.PositiveSmallIntegerField(default=40)
    peso_fase = models.PositiveSmallIntegerField(default=25)
    peso_cheque = models.PositiveSmallIntegerField(default=25)
    peso_geografia = models.PositiveSmallIntegerField(default=10)
    peso_risco = models.PositiveSmallIntegerField(default=0)
    parcela_minima = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("0.10"))
    limiar_compativel = models.PositiveSmallIntegerField(default=60)
    limiar_parcial = models.PositiveSmallIntegerField(default=30)
    activa = models.BooleanField(default=False)
    nota = models.CharField(max_length=200, blank=True)
    criada_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "configuração da compatibilidade"
        verbose_name_plural = "configurações da compatibilidade"
        ordering = ["-versao"]
        constraints = [
            models.CheckConstraint(name="pesos_somam_100", condition=Exact(
                F("peso_sector") + F("peso_fase") + F("peso_cheque") + F("peso_geografia") + F("peso_risco"), 100)),
            models.UniqueConstraint(fields=["activa"], condition=models.Q(activa=True), name="uma_configuracao_activa"),
        ]

    def __str__(self) -> str:
        return f"Versão {self.versao}{' (activa)' if self.activa else ''}"


def configuracao_activa() -> ConfiguracaoCompatibilidade:
    c = ConfiguracaoCompatibilidade.objects.filter(activa=True).first()
    if c is None:
        c = ConfiguracaoCompatibilidade.objects.create(versao=1, activa=True, nota="Valores de partida (base de UX 6.5).")
    return c
