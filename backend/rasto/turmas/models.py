import hashlib

from django.conf import settings
from django.db import models
from django.db.models.functions import Lower

from rasto.nucleo.formatos import fmt_periodo
from rasto.nucleo.models import ModeloBase
from rasto.organizacoes.models import Organizacao
from rasto.startups.models import Startup


class Turma(ModeloBase):
    class Estado(models.TextChoices):
        RASCUNHO = "rascunho", "Rascunho"
        ACTIVA = "activa", "Activa"
        ENCERRADA = "encerrada", "Encerrada"

    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, related_name="turmas")
    programa = models.CharField(max_length=120)
    edicao = models.CharField(max_length=60)
    inicio = models.DateField()
    fim = models.DateField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.RASCUNHO)
    criada_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")

    class Meta:
        ordering = ["-inicio"]
        constraints = [models.CheckConstraint(condition=models.Q(fim__gte=models.F("inicio")), name="turma_fim_depois_inicio")]

    def __str__(self) -> str:
        return f"{self.programa} {self.edicao}"

    @property
    def periodo(self) -> str:
        return fmt_periodo(self.inicio, self.fim)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class Convite(ModeloBase):
    class Estado(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ACEITE = "aceite", "Aceite"
        RECUSADO = "recusado", "Recusado"
        EXPIRADO = "expirado", "Expirado"
        CANCELADO = "cancelado", "Cancelado"
        ERRO_ENVIO = "erro_envio", "Erro de envio"

    class Canal(models.TextChoices):
        EMAIL = "email", "E-mail"
        LIGACAO = "ligacao", "Ligação"

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="convites")
    email = models.EmailField()
    token_hash = models.CharField(max_length=64, unique=True)  # o token em claro nunca é guardado
    canal = models.CharField(max_length=10, choices=Canal.choices, default=Canal.EMAIL)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDENTE)
    expira_em = models.DateTimeField()
    aceite_em = models.DateTimeField(null=True, blank=True)
    enviado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    reenvios = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-criado_em"]
        constraints = [
            models.UniqueConstraint(Lower("email"), "turma", name="convite_activo_unico_por_turma",
                                    condition=models.Q(estado__in=["pendente", "aceite", "erro_envio"])),
        ]


class StartupTurma(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="turmas")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="startups")
    convite = models.OneToOneField(Convite, null=True, on_delete=models.SET_NULL, related_name="participacao")
    entrou_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["startup", "turma"], name="startup_turma_unica")]
