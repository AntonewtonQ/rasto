"""Formato único de erro da API (base técnica 8.1):
{"erro": {"codigo": "...", "mensagem": "...", "campos": {...}}}
400 validação · 401 sem sessão · 403 papel errado · 404 fora do âmbito · 409 conflito de estado · 429 limite."""

from django.core.exceptions import ValidationError as ValidacaoDjango
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from rasto.nucleo.erros import ErroDominio, TransicaoInvalida


def _mensagem(detalhe) -> str:
    if isinstance(detalhe, list):
        return " ".join(_mensagem(d) for d in detalhe)
    if isinstance(detalhe, dict):
        return " ".join(_mensagem(v) for v in detalhe.values())
    return str(detalhe)


def tratar_excepcao(exc, contexto):
    if isinstance(exc, TransicaoInvalida):
        return Response({"erro": {"codigo": "transicao_invalida", "mensagem": str(exc)}}, status=status.HTTP_409_CONFLICT)
    if isinstance(exc, ErroDominio):
        return Response({"erro": {"codigo": "regra_de_negocio", "mensagem": str(exc)}}, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exc, ValidacaoDjango):
        return Response({"erro": {"codigo": "validacao", "mensagem": " ".join(exc.messages)}}, status=400)
    if isinstance(exc, Http404):
        exc = exceptions.NotFound("Não encontrado.")
    resposta = exception_handler(exc, contexto)
    if resposta is None:
        return None
    codigos = {400: "validacao", 401: "sem_sessao", 403: "sem_permissao", 404: "nao_encontrado",
               405: "metodo_nao_permitido", 429: "limite_de_pedidos"}
    corpo = {"codigo": codigos.get(resposta.status_code, "erro"), "mensagem": _mensagem(resposta.data)}
    if isinstance(exc, exceptions.ValidationError) and isinstance(resposta.data, dict):
        corpo["campos"] = {k: [str(x) for x in (v if isinstance(v, list) else [v])] for k, v in resposta.data.items()}
        corpo["mensagem"] = "Há campos a corrigir."
    if resposta.status_code == 403 and isinstance(exc, exceptions.NotAuthenticated):
        resposta.status_code = 401
        corpo["codigo"] = "sem_sessao"
    resposta.data = {"erro": corpo}
    return resposta
