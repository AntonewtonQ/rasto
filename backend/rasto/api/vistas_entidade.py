from django.db.models import Count, Q
from django.http import FileResponse, Http404
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from rasto.nucleo.erros import ErroDominio
from rasto.nucleo.politicas import obter_no_ambito_ou_404
from rasto.organizacoes import services as org_services
from rasto.organizacoes.models import Comprovativo, Organizacao
from rasto.sinais.models import Sinal
from rasto.sinais.selectors import pendentes_da_entidade
from rasto.turmas.models import Convite, Turma

from . import representacoes as rep
from .permissoes import VistaPapel

EDITAVEL = (Organizacao.Estado.RASCUNHO, Organizacao.Estado.PEDIDO_INFO, Organizacao.Estado.RECUSADA,
            Organizacao.Estado.EXPIRADA)


def org_de(request) -> Organizacao:
    org = org_services.organizacao_do_utilizador(request.user)
    if org is None:
        raise Http404
    return org


def turmas_da_entidade(utilizador):
    return Turma.objects.filter(organizacao__membros__utilizador=utilizador)


def contagens_turma(t: Turma) -> dict:
    c = t.convites.aggregate(
        total=Count("id", filter=~Q(estado=Convite.Estado.CANCELADO)),
        aceites=Count("id", filter=Q(estado=Convite.Estado.ACEITE)),
        pendentes=Count("id", filter=Q(estado=Convite.Estado.PENDENTE)),
        expirados=Count("id", filter=Q(estado=Convite.Estado.EXPIRADO)),
        erros=Count("id", filter=Q(estado=Convite.Estado.ERRO_ENVIO)),
    )
    c["validados"] = Sinal.objects.filter(turma=t, tipo="participacao", estado="validado").count()
    c["perfis_publicados"] = t.startups.filter(startup__estado="publicado").count()
    return c


class DadosEntidadeIn(serializers.Serializer):
    nome_publico = serializers.CharField(max_length=120, required=False, allow_blank=True)
    responsavel_nome = serializers.CharField(max_length=120)
    responsavel_cargo = serializers.CharField(max_length=120, required=False, allow_blank=True)
    responsavel_email = serializers.EmailField()
    descricao_programa = serializers.CharField(max_length=600)


class Entidade(VistaPapel):
    """A entidade do utilizador (dados completos para a própria)."""

    papeis = ("entidade",)

    def get(self, request):
        org = org_de(request)
        return Response({"organizacao": rep.organizacao(org, completa=True),
                         "comprovativos": [rep.comprovativo(c) for c in org.comprovativos.order_by("criado_em")]})


class Comprovativos(VistaPapel):
    """E-01, passo 2: anexar comprovativos (PDF, JPEG ou PNG até 2 MB)."""

    papeis = ("entidade",)
    parser_classes = [MultiPartParser]

    def post(self, request):
        org = org_de(request)
        ficheiro = request.FILES.get("ficheiro")
        if not ficheiro:
            raise ErroDominio("Escolha um ficheiro.")
        c = org_services.adicionar_comprovativo(utilizador=request.user, organizacao=org, ficheiro=ficheiro,
                                                descricao=request.data.get("descricao", "Comprovativo"))
        return Response(rep.comprovativo(c), status=201)


class Comprovativo_(VistaPapel):
    papeis = ("entidade",)

    def delete(self, request, pk):
        org = org_de(request)
        if org.estado_verificacao not in EDITAVEL:
            raise ErroDominio("Os comprovativos já não podem ser alterados.")
        c = obter_no_ambito_ou_404(org.comprovativos.all(), pk=pk)
        c.ficheiro.delete(save=False)
        c.delete()
        return Response(status=204)


class FicheiroComprovativo(VistaPapel):
    """Só a própria entidade e a administração; sempre como anexo."""

    papeis = ("entidade", "admin")

    def get(self, request, pk):
        if request.user.papel_id == "admin":
            qs = Comprovativo.objects.all()
        else:
            qs = Comprovativo.objects.filter(organizacao__membros__utilizador=request.user)
        c = obter_no_ambito_ou_404(qs, pk=pk)
        r = FileResponse(c.ficheiro.open("rb"), as_attachment=True, filename=c.nome_original, content_type=c.tipo_mime)
        r["X-Content-Type-Options"] = "nosniff"
        return r


