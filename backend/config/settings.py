"""Definições do Rasto. Tudo o que muda entre ambientes vem de variáveis de ambiente (ficheiro .env)."""

import os
import re
from pathlib import Path

from csp.constants import NONE, SELF

BASE_DIR = Path(__file__).resolve().parent.parent


def _carregar_env(caminho: Path) -> None:
    """Lê um .env simples (CHAVE=valor) sem dependências externas; o ambiente real tem prioridade."""
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        valor = re.split(r"\s+#", valor, maxsplit=1)[0]  # comentário no fim da linha
        os.environ.setdefault(chave.strip(), valor.strip())


_carregar_env(BASE_DIR / ".env")


def env(chave: str, defeito: str = "") -> str:
    return os.environ.get(chave, defeito)


DEBUG = env("DJANGO_DEBUG", "0") == "1"
SECRET_KEY = env("DJANGO_SECRET_KEY") or ("dev-inseguro" if DEBUG else "")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY em falta.")
ALLOWED_HOSTS = [h for h in env("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h]
# Nomes internos da rede Docker (o Next.js chama o Django por http://web:8000), definidos no compose.yml.
ALLOWED_HOSTS += [h for h in env("DJANGO_HOSTS_INTERNOS").split(",") if h]
# URL público (o do Next.js, mesma origem que a API através do Caddy ou das rewrites do Next em desenvolvimento).
SITE_URL = env("SITE_URL", "http://localhost:3000").rstrip("/")
# Os pedidos chegam encaminhados pelo Next.js (desenvolvimento) ou pelo Caddy (produção): a origem do navegador é
# o SITE_URL, não o anfitrião interno do Django.
CSRF_TRUSTED_ORIGINS = [SITE_URL] + [f"https://{h}" for h in ALLOWED_HOSTS if h not in ("localhost", "127.0.0.1")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.headless",
    "rest_framework",
    "drf_spectacular",
    "axes",
    "csp",
    "rasto.nucleo",
    "rasto.contas",
    "rasto.auditoria",
    "rasto.organizacoes",
    "rasto.startups",
    "rasto.turmas",
    "rasto.sinais",
    "rasto.api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "axes.middleware.AxesMiddleware",
    "rasto.nucleo.middleware.ExigirMfaAdministracao",
    "rasto.nucleo.middleware.ExpiracaoSessaoAdministracao",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("PGHOST", "localhost"),
        "PORT": env("PGPORT", "5433"),
        "NAME": env("PGDATABASE", "rasto"),
        "USER": env("PGUSER", "rasto"),
        "PASSWORD": env("PGPASSWORD", "rasto"),
        "CONN_MAX_AGE": 60,
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Contas e autenticação ---------------------------------------------------
AUTH_USER_MODEL = "contas.Utilizador"
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LOGIN_URL = "/entrar"
PASSWORD_RESET_TIMEOUT = 3600  # 1 hora

ACCOUNT_ADAPTER = "rasto.contas.adaptador.AdaptadorConta"
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*"]
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED = False
ACCOUNT_PREVENT_ENUMERATION = True
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False  # não enviar e-mails a endereços sem conta (evita abuso do formulário)
ACCOUNT_EMAIL_NOTIFICATIONS = True  # avisar quando a palavra-passe muda
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""  # o assunto já diz «Rasto: …»
ACCOUNT_RATE_LIMITS = {"login_failed": "5/15m/ip,5/15m/key", "reset_password": "5/h/ip,3/h/key"}
MFA_SUPPORTED_TYPES = ["totp", "recovery_codes"]

# allauth headless: entrada, 2FA e recuperação por JSON em /_allauth/browser/v1/ (base técnica 1.5).
HEADLESS_ONLY = True
HEADLESS_CLIENTS = ("browser",)
HEADLESS_SERVE_SPECIFICATION = DEBUG
HEADLESS_FRONTEND_URLS = {
    "account_reset_password": f"{SITE_URL}/recuperar",
    "account_reset_password_from_key": f"{SITE_URL}/recuperar/{{key}}",
    "account_signup": f"{SITE_URL}/registo/entidade",
}

# --- API ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser", "rest_framework.parsers.MultiPartParser"],
    "EXCEPTION_HANDLER": "rasto.api.erros.tratar_excepcao",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle", "rest_framework.throttling.UserRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"anon": "60/min", "user": "600/min"},
    "UNAUTHENTICATED_USER": "django.contrib.auth.models.AnonymousUser",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "API do Rasto",
    "DESCRIPTION": "API JSON da plataforma Rasto (TCC, ISPTEC). Autenticação por sessão; ver /_allauth/browser/v1/.",
    "VERSION": "1",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}
MFA_TOTP_ISSUER = "Rasto"
MFA_RECOVERY_CODE_COUNT = 10

# Força bruta (django-axes): 5 falhas em 15 min por e-mail × IP bloqueiam 15 min.
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 0.25
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
AXES_USERNAME_CALLABLE = "rasto.contas.axes.nome_de_utilizador"
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_CALLABLE = "rasto.contas.axes.resposta_bloqueio"

# --- Sessões e cookies -------------------------------------------------------
SESSION_COOKIE_AGE = 14 * 24 * 3600
SESSION_COOKIE_AGE_ADMIN = 2 * 3600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False  # o frontend lê-o para enviar X-CSRFToken (padrão do Django para pedidos JS)
# DJANGO_SEM_HTTPS=1 só no modo de demonstração em rede local (infra/demo.sh rede): os navegadores não guardam
# cookies «Secure» sem HTTPS. Nunca em staging nem em produção.
SEM_HTTPS = env("DJANGO_SEM_HTTPS", "0") == "1"
if not DEBUG and not SEM_HTTPS:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_NAME = "__Host-sessao"
if not DEBUG:
    SECURE_SSL_REDIRECT = env("DJANGO_SSL_REDIRECT", "1") == "1" and not SEM_HTTPS
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# HSTS preload fica de fora até haver domínio definitivo (inscrever na lista dos navegadores é difícil de desfazer).
# drf_spectacular W001/W002: esquema OpenAPI ainda sem anotações de resposta (pendente do Sprint 2).
SILENCED_SYSTEM_CHECKS = ["security.W021", "drf_spectacular.W001", "drf_spectacular.W002"]
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": [SELF],
        "script-src": [SELF],
        "style-src": [SELF],
        "img-src": [SELF, "data:"],
        "font-src": [SELF],
        "connect-src": [SELF],
        "form-action": [SELF],
        "frame-ancestors": [NONE],
        "base-uri": [SELF],
        "object-src": [NONE],
    }
}

