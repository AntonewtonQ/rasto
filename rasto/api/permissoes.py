"""Primeira camada do controlo de acesso (papel). A segunda (objecto) está nos querysets com âmbito de cada
vista: fora do âmbito a resposta é 404 (base técnica 7.1)."""

from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.views import APIView


class TemPapel(BasePermission):
    message = "Esta área não pertence ao seu papel."

    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.papel_id in getattr(view, "papeis", ()))


class VistaPapel(APIView):
    """Vista que só responde aos papéis indicados em `papeis` (o teste da matriz percorre-as todas)."""

    papeis: tuple[str, ...] = ()
    permission_classes = [TemPapel]


class VistaPublica(APIView):
    """Vista sem sessão obrigatória. Cada uma é revista à mão (lista PUBLICAS no teste da matriz)."""

    publica = True
    permission_classes = [AllowAny]
