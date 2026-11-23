from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework.response import Response

from rasto.acessos import services as acessos
from rasto.acessos.models import PedidoAcesso
from rasto.catalogo.models import ItemCatalogo, taxa_actual
from rasto.compatibilidade.services import explicar, sugestoes
from rasto.investidores import services as inv_services
from rasto.nucleo.politicas import obter_no_ambito_ou_404
from rasto.startups.models import Startup

from . import representacoes as rep
from .permissoes import VistaPapel, VistaPublica
from .vistas_conta import BACKEND, validar_palavra_passe


def _investidor(request):
    inv = inv_services.investidor_do_utilizador(request.user)
    if inv is None:
        raise Http404
    return inv


class Catalogo(VistaPapel):
    """Listas configuráveis (sectores, fases, geografias, riscos) e a taxa de referência em vigor."""

    papeis = ("startup", "investidor", "entidade", "admin")

    def get(self, request):
        dados = {t: [] for t, _ in ItemCatalogo.Tipo.choices}
        for i in ItemCatalogo.objects.filter(activo=True):
            dados[i.tipo].append({"id": str(i.id), "codigo": i.codigo, "nome": i.nome, "descricao": i.descricao})
        t = taxa_actual()
        dados["taxa"] = {"data": t.data, "aoa_por_usd": str(t.aoa_por_usd)} if t else None
        return Response(dados)


class RegistoInvestidorIn(serializers.Serializer):
    nome = serializers.CharField(max_length=120)
    tipo = serializers.ChoiceField(choices=["anjo", "fundo", "corporate"])
    organizacao = serializers.CharField(max_length=160, required=False, allow_blank=True, default="")
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


