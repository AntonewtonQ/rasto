"""Pipeline (S-08, I-06) e actualizações (S-12). A mesma vista serve os dois lados; o âmbito vem do queryset."""

from datetime import date

from django.http import Http404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.response import Response

from rasto.actualizacoes import services as act
from rasto.actualizacoes.models import Actualizacao
from rasto.nucleo.erros import ErroDominio
from rasto.nucleo.formatos import fmt_dinheiro
from rasto.nucleo.politicas import obter_no_ambito_ou_404
from rasto.pipeline import services as pl
from rasto.pipeline.models import ETAPAS, MOTIVOS_PERDA, NOME_ETAPA
from rasto.startups.models import startup_do_utilizador

from .permissoes import VistaPapel


def _relacao(r, detalhe: bool = False) -> dict:
    if r.lado == "startup":
        if r.investidor_id:
            u = r.investidor.utilizador
            nome, sub = u.nome or u.email, " · ".join(x for x in (r.investidor.get_tipo_display(), r.investidor.organizacao) if x)
        else:
            nome, sub = r.contacto_externo, "Fora da plataforma"
    else:
        nome, sub = r.startup.nome, " · ".join(x for x in (r.startup.sector.nome if r.startup.sector else "",
                                                           r.startup.fase.nome if r.startup.fase else "") if x)
    d = {"id": str(r.id), "lado": r.lado, "nome": nome, "sub": sub, "externa": r.externa, "etapa": r.etapa,
         "etapa_nome": NOME_ETAPA[r.etapa], "valor": r.valor_indicativo, "moeda": r.moeda,
         "valor_texto": fmt_dinheiro(r.valor_indicativo, r.moeda) if r.valor_indicativo else None,
         "perdida": bool(r.perdida_em), "perdida_em": r.perdida_em, "motivo_perda": dict(MOTIVOS_PERDA[r.lado]).get(r.motivo_perda),
         "nota_perda": r.nota_perda_privada, "ultima_actividade": pl.ultima_actividade(r), "parada": pl.esta_parada(r),
         "adiado_ate": r.lembrete_adiado_ate if r.lembrete_adiado_ate and r.lembrete_adiado_ate > timezone.now() else None,
         "versao": r.versao, "startup_id": str(r.startup_id)}
    if detalhe:
        d["movimentos"] = [{"de": NOME_ETAPA.get(m.etapa_de), "para": NOME_ETAPA[m.etapa_para], "em": m.criado_em,
                            "autor": (m.autor.nome or m.autor.email) if m.autor else None}
                           for m in r.movimentos.select_related("autor").order_by("-criado_em")]
        d["interaccoes"] = [{"id": i.id, "tipo": i.tipo, "tipo_rotulo": i.get_tipo_display(), "texto": i.texto,
                             "em": i.ocorreu_em, "autor": (i.autor.nome or i.autor.email) if i.autor else None}
                            for i in r.interaccoes.select_related("autor")]
    return d


def _qs(request):
    return pl.relacoes_do_utilizador(request.user).select_related(
        "investidor__utilizador", "startup__sector", "startup__fase")


def _quadro(request, lado: str) -> dict:
    rel = list(pl.com_actividade(_qs(request)))
    d = {"etapas": [{"n": n, "codigo": c, "nome": nome} for n, c, nome in ETAPAS],
         "motivos": [{"valor": v, "rotulo": r} for v, r in MOTIVOS_PERDA[lado]],
         "relacoes": [_relacao(r) for r in rel]}
    if lado == "startup":
        s = startup_do_utilizador(request.user)
        if s is None:
            raise Http404
        d["indicadores"] = pl.indicadores(s)
        d["pedidos_pendentes"] = s.pedidos_acesso.filter(estado="pendente").count()
    return d


class PipelineStartup(VistaPapel):
    papeis = ("startup",)

    def get(self, request):
        return Response(_quadro(request, "startup"))

    def post(self, request):
        s = startup_do_utilizador(request.user)
        if s is None:
            raise Http404
        r = pl.adicionar_externo(utilizador=request.user, startup=s, nome=str(request.data.get("nome", "")),
                                 organizacao=str(request.data.get("organizacao", "")))
        return Response(_relacao(r), status=201)


class PipelineInvestidor(VistaPapel):
    papeis = ("investidor",)

    def get(self, request):
        return Response(_quadro(request, "investidor"))


class Relacao(VistaPapel):
    papeis = ("startup", "investidor")

    def get(self, request, pk):
        return Response(_relacao(obter_no_ambito_ou_404(_qs(request), pk=pk), detalhe=True))


