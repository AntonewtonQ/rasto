from django.conf import settings
from django.db import models

from rasto.nucleo.models import ModeloBase


class Investidor(ModeloBase):
    """Perfil do investidor. Só é visto pelas startups a quem pede acesso (base de UX 4.7).
    No MVP a conta fica aprovada no registo (decisão de 23/11/2026; Dec-1 da base de UX fica para trabalho futuro)."""

    class Tipo(models.TextChoices):
        ANJO = "anjo", "Investidor anjo"
        FUNDO = "fundo", "Fundo de investimento"
        CORPORATE = "corporate", "Empresa (corporate)"

    class EstadoConta(models.TextChoices):
        APROVADA = "aprovada", "Aprovada"
        SUSPENSA = "suspensa", "Suspensa"

    utilizador = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="investidor")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    organizacao = models.CharField(max_length=160, blank=True, help_text="Fundo ou empresa (vazio para anjos).")
    estado_conta = models.CharField(max_length=20, choices=EstadoConta.choices, default=EstadoConta.APROVADA)

    def __str__(self) -> str:
        return self.utilizador.nome or self.utilizador.email


class Mandato(ModeloBase):
    """O que o investidor procura. Mínimo: sector e fase (base de UX 5.5)."""

    investidor = models.OneToOneField(Investidor, on_delete=models.CASCADE, related_name="mandato")
    sectores = models.ManyToManyField("catalogo.ItemCatalogo", related_name="+", blank=True, limit_choices_to={"tipo": "sector"})
    fases = models.ManyToManyField("catalogo.ItemCatalogo", related_name="+", blank=True, limit_choices_to={"tipo": "fase"})
    geografias = models.ManyToManyField("catalogo.ItemCatalogo", related_name="+", blank=True, limit_choices_to={"tipo": "geografia"})
    risco = models.ForeignKey("catalogo.ItemCatalogo", null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
                              limit_choices_to={"tipo": "risco"})
    cheque_min = models.PositiveBigIntegerField(null=True, blank=True)
    cheque_max = models.PositiveBigIntegerField(null=True, blank=True)
    moeda_cheque = models.CharField(max_length=3, default="USD")

    @property
    def minimo_completo(self) -> bool:
        return self.sectores.exists() and self.fases.exists()
