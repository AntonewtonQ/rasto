from django.contrib.auth import login
from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response

from rasto.nucleo.erros import ErroDominio
from rasto.nucleo.politicas import obter_no_ambito_ou_404
from rasto.sinais.models import Sinal
from rasto.startups import services as st_services
from rasto.startups.models import MembroStartup, startup_do_utilizador

from . import representacoes as rep
from .permissoes import VistaPapel, VistaPublica
from .vistas_conta import BACKEND, validar_palavra_passe


class InicioStartup(VistaPapel):
    """S-01 (mínimo do Sprint 1): perfil, sinais (incluindo os pendentes, que só a startup vê) e passos."""

    papeis = ("startup",)

    def get(self, request):
        s = startup_do_utilizador(request.user)
        if s is None:
            raise Http404
        sinais = list(Sinal.objects.filter(startup=s).select_related("validador", "turma", "validado_por", "startup"))
        tem_validado = any(x.estado == "validado" for x in sinais)
        pediu = any(x.estado in ("pendente", "validado") for x in sinais)
        equipa = s.membros.count() > 1 or s.convites_equipa.filter(estado="pendente").exists()
        return Response({
            "startup": {"id": str(s.id), "nome": s.nome, "estado": s.estado},
            "completude": 10 if tem_validado else 0,
            "sinais": [rep.sinal(x, para_startup=True) for x in sinais],
            "passos": [
                {"texto": "Conta da startup criada", "feito": True},
                {"texto": "Convidar a equipa", "feito": equipa, "href": "/s/equipa"},
                {"texto": "Pedir o selo à sua aceleradora", "feito": pediu, "href": "/s/selos"},
                {"texto": "Selo confirmado pela aceleradora", "feito": tem_validado, "selo": tem_validado},
                {"texto": "Perfil mínimo: sector, fase, cidade, resumo e ronda", "feito": False},
            ],
        })


# --- Registo, equipa e pedido do selo -------------------------------------------------------------------------------

def _startup(request):
    s = startup_do_utilizador(request.user)
    if s is None:
        raise Http404
    return s


class RegistoStartupIn(serializers.Serializer):
    nome = serializers.CharField(max_length=120)
    nome_startup = serializers.CharField(max_length=120)
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


class RegistoStartup(VistaPublica):
    """A startup cria a sua conta e entra."""

    def post(self, request):
        s = RegistoStartupIn(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        u, startup = st_services.registar_startup(email=d["email"], palavra_passe=d["palavra_passe"], nome=d["nome"],
                                                  nome_startup=d["nome_startup"], request=request)
        login(request, u, backend=BACKEND)
        return Response({"utilizador": rep.utilizador(u), "startup": {"id": str(startup.id), "nome": startup.nome}}, status=201)


class Selos(VistaPapel):
    """Sinais de participação da startup (pedidos e confirmados) e turmas a que pode pedir o selo."""

    papeis = ("startup",)

    def get(self, request):
        s = _startup(request)
        sinais = Sinal.objects.filter(startup=s, tipo=Sinal.Tipo.PARTICIPACAO).select_related("validador", "turma", "validado_por", "startup")
        ja = {x.turma_id for x in sinais if x.estado in ("pendente", "validado", "recusado")}
        entidades: dict[str, dict] = {}
        for t in st_services.turmas_para_pedido():
            e = entidades.setdefault(str(t.organizacao_id), {"id": str(t.organizacao_id), "nome": t.organizacao.nome,
                                                             "tipo_rotulo": t.organizacao.get_tipo_display(), "turmas": []})
            e["turmas"].append({**rep.turma(t), "ja_pedido": t.id in ja})
        return Response({"sinais": [rep.sinal(x, para_startup=True) | {"nota": x.evidencia} for x in sinais],
                         "entidades": list(entidades.values())})

    def post(self, request):
        turma = obter_no_ambito_ou_404(st_services.turmas_para_pedido(), pk=request.data.get("turma"))
        sinal = st_services.pedir_selo(utilizador=request.user, startup=_startup(request), turma=turma,
                                       nota=str(request.data.get("nota", "")), request=request)
        return Response(rep.sinal(sinal, para_startup=True), status=201)


class CancelarSelo(VistaPapel):
    papeis = ("startup",)

    def delete(self, request, pk):
        s = _startup(request)
        sinal = obter_no_ambito_ou_404(Sinal.objects.filter(startup=s), pk=pk)
        st_services.cancelar_pedido_selo(utilizador=request.user, sinal=sinal)
        return Response(status=204)


class EquipaStartup(VistaPapel):
    papeis = ("startup",)

    def get(self, request):
        s = _startup(request)
        sou_fundador = MembroStartup.objects.filter(utilizador=request.user, startup=s, funcao="fundador").exists()
        return Response({
            "startup": {"id": str(s.id), "nome": s.nome}, "sou_fundador": sou_fundador,
            "membros": [{"id": m.id, "nome": m.utilizador.nome, "email": m.utilizador.email, "funcao": m.funcao,
                         "funcao_rotulo": m.get_funcao_display(), "eu": m.utilizador_id == request.user.id}
                        for m in s.membros.select_related("utilizador").order_by("funcao", "utilizador__nome")],
            "convites": [{"id": str(c.id), "email": c.email, "expira_em": c.expira_em}
                         for c in s.convites_equipa.filter(estado="pendente")],
        })

    def post(self, request):
        email = str(request.data.get("email", "")).strip()
        if not email:
            raise ErroDominio("Indique o e-mail do colega.")
        c, _token = st_services.convidar_membro(utilizador=request.user, startup=_startup(request), email=email)
        return Response({"id": str(c.id), "email": c.email, "expira_em": c.expira_em}, status=201)


class CancelarConviteEquipaStartup(VistaPapel):
    papeis = ("startup",)

    def post(self, request, pk):
        c = obter_no_ambito_ou_404(_startup(request).convites_equipa.all(), pk=pk)
        st_services.cancelar_convite_membro(utilizador=request.user, convite=c)
        return Response(status=204)


class MembroEquipaStartup(VistaPapel):
    papeis = ("startup",)

    def delete(self, request, pk):
        s = _startup(request)
        m = obter_no_ambito_ou_404(s.membros.select_related("utilizador"), pk=pk)
        st_services.retirar_membro(utilizador=request.user, startup=s, membro=m)
        return Response(status=204)