class MoverIn(serializers.Serializer):
    etapa = serializers.IntegerField(min_value=1, max_value=7)
    versao = serializers.IntegerField(required=False, allow_null=True)
    valor = serializers.IntegerField(required=False, allow_null=True, min_value=1)
    moeda = serializers.ChoiceField(choices=["AOA", "USD"], required=False, allow_null=True)


class AccaoRelacao(VistaPapel):
    papeis = ("startup", "investidor")

    def post(self, request, pk, accao):
        r = obter_no_ambito_ou_404(_qs(request), pk=pk)
        u, d = request.user, request.data
        if accao == "mover":
            s = MoverIn(data=d)
            s.is_valid(raise_exception=True)
            r = pl.mover(utilizador=u, relacao=r, **s.validated_data)
        elif accao == "perder":
            r = pl.marcar_perdida(utilizador=u, relacao=r, motivo=str(d.get("motivo", "")), nota=str(d.get("nota", "")),
                                  versao=d.get("versao"))
        elif accao == "desfazer-perda":
            r = pl.desfazer_perda(utilizador=u, relacao=r)
        elif accao == "adiar":
            r = pl.adiar_lembrete(utilizador=u, relacao=r)
        elif accao == "interaccoes":
            quando = serializers.DateTimeField(required=False, allow_null=True).to_internal_value(d["ocorreu_em"]) \
                if d.get("ocorreu_em") else None
            pl.registar_interaccao(utilizador=u, relacao=r, tipo=str(d.get("tipo", "")), texto=str(d.get("texto", "")),
                                   ocorreu_em=quando)
        else:
            raise Http404
        return Response(_relacao(_qs(request).get(pk=r.pk), detalhe=True))


# --- Actualizações ---------------------------------------------------------------------------------------------------

def actualizacao(a: Actualizacao, com_falhas: bool = False) -> dict:
    d = {"id": str(a.id), "periodo": a.periodo, "mes": act.nome_mes(a.periodo), "estado": a.estado,
         "metricas": act.metricas_legiveis(a), "destaques": a.destaques, "pedidos_ajuda": a.pedidos_ajuda,
         "corrige": {"id": str(a.corrige_id), "mes": act.nome_mes(a.corrige.periodo)} if a.corrige_id else None,
         "publicada_em": a.publicada_em}
    if com_falhas:
        d["falhas_envio"] = act.falhas_envio(a)
    return d


class ActualizacaoIn(serializers.Serializer):
    periodo = serializers.DateField(input_formats=["%Y-%m-%d", "%Y-%m"])
    metricas = serializers.DictField(child=serializers.CharField(allow_blank=True, allow_null=True), default=dict)
    destaques = serializers.CharField(max_length=600, allow_blank=True, default="")
    pedidos_ajuda = serializers.CharField(max_length=300, allow_blank=True, default="")
    corrige = serializers.UUIDField(required=False, allow_null=True)


class Actualizacoes(VistaPapel):
    papeis = ("startup",)

    def _s(self, request):
        s = startup_do_utilizador(request.user)
        if s is None:
            raise Http404
        return s

    def get(self, request):
        s = self._s(request)
        rascunho = s.actualizacoes.filter(estado="rascunho").first()
        hoje = timezone.localdate()
        return Response({
            "publicadas": [actualizacao(a, com_falhas=True) for a in act.visiveis_para_investidor(s).select_related("corrige")],
            "rascunho": actualizacao(rascunho) | {"metricas_brutas": rascunho.metricas} if rascunho else None,
            "modelo": act.modelo(s), "destinatarios": len(act.destinatarios(s)),
            "periodo_sugerido": act.mes_anterior(hoje) if not s.actualizacoes.filter(
                estado="publicada", periodo=act.mes_anterior(hoje)).exists() else date(hoje.year, hoje.month, 1),
            "perfil_publicado": s.estado == "publicado"})

    def put(self, request):
        p = ActualizacaoIn(data=request.data)
        p.is_valid(raise_exception=True)
        s = self._s(request)
        v = p.validated_data
        corrige = obter_no_ambito_ou_404(s.actualizacoes.all(), pk=v["corrige"]) if v.get("corrige") else None
        a = act.guardar_rascunho(utilizador=request.user, startup=s, periodo=v["periodo"], metricas=v["metricas"],
                                 destaques=v["destaques"], pedidos_ajuda=v["pedidos_ajuda"], corrige=corrige)
        return Response(actualizacao(a))

    def post(self, request):
        """Publica o rascunho."""
        s = self._s(request)
        a = s.actualizacoes.filter(estado="rascunho").first()
        if a is None:
            raise ErroDominio("Não há rascunho para publicar.")
        return Response(actualizacao(act.publicar(utilizador=request.user, actualizacao=a, request=request)), status=201)