# --- Ficheiros -----------------------------------------------------------------
STATIC_URL = "/api/static/"  # só o admin interno usa ficheiros estáticos do Django
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}
# Ficheiros privados (comprovativos): fora da pasta pública, servidos só por vista autenticada.
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/nao-publico/"
COMPROVATIVO_TAMANHO_MAX = 2 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024

# --- E-mail ----------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "Rasto <nao-responder@localhost>")
# Ordem: ficheiros (testes ponta a ponta) > SMTP (com servidor e credenciais) > consola (desenvolvimento).
# O SMTP nunca envia para domínios reservados (.test, .demo, .example…), usados nos dados fictícios.
if env("EMAIL_FICHEIROS"):
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = env("EMAIL_FICHEIROS")
elif env("EMAIL_HOST") and env("EMAIL_HOST_PASSWORD"):
    EMAIL_BACKEND = "rasto.nucleo.email_backend.SmtpSemDominiosReservados"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = int(env("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 20
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- Local -----------------------------------------------------------------------
LANGUAGE_CODE = "pt-pt"
TIME_ZONE = "Africa/Luanda"
USE_I18N = True
USE_TZ = True

# Prazos de partida (base de UX 5.0); a administração pode alterá-los na tabela Parametro.
PRAZOS_DEFEITO = {
    "convite_dias": 14,
    "verificacao_indicativa_dias_uteis": 3,
    "pedido_informacao_dias": 14,
    "validacao_sinal_dias": 30,
    "lembrete_convite_dias": 7,
    "lembrete_validacao_dias": 7,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"consola": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["consola"], "level": "INFO"},
}
