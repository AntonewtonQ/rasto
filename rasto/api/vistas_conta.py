from django.contrib.auth import login, password_validation
from django.core.exceptions import ValidationError
from django.middleware.csrf import get_token
from rest_framework import serializers
from rest_framework.response import Response

from rasto.organizacoes import services as org_services
from rasto.startups.models import startup_do_utilizador

from . import representacoes as rep
from .permissoes import VistaPublica

BACKEND = "allauth.account.auth_backends.AuthenticationBackend"


def validar_palavra_passe(v: str):
    try:
        password_validation.validate_password(v)
    except ValidationError as e:
        raise serializers.ValidationError(list(e.messages)) from e


def contadores(u) -> dict:
    if u.papel_id == "entidade":
        from rasto.sinais.selectors import pendentes_da_entidade

        return {"validacoes_pendentes": pendentes_da_entidade(u).count()}
    return {}


class Csrf(VistaPublica):
    """Garante o cookie csrftoken; o frontend envia-o depois no cabeçalho X-CSRFToken."""

    def get(self, request):
        return Response({"csrf": get_token(request)})


class Eu(VistaPublica):
    """Quem está autenticado, o papel, a entidade ou startup e os contadores da navegação."""

    def get(self, request):
        u = request.user
        if not u.is_authenticated:
            return Response({"autenticado": False})
        from allauth.mfa.models import Authenticator

        d = {"autenticado": True, "utilizador": rep.utilizador(u),
             "mfa_activa": Authenticator.objects.filter(user=u, type=Authenticator.Type.TOTP).exists(),
             "contadores": contadores(u)}
        if u.papel_id == "entidade":
            org = org_services.organizacao_do_utilizador(u)
            d["organizacao"] = rep.organizacao(org) if org else None
        if u.papel_id == "startup":
            s = startup_do_utilizador(u)
            d["startup"] = {"id": str(s.id), "nome": s.nome, "estado": s.estado} if s else None
        return Response(d)


class RegistoEntidadeIn(serializers.Serializer):
    tipo = serializers.ChoiceField(choices=["aceleradora", "universidade"])
    nome_legal = serializers.CharField(max_length=160)
    nif = serializers.RegexField(r"^\d{9,14}$", max_length=14, error_messages={
        "invalid": "O NIF tem de ter entre 9 e 14 dígitos, sem espaços."})
    site = serializers.URLField(required=False, allow_blank=True)
    cidade = serializers.CharField(max_length=80, required=False, allow_blank=True)
    nome = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    palavra_passe = serializers.CharField(min_length=12, trim_whitespace=False)
    consentimento = serializers.BooleanField()

    def validate_consentimento(self, v):
        if not v:
            raise serializers.ValidationError("Para criar a conta, aceite o aviso de privacidade.")
        return v

    def validate_palavra_passe(self, v):
        validar_palavra_passe(v)
        return v


class RegistoEntidade(VistaPublica):
    """E-01, passo 1: cria a conta e a entidade em rascunho e inicia a sessão."""

    def post(self, request):
        s = RegistoEntidadeIn(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        u, org = org_services.registar_entidade(email=d["email"], palavra_passe=d["palavra_passe"], nome=d["nome"],
                                                tipo=d["tipo"], nome_legal=d["nome_legal"], nif=d["nif"],
                                                site=d.get("site", ""), cidade=d.get("cidade", ""), request=request)
        login(request, u, backend=BACKEND)
        return Response({"utilizador": rep.utilizador(u), "organizacao": rep.organizacao(org, completa=True)}, status=201)
