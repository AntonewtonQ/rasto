from django.conf import settings
from django.http import JsonResponse

# Caminhos que a administração sem 2FA pode usar: os do allauth (para activar a 2FA e sair) e a identidade.
LIVRES = ("/_allauth/", "/api/v1/eu", "/api/v1/csrf", "/saude", "/api/static/")


class ExigirMfaAdministracao:
    """A 2FA é obrigatória para a administração (base técnica 7.2): sem autenticador TOTP activo, a conta de
    administração só consegue usar os endpoints de configuração da 2FA. A API responde 403 com
    o código «mfa_obrigatoria», que o frontend usa para abrir o ecrã de activação."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        u = request.user
        if u.is_authenticated and u.papel_id == "admin" and not request.path.startswith(LIVRES):
            from allauth.mfa.models import Authenticator

            if not Authenticator.objects.filter(user=u, type=Authenticator.Type.TOTP).exists():
                return JsonResponse({"erro": {"codigo": "mfa_obrigatoria", "mensagem":
                                     "A administração tem de activar a autenticação em dois passos."}}, status=403)
        return self.get_response(request)


class ExpiracaoSessaoAdministracao:
    """Sessões da administração expiram após 2 h de inactividade; as restantes após 14 dias."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        u = request.user
        if u.is_authenticated and u.papel_id == "admin":
            request.session.set_expiry(settings.SESSION_COOKIE_AGE_ADMIN)
        return self.get_response(request)
