from django.db import models

from rasto.nucleo.models import ModeloBase


class PedidoAcesso(ModeloBase):
    """Pedido de acesso consentido (base de UX 5.6). Aceite e não revogado = o investidor vê a camada 2.
    Guarda a pontuação e a decomposição do momento do pedido (base técnica 5.2), com a versão dos pesos."""

    class Estado(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ACEITE = "aceite", "Aceite"
        RECUSADO = "recusado", "Recusado"
        EXPIRADO = "expirado", "Expirado"
        RETIRADO = "retirado", "Retirado pelo investidor"
        REVOGADO = "revogado", "Acesso retirado pela startup"

    class Motivo(models.TextChoices):
        NAO_CAPTAR = "nao_captar", "Não estamos a captar investimento neste momento"
        CHEQUE = "cheque", "O valor do cheque não encaixa na nossa ronda"
        FASE_SECTOR = "fase_sector", "A fase ou o sector não encaixam"
        SEM_MOTIVO = "sem_motivo", "Prefiro não indicar motivo"

    investidor = models.ForeignKey("investidores.Investidor", on_delete=models.CASCADE, related_name="pedidos")
    startup = models.ForeignKey("startups.Startup", on_delete=models.CASCADE, related_name="pedidos_acesso")
    nota = models.CharField(max_length=300)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDENTE)
    motivo_recusa = models.CharField(max_length=20, choices=Motivo.choices, blank=True)
    motivo_partilhado = models.BooleanField(default=False)
    pontuacao = models.PositiveSmallIntegerField(null=True, blank=True)
    decomposicao = models.JSONField(default=list)
    config_versao = models.PositiveIntegerField(null=True, blank=True)
    origem = models.CharField(max_length=20, default="perfil")  # sugestao | perfil
    posicao_lista = models.PositiveSmallIntegerField(null=True, blank=True)
    expira_em = models.DateTimeField()
    decidido_em = models.DateTimeField(null=True, blank=True)
    revogado_em = models.DateTimeField(null=True, blank=True)
    novo_pedido_a_partir_de = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-criado_em"]
        constraints = [models.UniqueConstraint(fields=["investidor", "startup"], condition=models.Q(estado="pendente"),
                                               name="um_pedido_pendente_por_par")]
