import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class Papel(models.Model):
    """Uma conta, um papel (base de UX 4.1)."""

    STARTUP = "startup"
    INVESTIDOR = "investidor"
    ENTIDADE = "entidade"
    ADMIN = "admin"

    codigo = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = "papéis"

    def __str__(self) -> str:
        return self.nome


class GestorUtilizador(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        utilizador = self.model(email=self.normalize_email(email).lower(), **extra)
        utilizador.set_password(password)
        utilizador.save(using=self._db)
        return utilizador

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("papel_id", Papel.ADMIN)
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)


class Utilizador(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=120, blank=True)
    papel = models.ForeignKey(Papel, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField("activo", default=True)
    is_staff = models.BooleanField(default=False)
    criado_em = models.DateTimeField(default=timezone.now)
    anonimizado_em = models.DateTimeField(null=True, blank=True)

    objects = GestorUtilizador()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = "utilizador"

    def __str__(self) -> str:
        return self.nome or self.email


class Consentimento(models.Model):
    """Consentimento por finalidade, com a versão do texto aceite e a data (Lei n.º 22/11)."""

    class Finalidade(models.TextChoices):
        CONTA = "conta", "Criação e uso da conta"
        COMUNICACOES = "comunicacoes", "Comunicações por e-mail"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name="consentimentos")
    finalidade = models.CharField(max_length=20, choices=Finalidade.choices)
    versao_texto = models.CharField(max_length=20)
    concedido_em = models.DateTimeField(default=timezone.now)
    retirado_em = models.DateTimeField(null=True, blank=True)


VERSAO_PRIVACIDADE = "2026-11-03"


def registar_consentimento(utilizador: Utilizador, finalidade: str = Consentimento.Finalidade.CONTA) -> Consentimento:
    return Consentimento.objects.create(utilizador=utilizador, finalidade=finalidade, versao_texto=VERSAO_PRIVACIDADE)
