from dataclasses import asdict

from django.contrib.auth import login
from rest_framework import serializers
from rest_framework.response import Response

from rasto.contas.models import Utilizador
from rasto.nucleo.erros import ErroDominio
from rasto.nucleo.politicas import obter_no_ambito_ou_404
from rasto.sinais.models import Sinal
from rasto.turmas import services
from rasto.turmas.models import Convite

from . import representacoes as rep
from .permissoes import VistaPapel, VistaPublica
from .vistas_conta import BACKEND, validar_palavra_passe
from .vistas_entidade import contagens_turma, org_de, turmas_da_entidade

FORMATOS_DATA = ["%d/%m/%Y", "%Y-%m-%d", "iso-8601"]


class TurmaIn(serializers.Serializer):
    programa = serializers.CharField(max_length=120)
    edicao = serializers.CharField(max_length=60)
    inicio = serializers.DateField(input_formats=FORMATOS_DATA)
    fim = serializers.DateField(input_formats=FORMATOS_DATA)


class Turmas(VistaPapel):
    """E-03 (lista, mais recente primeiro) e E-04 (criar)."""

    papeis = ("entidade",)

    def get(self, request):
        return Response({"turmas": [{**rep.turma(t), "contagens": contagens_turma(t)}
                                    for t in turmas_da_entidade(request.user)]})

    def post(self, request):
        s = TurmaIn(data=request.data)
        s.is_valid(raise_exception=True)
        t = services.criar_turma(utilizador=request.user, organizacao=org_de(request), **s.validated_data)
        return Response(rep.turma(t), status=201)


class Turma_(VistaPapel):
    """E-05: startups aceites (com o estado da participação) e convites."""

    papeis = ("entidade",)

    def get(self, request, pk):
        t = obter_no_ambito_ou_404(turmas_da_entidade(request.user).select_related("organizacao"), pk=pk)
        participacoes = {s.startup_id: s for s in Sinal.objects.filter(turma=t, tipo="participacao")}
        startups = []
        for st in t.startups.select_related("startup"):
            p = participacoes.get(st.startup_id)
            startups.append({"id": str(st.startup.id), "nome": st.startup.nome, "entrou_em": st.entrou_em,
                             "participacao": {"id": str(p.id), "estado": p.estado_visivel,
                                              "validado_em": p.validado_em} if p else None})
        return Response({"turma": rep.turma(t), "contagens": contagens_turma(t),
                         "pode_convidar": t.organizacao.pode_convidar_e_validar and t.estado != "encerrada",
                         "frase_exemplo": services.frase_validacao(t, "{Startup}"),
                         "startups": startups,
                         "convites": [rep.convite(c) for c in t.convites.exclude(estado="cancelado")
                                      .select_related("enviado_por")]})


class TextoIn(serializers.Serializer):
    texto = serializers.CharField(max_length=20000)


class VerificarEmails(VistaPapel):
    """E-06: validação linha a linha, sem enviar nada."""

    papeis = ("entidade",)

    def post(self, request, pk):
        t = obter_no_ambito_ou_404(turmas_da_entidade(request.user), pk=pk)
        s = TextoIn(data=request.data)
        s.is_valid(raise_exception=True)
        linhas = services.validar_lista_emails(turma=t, texto=s.validated_data["texto"])
        return Response({"linhas": [{**asdict(linha), "enviavel": linha.enviavel} for linha in linhas],
                         "enviaveis": sum(linha.enviavel for linha in linhas)})


class Convites(VistaPapel):
    """E-06: envio por e-mail. As linhas inválidas não bloqueiam as válidas."""

    papeis = ("entidade",)

    def post(self, request, pk):
        t = obter_no_ambito_ou_404(turmas_da_entidade(request.user).select_related("organizacao"), pk=pk)
        s = TextoIn(data=request.data)
        s.is_valid(raise_exception=True)
        enviados, linhas = services.enviar_convites(utilizador=request.user, turma=t, texto=s.validated_data["texto"])
        return Response({"enviados": [rep.convite(c) for c in enviados],
                         "linhas": [{**asdict(linha), "enviavel": linha.enviavel} for linha in linhas]}, status=201)


