"""Actualização mensal da startup (RF31; base de UX 5.8). Publicada não muda: corrige-se com outra."""

from django.conf import settings
from django.db import models
from django.db.models import Q

from rasto.nucleo.models import ModeloBase

# Métricas sugeridas por fase [S] [H-10]: lista de partida, a validar nos testes (tarefa S9).
# (código, rótulo, unidade): unidade "kz" = valor em Kz; "n" = número; "meses"; "pct".
METRICAS_POR_FASE = {
    "ideia": [("entrevistas", "Clientes entrevistados", "n"), ("lista_espera", "Pessoas na lista de espera", "n"),
              ("equipa", "Pessoas na equipa", "n")],
    "pre_seed": [("utilizadores_activos", "Utilizadores activos", "n"), ("clientes_pagantes", "Clientes pagantes", "n"),
                 ("receita_mensal", "Receita do mês", "kz"), ("equipa", "Pessoas na equipa", "n")],
    "seed": [("receita_mensal", "Receita do mês", "kz"), ("clientes_pagantes", "Clientes pagantes", "n"),
             ("meses_caixa", "Meses de caixa", "meses"), ("equipa", "Pessoas na equipa", "n")],
    "serie_a": [("receita_mensal", "Receita do mês", "kz"), ("clientes_pagantes", "Clientes pagantes", "n"),
                ("margem_bruta", "Margem bruta", "pct"), ("meses_caixa", "Meses de caixa", "meses"),
                ("equipa", "Pessoas na equipa", "n")],
}
METRICAS_SEM_FASE = METRICAS_POR_FASE["pre_seed"]


class Actualizacao(ModeloBase):
    class Estado(models.TextChoices):
        RASCUNHO = "rascunho", "Rascunho"
        PUBLICADA = "publicada", "Publicada"

    startup = models.ForeignKey("startups.Startup", on_delete=models.CASCADE, related_name="actualizacoes")
    periodo = models.DateField(help_text="Primeiro dia do mês a que se refere.")
    metricas = models.JSONField(default=dict, blank=True)
    destaques = models.CharField(max_length=600, blank=True)
    pedidos_ajuda = models.CharField(max_length=300, blank=True)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.RASCUNHO)
    corrige = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name="correccoes")
    publicada_em = models.DateTimeField(null=True, blank=True)
    publicada_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    class Meta:
        verbose_name = "actualização"
        verbose_name_plural = "actualizações"
        ordering = ["-periodo", "-publicada_em"]
        constraints = [
            models.UniqueConstraint(fields=["startup"], condition=Q(estado="rascunho"), name="um_rascunho_por_startup"),
            models.UniqueConstraint(fields=["startup", "periodo"], condition=Q(estado="publicada", corrige__isnull=True),
                                    name="uma_actualizacao_por_mes"),
        ]
