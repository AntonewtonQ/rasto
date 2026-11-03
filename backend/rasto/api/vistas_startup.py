from django.http import Http404
from rest_framework.response import Response

from rasto.sinais.models import Sinal
from rasto.startups.models import startup_do_utilizador

from . import representacoes as rep
from .permissoes import VistaPapel


class InicioStartup(VistaPapel):
    """S-01 (mínimo do Sprint 1): perfil, sinais (incluindo os pendentes, que só a startup vê) e passos."""

    papeis = ("startup",)

    def get(self, request):
        s = startup_do_utilizador(request.user)
        if s is None:
            raise Http404
        sinais = list(Sinal.objects.filter(startup=s).select_related("validador", "turma", "validado_por", "startup"))
        tem_validado = any(x.estado == "validado" for x in sinais)
        return Response({
            "startup": {"id": str(s.id), "nome": s.nome, "estado": s.estado},
            "completude": 10 if tem_validado else 0,
            "sinais": [rep.sinal(x, para_startup=True) for x in sinais],
            "passos": [
                {"texto": "Conta criada a partir do convite", "feito": True},
                {"texto": "Participação confirmada pela entidade", "feito": tem_validado, "selo": tem_validado},
                {"texto": "Perfil mínimo: sector, fase, cidade, resumo e ronda", "feito": False},
                {"texto": "Marcos com data (ex.: MVP lançado)", "feito": False},
            ],
        })
