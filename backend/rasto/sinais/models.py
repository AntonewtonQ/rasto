from django.conf import settings
from django.db import models

from rasto.nucleo.models import ModeloBase
from rasto.organizacoes.models import Organizacao
from rasto.startups.models import Startup
from rasto.turmas.models import Turma


class Sinal(ModeloBase):
    class Tipo(models.TextChoices):
        PARTICIPACAO = "participacao", "Participação num programa"
        MARCO = "marco", "Marco com data"

    class Estado(models.TextChoices):
        DECLARADO = "declarado", "Declarado"
        PENDENTE = "pendente", "Pendente de validação"
        VALIDADO = "validado", "Validado"
        RECUSADO = "recusado", "Recusado"
        EXPIRADO = "expirado", "Expirado"
        RETIRADO = "retirado", "Retirado"

    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="sinais")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    descricao = models.CharField(max_length=200)
    data_facto = models.DateField(null=True, blank=True)
    validador = models.ForeignKey(Organizacao, null=True, blank=True, on_delete=models.PROTECT, related_name="sinais")
    turma = models.ForeignKey(Turma, null=True, blank=True, on_delete=models.SET_NULL, related_name="sinais")
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.DECLARADO)
    evidencia = models.TextField(blank=True)
    frase_validada = models.TextField(blank=True, help_text="Texto exacto que a entidade confirmou.")
    pedido_em = models.DateTimeField(null=True, blank=True)
    expira_em = models.DateTimeField(null=True, blank=True)
    validado_em = models.DateTimeField(null=True, blank=True)
    validado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="+")
    motivo = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "sinais"
        ordering = ["-criado_em"]
        constraints = [
            # "Sem nome e data, não é validado" (base de UX 6.2).
            models.CheckConstraint(
                name="validado_completo",
                condition=~models.Q(estado="validado")
                | (models.Q(validador__isnull=False) & models.Q(validado_por__isnull=False)
                   & models.Q(validado_em__isnull=False) & ~models.Q(frase_validada="")),
            ),
            models.UniqueConstraint(fields=["startup", "turma"], condition=models.Q(tipo="participacao"),
                                    name="uma_participacao_por_turma"),
        ]

    def __str__(self) -> str:
        return self.descricao

    @property
    def estado_visivel(self) -> str:
        """Validado com aviso quando a entidade validadora está suspensa (base de UX 5.4)."""
        if self.estado == self.Estado.VALIDADO and self.validador and \
                self.validador.estado_verificacao == Organizacao.Estado.SUSPENSA:
            return "validado_com_aviso"
        return self.estado
