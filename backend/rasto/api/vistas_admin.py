from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response

from rasto.nucleo.politicas import obter_no_ambito_ou_404
from rasto.organizacoes import services
from rasto.organizacoes.models import CRITERIOS, ESTADOS_CRITERIO, Organizacao

from . import representacoes as rep
from .permissoes import VistaPapel

E = Organizacao.Estado
FILTROS = {
    "por_decidir": [E.SUBMETIDA, E.EM_ANALISE],
    "pedido_info": [E.PEDIDO_INFO],
    "verificada": [E.VERIFICADA],
    "outras": [E.RECUSADA, E.SUSPENSA, E.EXPIRADA],
}


class Verificacoes(VistaPapel):
    """D-01: por estado, ordenadas pelo prazo indicativo mais próximo."""

    papeis = ("admin",)

    def get(self, request):
        filtro = request.query_params.get("estado", "por_decidir")
        orgs = Organizacao.objects.filter(estado_verificacao__in=FILTROS.get(filtro, FILTROS["por_decidir"]))
        q = request.query_params.get("q", "").strip()
        if q:
            orgs = orgs.filter(Q(nome_legal__icontains=q) | Q(nif__icontains=q) | Q(nome_publico__icontains=q))
        orgs = orgs.order_by("prazo_resposta", "submetida_em")
        return Response({"filtro": filtro,
                         "contagens": {k: Organizacao.objects.filter(estado_verificacao__in=v).count()
                                       for k, v in FILTROS.items()},
                         "organizacoes": [rep.organizacao(o, completa=True) for o in orgs]})


class Verificacao(VistaPapel):
    """D-02: abrir o processo (passa a «em análise») e ver critérios, comprovativos e registo."""

    papeis = ("admin",)

    def get(self, request, pk):
        org = obter_no_ambito_ou_404(Organizacao.objects.all(), pk=pk)
        return Response(self._dados(org))

    def _dados(self, org):
        ultima = org.verificacoes.exclude(criterios={}).first()
        return {"organizacao": rep.organizacao(org, completa=True),
                "criterios": [{"chave": c, "rotulo": r, "ajuda": a,
                               "avaliacao": (ultima.criterios.get(c) if ultima else None)} for c, r, a in CRITERIOS],
                "estados_criterio": [{"valor": v, "rotulo": r} for v, r in ESTADOS_CRITERIO],
                "comprovativos": [rep.comprovativo(c) for c in org.comprovativos.all()],
                "historico": [{"decisao": v.decisao, "rotulo": v.get_decisao_display(), "motivo": v.motivo,
                               "criterios": v.criterios, "criado_em": v.criado_em,
                               "decidido_por": str(v.decidido_por) if v.decidido_por else None}
                              for v in org.verificacoes.select_related("decidido_por")]}


class AbrirVerificacao(Verificacao):
    def post(self, request, pk):
        org = obter_no_ambito_ou_404(Organizacao.objects.all(), pk=pk)
        services.abrir_processo(admin=request.user, organizacao=org)
        org.refresh_from_db()
        return Response(self._dados(org))


class CriterioIn(serializers.Serializer):
    estado = serializers.ChoiceField(choices=[v for v, _ in ESTADOS_CRITERIO], required=False, allow_blank=True)
    nota = serializers.CharField(max_length=500, required=False, allow_blank=True, default="")


class DecisaoIn(serializers.Serializer):
    decisao = serializers.ChoiceField(choices=["verificar", "pedir_info", "recusar", "suspender", "reactivar"])
    criterios = serializers.DictField(child=CriterioIn(), required=False, default=dict)
    motivo = serializers.CharField(max_length=500, required=False, allow_blank=True, default="")


class DecidirVerificacao(Verificacao):
    def post(self, request, pk):
        org = obter_no_ambito_ou_404(Organizacao.objects.all(), pk=pk)
        s = DecisaoIn(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        services.decidir_verificacao(admin=request.user, organizacao=org, decisao=d["decisao"],
                                     criterios=d["criterios"], motivo=d["motivo"], request=request)
        org.refresh_from_db()
        return Response(self._dados(org))
