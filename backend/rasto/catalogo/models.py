from django.conf import settings
from django.db import models

from rasto.nucleo.models import ModeloBase


class ItemCatalogo(ModeloBase):
    """Listas configuráveis pela administração (D-04): sectores, fases, geografias e níveis de risco.
    Desactivar um item retira-o dos formulários sem mudar o código (base de UX 5.5)."""

    class Tipo(models.TextChoices):
        SECTOR = "sector", "Sector"
        FASE = "fase", "Fase"
        GEOGRAFIA = "geografia", "Geografia"
        RISCO = "risco", "Nível de risco"

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    codigo = models.CharField(max_length=40)
    nome = models.CharField(max_length=80)
    descricao = models.CharField(max_length=160, blank=True)
    ordem = models.PositiveSmallIntegerField(default=0, help_text="Nas fases, a ordem define a adjacência.")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "item de catálogo"
        verbose_name_plural = "catálogo"
        ordering = ["tipo", "ordem", "nome"]
        constraints = [models.UniqueConstraint(fields=["tipo", "codigo"], name="item_catalogo_unico")]

    def __str__(self) -> str:
        return f"{self.get_tipo_display()}: {self.nome}"


class TaxaCambio(models.Model):
    """Taxa de referência USD → Kz definida pela administração (D-05). Os valores guardam-se na moeda de origem
    (ADR-14); a conversão só serve para comparar e mostrar equivalências, sempre com a data da taxa."""

    data = models.DateField(unique=True)
    aoa_por_usd = models.DecimalField(max_digits=12, decimal_places=2)
    definida_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    class Meta:
        verbose_name = "taxa de câmbio de referência"
        verbose_name_plural = "taxas de câmbio de referência"
        ordering = ["-data"]

    def __str__(self) -> str:
        return f"{self.data:%d/%m/%Y}: 1 USD = {self.aoa_por_usd} Kz"


def taxa_actual() -> TaxaCambio | None:
    return TaxaCambio.objects.order_by("-data").first()