class RegistoInvestidor(VistaPublica):
    def post(self, request):
        s = RegistoInvestidorIn(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        u, _inv = inv_services.registar_investidor(email=d["email"], palavra_passe=d["palavra_passe"], nome=d["nome"],
                                                   tipo=d["tipo"], organizacao=d["organizacao"], request=request)
        login(request, u, backend=BACKEND)
        return Response({"utilizador": rep.utilizador(u)}, status=201)


def _mandato(m) -> dict:
    return {"sectores": [str(i.id) for i in m.sectores.all()], "fases": [str(i.id) for i in m.fases.all()],
            "geografias": [str(i.id) for i in m.geografias.all()], "risco": str(m.risco_id) if m.risco_id else None,
            "cheque_min": m.cheque_min, "cheque_max": m.cheque_max, "moeda_cheque": m.moeda_cheque,
            "minimo_completo": m.minimo_completo, "actualizado_em": m.actualizado_em}


class MandatoIn(serializers.Serializer):
    sectores = serializers.ListField(child=serializers.UUIDField(), default=list)
    fases = serializers.ListField(child=serializers.UUIDField(), default=list)
    geografias = serializers.ListField(child=serializers.UUIDField(), default=list)
    risco = serializers.UUIDField(required=False, allow_null=True, default=None)
    cheque_min = serializers.IntegerField(required=False, allow_null=True, min_value=0, default=None)
    cheque_max = serializers.IntegerField(required=False, allow_null=True, min_value=0, default=None)
    moeda_cheque = serializers.ChoiceField(choices=["AOA", "USD"], default="USD")


class Mandato(VistaPapel):
    papeis = ("investidor",)

    def get(self, request):
        inv = _investidor(request)
        compat = len(sugestoes(inv.mandato)) if inv.mandato.minimo_completo else 0
        return Response({"mandato": _mandato(inv.mandato), "compativeis": compat,
                         "publicadas": Startup.objects.filter(estado="publicado").count()})

    def put(self, request):
        s = MandatoIn(data=request.data)
        s.is_valid(raise_exception=True)
        m = inv_services.guardar_mandato(utilizador=request.user, **s.validated_data)
        return Response({"mandato": _mandato(m), "compativeis": len(sugestoes(m)) if m.minimo_completo else 0,
                         "publicadas": Startup.objects.filter(estado="publicado").count()})


def _cartao(s, e, inv) -> dict:
    p = rep.perfil_startup(s, camada=1)
    return {"startup": {k: p[k] for k in ("id", "nome", "sector", "fase", "provincia", "cidade", "ronda", "verificados")},
            "compatibilidade": e.como_dict(), "tem_acesso": acessos.tem_acesso(inv, s)}


class Sugestoes(VistaPapel):
    """I-03: ordenadas pela pontuação; ?parciais=1 inclui as compatibilidades parciais (contagem honesta)."""

    papeis = ("investidor",)

    def get(self, request):
        inv = _investidor(request)
        if not inv.mandato.minimo_completo:
            return Response({"mandato_incompleto": True, "sugestoes": [], "publicadas": Startup.objects.filter(estado="publicado").count()})
        parciais = request.query_params.get("parciais") == "1"
        lista = sugestoes(inv.mandato, incluir_parciais=parciais)
        return Response({"mandato_incompleto": False, "publicadas": Startup.objects.filter(estado="publicado").count(),
                         "compativeis": sum(1 for _, e in lista if e.classificacao == "compativel"),
                         "sugestoes": [_cartao(s, e, inv) | {"posicao": i} for i, (s, e) in enumerate(lista, start=1)]})


class PerfilParaInvestidor(VistaPapel):
    """I-04: camada 1 para qualquer investidor; camada 2 com pedido aceite e não revogado."""

    papeis = ("investidor",)

    def get(self, request, pk):
        inv = _investidor(request)
        s = obter_no_ambito_ou_404(Startup.objects.filter(estado="publicado").select_related("sector", "fase", "provincia"), pk=pk)
        camada = 2 if acessos.tem_acesso(inv, s) else 1
        pedido = PedidoAcesso.objects.filter(investidor=inv, startup=s).order_by("-criado_em").first()
        return Response({"perfil": rep.perfil_startup(s, camada=camada),
                         "compatibilidade": explicar(s, inv.mandato).como_dict() if inv.mandato.minimo_completo else None,
                         "pedido": _pedido(pedido) if pedido else None,
                         "novo_pedido_a_partir_de": acessos.bloqueado_ate(inv, s)})


def _pedido(p: PedidoAcesso) -> dict:
    return {"id": str(p.id), "estado": p.estado, "estado_rotulo": p.get_estado_display(), "nota": p.nota,
            "expira_em": p.expira_em, "decidido_em": p.decidido_em, "criado_em": p.criado_em,
            "motivo": p.get_motivo_recusa_display() if p.motivo_partilhado else None,
            "novo_pedido_a_partir_de": p.novo_pedido_a_partir_de}


class PedirAcesso(VistaPapel):
    papeis = ("investidor",)

    def post(self, request, pk):
        inv = _investidor(request)
        s = obter_no_ambito_ou_404(Startup.objects.all(), pk=pk)
        posicao = request.data.get("posicao")
        p = acessos.pedir_acesso(investidor=inv, startup=s, nota=str(request.data.get("nota", "")),
                                 origem=str(request.data.get("origem", "perfil")),
                                 posicao=int(posicao) if str(posicao).isdigit() else None, request=request)
        return Response(_pedido(p), status=201)


class RetirarPedido(VistaPapel):
    papeis = ("investidor",)

    def post(self, request, pk):
        inv = _investidor(request)
        p = obter_no_ambito_ou_404(PedidoAcesso.objects.filter(investidor=inv), pk=pk)
        return Response(_pedido(acessos.retirar(investidor=inv, pedido=p)))


class MeusPedidos(VistaPapel):
    papeis = ("investidor",)

    def get(self, request):
        inv = _investidor(request)
        return Response({"pedidos": [_pedido(p) | {"startup": {"id": str(p.startup_id), "nome": p.startup.nome}}
                                     for p in PedidoAcesso.objects.filter(investidor=inv).select_related("startup")]})


class AbrirDocumento(VistaPapel):
    """Redireccionamento auditado: o investidor nunca vê o URL directo; só com acesso aceite (base técnica 7.3)."""

    papeis = ("investidor",)

    def get(self, request, pk, doc):
        inv = _investidor(request)
        s = obter_no_ambito_ou_404(Startup.objects.all(), pk=pk)
        if not acessos.tem_acesso(inv, s):
            raise Http404
        d = obter_no_ambito_ou_404(s.documentos.all(), pk=doc)
        acessos.registar_abertura_documento(investidor=inv, documento=d, request=request)
        r = redirect(d.url)
        r["Referrer-Policy"] = "no-referrer"
        return r
