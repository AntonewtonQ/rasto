import json

from django.http import JsonResponse


def nome_de_utilizador(request, credentials):
    """O allauth headless envia JSON ({"email": …}); o django-axes precisa do identificador para bloquear por
    e-mail × IP."""
    if credentials:
        valor = credentials.get("email") or credentials.get("username")
        if valor:
            return str(valor).lower()
    try:
        corpo = json.loads(request.body or b"{}")
    except (ValueError, TypeError):
        corpo = {}
    return str(corpo.get("email", "")).lower() or None


def resposta_bloqueio(request, *args, **kwargs):
    return JsonResponse({"erro": {"codigo": "bloqueado", "mensagem": (
        "Demasiadas tentativas falhadas. Por segurança, a entrada com este e-mail está bloqueada neste "
        "aparelho durante 15 minutos. Pode recuperar a palavra-passe entretanto.")}}, status=429)