class EmailIn(serializers.Serializer):
    email = serializers.EmailField()


class ConviteLigacao(VistaPapel):
    """E-06: ligação pessoal de uso único para WhatsApp/SMS. A ligação só existe nesta resposta."""

    papeis = ("entidade",)

    def post(self, request, pk):
        t = obter_no_ambito_ou_404(turmas_da_entidade(request.user).select_related("organizacao"), pk=pk)
        s = EmailIn(data=request.data)
        s.is_valid(raise_exception=True)
        c, url, mensagem = services.gerar_ligacao_convite(utilizador=request.user, turma=t,
                                                          email=s.validated_data["email"])
        return Response({"convite": rep.convite(c), "ligacao": url, "mensagem": mensagem}, status=201)


def _convite_da_entidade(request, pk) -> Convite:
    return obter_no_ambito_ou_404(Convite.objects.filter(turma__organizacao__membros__utilizador=request.user)
                                  .select_related("turma__organizacao"), pk=pk)


class ReenviarConvite(VistaPapel):
    papeis = ("entidade",)

    def post(self, request, pk):
        c = _convite_da_entidade(request, pk)
        email = request.data.get("email") or None
        return Response(rep.convite(services.reenviar_convite(utilizador=request.user, convite=c, email=email)))


class CancelarConvite(VistaPapel):
    papeis = ("entidade",)

    def post(self, request, pk):
        c = _convite_da_entidade(request, pk)
        return Response(rep.convite(services.cancelar_convite(utilizador=request.user, convite=c)))


# --- Convite público (C-03) --------------------------------------------------------------------


class ConvitePublico(VistaPublica):
    """Estado do convite para o ecrã de aceitação: válido, expirado, já aceite, indisponível, inexistente,
    e se o e-mail já tem conta ou se a sessão é de outro papel."""

    def get(self, request, token):
        c = services.obter_convite(token)
        if c is None:
            return Response({"estado": "inexistente"}, status=404)
        t = c.turma
        d = {"estado": c.estado, "email": c.email, "expira_em": c.expira_em,
             "turma": rep.turma(t), "organizacao": rep.organizacao(t.organizacao),
             "enviado_por": (c.enviado_por.nome or c.enviado_por.email) if c.enviado_por else None,
             "conta_existe": Utilizador.objects.filter(email__iexact=c.email).exists()}
        u = request.user
        if u.is_authenticated:
            d["sessao"] = {"papel": u.papel_id, "email": u.email}
        return Response(d)


class AceitarConviteIn(serializers.Serializer):
    nome = serializers.CharField(max_length=120)
    nome_startup = serializers.CharField(max_length=120)
    palavra_passe = serializers.CharField(min_length=12, trim_whitespace=False)
    consentimento = serializers.BooleanField()

    def validate_palavra_passe(self, v):
        validar_palavra_passe(v)
        return v


class AceitarConvite(VistaPublica):
    """Sem sessão: cria a conta da startup e entra. Com sessão de startup: junta-se à turma."""

    def post(self, request, token):
        u = request.user
        if u.is_authenticated:
            st = services.aceitar_convite_conta_existente(token=token, utilizador=u)
            return Response({"startup": {"id": str(st.startup.id), "nome": st.startup.nome},
                             "turma": rep.turma(st.turma)})
        s = AceitarConviteIn(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        if not d["consentimento"]:
            raise ErroDominio("Para criar a conta, aceite o aviso de privacidade.")
        novo, st = services.aceitar_convite_nova_conta(token=token, nome=d["nome"], nome_startup=d["nome_startup"],
                                                       palavra_passe=d["palavra_passe"], consentiu=True)
        login(request, novo, backend=BACKEND)
        return Response({"utilizador": rep.utilizador(novo),
                         "startup": {"id": str(st.startup.id), "nome": st.startup.nome},
                         "turma": rep.turma(st.turma)}, status=201)


class RecusarConvite(VistaPublica):
    def post(self, request, token):
        c = services.recusar_convite(token=token)
        return Response({"estado": c.estado})