class Submeter(VistaPapel):
    """E-01, passo 3: dados do responsável e do programa; submete para verificação."""

    papeis = ("entidade",)

    def post(self, request):
        org = org_de(request)
        s = DadosEntidadeIn(data=request.data)
        s.is_valid(raise_exception=True)
        org = org_services.submeter_entidade(utilizador=request.user, organizacao=org, dados=s.validated_data,
                                             request=request)
        return Response(rep.organizacao(org, completa=True))


class Painel(VistaPapel):
    """E-02: estado da verificação, turma activa, «À espera de si» ordenado pelo prazo."""

    papeis = ("entidade",)

    def get(self, request):
        org = org_de(request)
        turmas = turmas_da_entidade(request.user)
        activa = turmas.filter(estado__in=["activa", "rascunho"]).first()
        espera = []
        pendentes = list(pendentes_da_entidade(request.user)[:50])
        if pendentes:
            espera.append({"tipo": "validacoes", "quantidade": len(pendentes),
                           "startups": [s.startup.nome for s in pendentes[:3]], "prazo": pendentes[0].expira_em})
        for c in Convite.objects.filter(turma__in=turmas, estado__in=["expirado", "erro_envio"]).select_related("turma")[:10]:
            espera.append({"tipo": f"convite_{c.estado}", "email": c.email, "turma_id": str(c.turma_id),
                           "prazo": c.expira_em})
        espera.sort(key=lambda x: x["prazo"].isoformat() if x["prazo"] else "")
        return Response({
            "organizacao": rep.organizacao(org, completa=True),
            "turma_activa": {**rep.turma(activa), "contagens": contagens_turma(activa)} if activa else None,
            "turmas": [rep.turma(t) for t in turmas[:5]],
            "a_espera": espera,
        })


# --- Equipa (E-09) ---------------------------------------------------------------------------------------------


class Equipa(VistaPapel):
    """Membros da entidade e convites pendentes; o responsável convida colegas por e-mail."""

    papeis = ("entidade",)

    def get(self, request):
        from rasto.organizacoes.models import MembroOrganizacao

        org = org_de(request)
        eu_resp = MembroOrganizacao.objects.filter(utilizador=request.user, organizacao=org, funcao="responsavel").exists()
        return Response({
            "organizacao": rep.organizacao(org, completa=True),
            "sou_responsavel": eu_resp,
            "membros": [{"id": m.id, "nome": m.utilizador.nome, "email": m.utilizador.email, "funcao": m.funcao,
                         "funcao_rotulo": m.get_funcao_display(), "eu": m.utilizador_id == request.user.id}
                        for m in org.membros.select_related("utilizador").order_by("-funcao", "utilizador__nome")],
            "convites": [{"id": str(c.id), "email": c.email, "expira_em": c.expira_em, "criado_em": c.criado_em}
                         for c in org.convites_equipa.filter(estado="pendente")],
        })

    def post(self, request):
        email = str(request.data.get("email", "")).strip()
        if not email:
            raise ErroDominio("Indique o e-mail do colega.")
        c, _token = org_services.convidar_membro(utilizador=request.user, organizacao=org_de(request), email=email)
        return Response({"id": str(c.id), "email": c.email, "expira_em": c.expira_em}, status=201)


class CancelarConviteEquipa(VistaPapel):
    papeis = ("entidade",)

    def post(self, request, pk):
        org = org_de(request)
        c = obter_no_ambito_ou_404(org.convites_equipa.all(), pk=pk)
        org_services.cancelar_convite_equipa(utilizador=request.user, convite=c)
        return Response(status=204)


class MembroEquipa(VistaPapel):
    papeis = ("entidade",)

    def delete(self, request, pk):
        org = org_de(request)
        m = obter_no_ambito_ou_404(org.membros.select_related("utilizador"), pk=pk)
        org_services.retirar_membro(utilizador=request.user, organizacao=org, membro=m)
        return Response(status=204)
