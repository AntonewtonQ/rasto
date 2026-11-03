from django.db import connection
from django.http import JsonResponse


def saude(request):
    """Monitor externo: só diz se a base de dados responde. Sem dados internos."""
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
        return JsonResponse({"estado": "ok"})
    except Exception:
        return JsonResponse({"estado": "erro"}, status=503)


def nao_encontrado(request, exception=None):
    return JsonResponse({"erro": {"codigo": "nao_encontrado", "mensagem": "Não encontrado."}}, status=404)


def erro_servidor(request):
    return JsonResponse({"erro": {"codigo": "erro_servidor",
                                  "mensagem": "Ocorreu um erro do nosso lado. Tente de novo dentro de alguns minutos."}},
                        status=500)
