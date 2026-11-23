"""Pipeline privado de cada lado (RF26–RF30; base técnica 4.1–4.3). Perdido não é etapa: é `perdida_em`."""

from django.conf import settings
from django.db import models
from django.db.models import Q

from rasto.nucleo.models import ModeloBase

ETAPAS = [(1, "identificado", "Identificado"), (2, "contactado", "Contactado"), (3, "reuniao", "Reunião"),
          (4, "analise", "Análise"), (5, "soft_commit", "Soft commit"), (6, "term_sheet", "Term sheet"),
          (7, "fechado", "Fechado")]
NOME_ETAPA = {n: nome for n, _, nome in ETAPAS}
SOFT_COMMIT, FECHADO = 5, 7

# Base de UX 5.7: lista fechada + Outro [S] [H-11]
MOTIVOS_PERDA = {
    "startup": [("sem_resposta", "Sem resposta do investidor"), ("fase", "Fase não encaixa"),
                ("cheque", "Valor do cheque não encaixa"), ("sector", "Sector não encaixa"),
                ("condicoes", "Condições não aceites"), ("nao_avancar", "Decidimos não avançar"), ("outro", "Outro")],
    "investidor": [("mandato", "Fora do mandato"), ("equipa", "Equipa"), ("traccao", "Tracção insuficiente"),
                   ("valorizacao", "Valorização"), ("capacidade", "Sem capacidade neste momento"), ("outro", "Outro")],
}


class Relacao(ModeloBase):
    class Lado(models.TextChoices):
        STARTUP = "startup", "Startup"
        INVESTIDOR = "investidor", "Investidor"

    lado = models.CharField(max_length=10, choices=Lado.choices)
    startup = models.ForeignKey("startups.Startup", on_delete=models.CASCADE, related_name="relacoes")
    investidor = models.ForeignKey("investidores.Investidor", null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="relacoes")
    contacto_externo = models.CharField(max_length=160, blank=True, help_text="Nome e organização, se fora da plataforma.")
    ronda = models.ForeignKey("startups.Ronda", null=True, blank=True, on_delete=models.SET_NULL, related_name="relacoes")
    pedido = models.ForeignKey("acessos.PedidoAcesso", null=True, blank=True, on_delete=models.SET_NULL, related_name="relacoes")
    etapa = models.PositiveSmallIntegerField(default=1, choices=[(n, nome) for n, _, nome in ETAPAS])
    valor_indicativo = models.BigIntegerField(null=True, blank=True)
    moeda = models.CharField(max_length=3, blank=True)
    motivo_perda = models.CharField(max_length=20, blank=True)
    nota_perda_privada = models.CharField(max_length=300, blank=True)
    perdida_em = models.DateTimeField(null=True, blank=True)
    lembrete_adiado_ate = models.DateTimeField(null=True, blank=True)
    versao = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "relação do pipeline"
        verbose_name_plural = "relações do pipeline"
        ordering = ["-actualizado_em"]
        constraints = [
            models.CheckConstraint(condition=Q(etapa__gte=1, etapa__lte=7), name="relacao_etapa_1_7"),
            models.CheckConstraint(condition=Q(perdida_em__isnull=True) | ~Q(motivo_perda=""), name="relacao_perdida_tem_motivo"),
            models.CheckConstraint(condition=Q(etapa__lt=5) | Q(perdida_em__isnull=False) | Q(valor_indicativo__isnull=False),
                                   name="relacao_soft_commit_tem_valor"),
            models.CheckConstraint(condition=~Q(lado="startup") | Q(investidor__isnull=False) | ~Q(contacto_externo=""),
                                   name="relacao_startup_tem_contraparte"),
            models.CheckConstraint(condition=~Q(lado="investidor") | Q(investidor__isnull=False), name="relacao_investidor_tem_dono"),
            models.UniqueConstraint(fields=["lado", "startup", "investidor"], condition=Q(investidor__isnull=False),
                                    name="relacao_unica_por_par"),
        ]

    @property
    def externa(self) -> bool:
        return self.investidor_id is None

    def __str__(self) -> str:
        return f"{self.lado}: {self.startup} × {self.investidor or self.contacto_externo}"


class MovimentoEtapa(models.Model):
    """Cada mudança de etapa (incluindo a inicial, com `etapa_de` nulo): base dos indicadores (6.1)."""

    relacao = models.ForeignKey(Relacao, on_delete=models.CASCADE, related_name="movimentos")
    etapa_de = models.PositiveSmallIntegerField(null=True, blank=True)
    etapa_para = models.PositiveSmallIntegerField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["criado_em"]


class Interaccao(models.Model):
    class Tipo(models.TextChoices):
        REUNIAO = "reuniao", "Reunião"
        CONTACTO = "contacto", "Contacto"
        NOTA = "nota", "Nota"

    relacao = models.ForeignKey(Relacao, on_delete=models.CASCADE, related_name="interaccoes")
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    ocorreu_em = models.DateTimeField()
    texto = models.CharField(max_length=600, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-ocorreu_em"]
