from django.utils import timezone
from rest_framework import serializers
from rest_framework.response import Response

from rasto.nucleo.erros import ErroDominio
from rasto.nucleo.politicas import obter_no_ambito_ou_404
from rasto.sinais import services
from rasto.sinais.selectors import pendentes_da_entidade, sinais_da_entidade

from . import representacoes as rep
from .permissoes import VistaPapel


def _com_frase(s) -> dict:
    d = rep.sinal(s)
    d["frase"] = s.frase_validada or services.frase_do_sinal(s)
    d["validavel_em_lote"] = s.tipo == "participacao"
    d["nota"] = s.evidencia
    d["pedido_pela_startup"] = not s.startup.turmas.filter(turma_id=s.turma_id).exists() if s.turma_id else False
    if s.expira_em:
        d["dias_restantes"] = (timezone.localtime(s.expira_em).date() - timezone.localdate()).days
    return d


class Validacoes(VistaPapel):
    """E-07: ?ver=pendentes (por prazo mais próximo) | ?ver=historico."""

    papeis = ("entidade",)

    def get(self, request):
        if request.query_params.get("ver") == "historico":
            qs = sinais_da_entidade(request.user).exclude(estado__in=["pendente", "declarado"]).order_by("-actualizado_em")
        else:
            qs = pendentes_da_entidade(request.user)
        return Response({"sinais": [_com_frase(s) for s in qs]})


class LoteIn(serializers.Serializer):
    sinais = serializers.ListField(child=serializers.UUIDField(), min_length=1, max_length=100)


class ValidarLote(VistaPapel):
    """Só participações entram em lote; os marcos validam-se um a um."""

    papeis = ("entidade",)

    def post(self, request):
        s = LoteIn(data=request.data)
        s.is_valid(raise_exception=True)
        ids = s.validated_data["sinais"]
        sinais = list(pendentes_da_entidade(request.user).filter(pk__in=ids))
        if len(sinais) != len(set(ids)):
            raise ErroDominio("Algum dos sinais seleccionados já não está pendente ou não é da sua entidade.")
        feitos = services.validar_em_lote(utilizador=request.user, sinais=sinais, request=request)
        return Response({"validados": [_com_frase(x) for x in feitos]})


class Validacao(VistaPapel):
    """E-08: ver a frase exacta e decidir."""

    papeis = ("entidade",)

    def get(self, request, pk):
        return Response(_com_frase(obter_no_ambito_ou_404(sinais_da_entidade(request.user), pk=pk)))


class MotivoIn(serializers.Serializer):
    motivo = serializers.CharField(max_length=300, required=False, allow_blank=True, default="")


class DecidirValidacao(VistaPapel):
    papeis = ("entidade",)
    accoes = {"validar", "recusar", "retirar"}

    def post(self, request, pk, accao):
        if accao not in self.accoes:
            raise ErroDominio("Acção desconhecida.")
        sinal = obter_no_ambito_ou_404(sinais_da_entidade(request.user), pk=pk)
        m = MotivoIn(data=request.data)
        m.is_valid(raise_exception=True)
        motivo = m.validated_data["motivo"]
        if accao == "validar":
            s = services.validar_sinal(utilizador=request.user, sinal=sinal, request=request)
        elif accao == "recusar":
            s = services.recusar_sinal(utilizador=request.user, sinal=sinal, motivo=motivo, request=request)
        else:
            s = services.retirar_validacao(utilizador=request.user, sinal=sinal, motivo=motivo, request=request)
        s.refresh_from_db()
        return Response(_com_frase(s))
