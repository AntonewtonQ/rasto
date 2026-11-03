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


def startup_do_utilizador(utilizador) -> Startup | None:
    m = MembroStartup.objects.select_related("startup").filter(utilizador=utilizador).first()
    return m.startup if m else None
