"""Controlo de acesso em duas camadas (base técnica 7.1).

1. Papel: cada vista da API declara os papéis que aceita (rasto/api/permissoes.py).
2. Objecto: cada vista obtém os objectos através de um queryset já filtrado pelo âmbito do utilizador
   (`obter_no_ambito_ou_404`). Fora do âmbito, a resposta é 404 e não 403, para não revelar que o objecto existe.
"""

from django.http import Http404

STARTUP = "startup"
INVESTIDOR = "investidor"
ENTIDADE = "entidade"
ADMIN = "admin"


def obter_no_ambito_ou_404(queryset, **filtros):
    try:
        return queryset.get(**filtros)
    except (queryset.model.DoesNotExist, ValueError) as exc:
        raise Http404 from exc
