from django.conf import settings
from django.db import models

from rasto.nucleo.models import ModeloBase


class Startup(ModeloBase):
    """No Sprint 1 só tem nome e estado; o perfil completo entra no Sprint 2."""

    class Estado(models.TextChoices):
        RASCUNHO = "rascunho", "Rascunho"
        PUBLICADO = "publicado", "Publicado"
        DESPUBLICADO = "despublicado", "Despublicado"

    nome = models.CharField(max_length=120)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.RASCUNHO)
    publicado_em = models.DateTimeField(null=True, blank=True)
    # Perfil (camada 1: qualquer investidor autenticado vê, depois de publicado)
    sector = models.ForeignKey("catalogo.ItemCatalogo", null=True, blank=True, on_delete=models.PROTECT, related_name="+",
                               limit_choices_to={"tipo": "sector"})
    fase = models.ForeignKey("catalogo.ItemCatalogo", null=True, blank=True, on_delete=models.PROTECT, related_name="+",
                             limit_choices_to={"tipo": "fase"})
    provincia = models.ForeignKey("catalogo.ItemCatalogo", null=True, blank=True, on_delete=models.PROTECT, related_name="+",
                                  limit_choices_to={"tipo": "geografia"})
    cidade = models.CharField(max_length=80, blank=True)
    resumo = models.CharField(max_length=280, blank=True)
    # Camada 2: só investidores com pedido de acesso aceite
    contacto_fundador = models.CharField(max_length=160, blank=True, help_text="E-mail ou telefone para os investidores com acesso.")

    def __str__(self) -> str:
        return self.nome


class MembroStartup(models.Model):
    class Funcao(models.TextChoices):
        FUNDADOR = "fundador", "Fundador(a)"
        MEMBRO = "membro", "Membro"

    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="membros_startup")
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="membros")
    funcao = models.CharField(max_length=20, choices=Funcao.choices, default=Funcao.FUNDADOR)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["utilizador", "startup"], name="membro_startup_unico")]


class Ronda(ModeloBase):
    """Ronda em curso. Valor inteiro na moeda de origem (ADR-14)."""

    class Moeda(models.TextChoices):
        AOA = "AOA", "Kz"
        USD = "USD", "USD"

    class Estado(models.TextChoices):
        ABERTA = "aberta", "Aberta"
        FECHADA = "fechada", "Fechada"

    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="rondas")
    valor_alvo = models.PositiveBigIntegerField()
    moeda = models.CharField(max_length=3, choices=Moeda.choices, default=Moeda.USD)
    data_inicio = models.DateField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ABERTA)

    class Meta:
        ordering = ["-data_inicio"]
        constraints = [models.UniqueConstraint(fields=["startup"], condition=models.Q(estado="aberta"), name="uma_ronda_aberta")]


class DocumentoLigacao(ModeloBase):
    """Ligação externa para um documento (cofre fora do escopo, ADR-06). O investidor só lhe chega por
    /startups/<id>/documentos/<doc>/abrir, depois de o pedido de acesso ser aceite."""

    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="documentos")
    titulo = models.CharField(max_length=120)
    url = models.URLField(max_length=500)

    class Meta:
        ordering = ["criado_em"]


def startup_do_utilizador(utilizador) -> Startup | None:
    m = MembroStartup.objects.select_related("startup").filter(utilizador=utilizador).first()
    return m.startup if m else None


class ConviteMembroStartup(ModeloBase):
    """Convite de um fundador a um colega para a equipa da startup. Uso único; só o hash do token é guardado."""

    class Estado(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ACEITE = "aceite", "Aceite"
        EXPIRADO = "expirado", "Expirado"
        CANCELADO = "cancelado", "Cancelado"

    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="convites_equipa")
    email = models.EmailField()
    token_hash = models.CharField(max_length=64, unique=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDENTE)
    expira_em = models.DateTimeField()
    enviado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    aceite_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-criado_em"]
        constraints = [models.UniqueConstraint(models.functions.Lower("email"), "startup",
                                               condition=models.Q(estado="pendente"), name="convite_startup_pendente_unico")]
