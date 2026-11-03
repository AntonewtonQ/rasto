import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone

from rasto.auditoria.services import registar
from rasto.contas.models import Papel, Utilizador, registar_consentimento
from rasto.nucleo.email import enfileirar
from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.parametros import prazo

from .models import (
    CRITERIOS,
    Comprovativo,
    ConviteEquipa,
    MembroOrganizacao,
    Organizacao,
    VerificacaoEntidade,
)

E = Organizacao.Estado
TIPOS_ACEITES = {b"%PDF": "application/pdf", b"\x89PNG": "image/png", b"\xff\xd8\xff": "image/jpeg"}


def _foto(org: Organizacao) -> dict:
    return {"estado": org.estado_verificacao, "motivo": org.motivo}


def organizacao_do_utilizador(utilizador) -> Organizacao | None:
    m = MembroOrganizacao.objects.select_related("organizacao").filter(utilizador=utilizador).first()
    return m.organizacao if m else None


@transaction.atomic
def registar_entidade(*, email: str, palavra_passe: str, nome: str, tipo: str, nome_legal: str, nif: str,
                      site: str = "", cidade: str = "", request=None) -> tuple[Utilizador, Organizacao]:
    """Passo 1 do registo (E-01): cria a conta da pessoa responsável e a entidade em rascunho."""
    email = email.strip().lower()
    if Utilizador.objects.filter(email__iexact=email).exists():
        raise ErroDominio("Já existe uma conta com este e-mail. Entre com essa conta ou use outro e-mail.")
    u = Utilizador.objects.create_user(email, palavra_passe, nome=nome, papel_id=Papel.ENTIDADE)
    registar_consentimento(u)
    org = Organizacao.objects.create(tipo=tipo, nome_legal=nome_legal, nif=nif, site=site, cidade=cidade,
                                     responsavel_nome=nome, responsavel_email=email, passo_registo=2)
    MembroOrganizacao.objects.create(utilizador=u, organizacao=org, funcao=MembroOrganizacao.Funcao.RESPONSAVEL)
    registar(actor=u, accao="entidade_criada", objecto=org, depois=_foto(org), request=request)
    return u, org


def _tipo_mime(conteudo: bytes) -> str | None:
    for assinatura, mime in TIPOS_ACEITES.items():
        if conteudo.startswith(assinatura):
            return mime
    return None


@transaction.atomic
def adicionar_comprovativo(*, utilizador, organizacao: Organizacao, ficheiro, descricao: str) -> Comprovativo:
    if organizacao.estado_verificacao not in (E.RASCUNHO, E.PEDIDO_INFO, E.RECUSADA, E.EXPIRADA):
        raise ErroDominio("Os comprovativos só podem ser alterados antes de submeter ou quando a plataforma pede informação.")
    if ficheiro.size > settings.COMPROVATIVO_TAMANHO_MAX:
        raise ErroDominio("Erro: o ficheiro tem mais de 2 MB. Reduza-o ou envie outro.")
    conteudo = ficheiro.read()
    mime = _tipo_mime(conteudo[:8])
    if mime is None:
        raise ErroDominio("Erro: só são aceites ficheiros PDF, JPEG ou PNG.")
    ficheiro.seek(0)
    c = Comprovativo(organizacao=organizacao, descricao=descricao[:120], nome_original=ficheiro.name[:200],
                     tipo_mime=mime, tamanho_bytes=ficheiro.size, sha256=hashlib.sha256(conteudo).hexdigest())
    c.ficheiro.save(ficheiro.name, ficheiro, save=False)
    c.save()
    registar(actor=utilizador, accao="comprovativo_enviado", objecto=organizacao,
             depois={"comprovativo": str(c.id), "sha256": c.sha256})
    return c


def dias_uteis_depois(inicio, dias: int):
    d = inicio
    while dias > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            dias -= 1
    return d


@transaction.atomic
def submeter_entidade(*, utilizador, organizacao: Organizacao, dados: dict | None = None, request=None) -> Organizacao:
    """Submete (ou volta a submeter depois de um pedido de informação) para verificação."""
    antes = _foto(organizacao)
    origem = organizacao.estado_verificacao
    if origem not in (E.RASCUNHO, E.PEDIDO_INFO, E.RECUSADA, E.EXPIRADA):
        raise TransicaoInvalida("Esta entidade já foi submetida.")
    for campo, valor in (dados or {}).items():
        setattr(organizacao, campo, valor)
    if not organizacao.comprovativos.exists():
        raise ErroDominio("Erro: anexe pelo menos um comprovativo antes de submeter.")
    if not (organizacao.responsavel_nome and organizacao.responsavel_email and organizacao.descricao_programa):
        raise ErroDominio("Erro: preencha os dados do responsável e o programa já realizado.")
    agora = timezone.now()
    organizacao.estado_verificacao = E.EM_ANALISE if origem == E.PEDIDO_INFO else E.SUBMETIDA
    organizacao.submetida_em = agora
    organizacao.prazo_resposta = dias_uteis_depois(timezone.localdate(), prazo("verificacao_indicativa_dias_uteis"))
    organizacao.passo_registo = 3
    organizacao.save()
    registar(actor=utilizador, accao="entidade_submetida", objecto=organizacao, antes=antes,
             depois=_foto(organizacao), request=request)
    for admin in Utilizador.objects.filter(papel_id=Papel.ADMIN, is_active=True):
        enfileirar(para=admin.email, assunto=f"Nova entidade para verificar: {organizacao.nome}",
                   modelo="emails/entidade_submetida.txt", contexto={"org": organizacao, "site": settings.SITE_URL})
    return organizacao


@transaction.atomic
def abrir_processo(*, admin, organizacao: Organizacao) -> Organizacao:
    if organizacao.estado_verificacao == E.SUBMETIDA:
        antes = _foto(organizacao)
        organizacao.estado_verificacao = E.EM_ANALISE
        organizacao.save(update_fields=["estado_verificacao", "actualizado_em"])
        VerificacaoEntidade.objects.create(organizacao=organizacao, decisao="abrir", decidido_por=admin)
        registar(actor=admin, accao="verificacao_aberta", objecto=organizacao, antes=antes, depois=_foto(organizacao))
    return organizacao


TRANSICOES = {
    "verificar": ({E.SUBMETIDA, E.EM_ANALISE}, E.VERIFICADA),
    "pedir_info": ({E.SUBMETIDA, E.EM_ANALISE}, E.PEDIDO_INFO),
    "recusar": ({E.SUBMETIDA, E.EM_ANALISE}, E.RECUSADA),
    "suspender": ({E.VERIFICADA}, E.SUSPENSA),
    "reactivar": ({E.SUSPENSA}, E.VERIFICADA),
}


@transaction.atomic
def decidir_verificacao(*, admin, organizacao: Organizacao, decisao: str, criterios: dict | None = None,
                        motivo: str = "", request=None) -> VerificacaoEntidade:
    if admin.papel_id != Papel.ADMIN:
        raise ErroDominio("Só a administração decide verificações.")
    if decisao not in TRANSICOES:
        raise ErroDominio("Decisão desconhecida.")
    origens, destino = TRANSICOES[decisao]
    if organizacao.estado_verificacao not in origens:
        raise TransicaoInvalida(
            f"Não é possível «{decisao}» uma entidade no estado «{organizacao.get_estado_verificacao_display()}».")
    criterios = criterios or {}
    if decisao == "verificar":
        em_falta = [rot for chave, rot, _ in CRITERIOS if criterios.get(chave, {}).get("estado") != "cumpre"]
        if em_falta:
            raise ErroDominio("Só é possível verificar com os 4 critérios em «Cumpre». Em falta: " + ", ".join(em_falta) + ".")
    if decisao in ("recusar", "suspender") and not motivo.strip():
        raise ErroDominio("Indique o motivo.")
    if decisao == "pedir_info":
        notas = [f"{rot}: {criterios.get(chave, {}).get('nota', '').strip()}" for chave, rot, _ in CRITERIOS
                 if criterios.get(chave, {}).get("estado") == "falta"]
        if not notas:
            raise ErroDominio("Para pedir informação, marque pelo menos um critério em «Falta» e diga o que falta.")
        motivo = "\n".join(notas)

    antes = _foto(organizacao)
    organizacao.estado_verificacao = destino
    organizacao.motivo = motivo
    if decisao == "verificar":
        organizacao.verificada_em = timezone.now()
        organizacao.verificada_por = admin
        organizacao.turmas.filter(estado="rascunho").update(estado="activa")
    if decisao == "pedir_info":
        organizacao.prazo_resposta = timezone.localdate() + timedelta(days=prazo("pedido_informacao_dias"))
    organizacao.save()
    v = VerificacaoEntidade.objects.create(organizacao=organizacao, criterios=criterios, decisao=decisao,
                                           motivo=motivo, decidido_por=admin)
    registar(actor=admin, accao=f"verificacao_{decisao}", objecto=organizacao, antes=antes,
             depois={**_foto(organizacao), "criterios": criterios}, request=request)
    for m in organizacao.membros.select_related("utilizador"):
        enfileirar(para=m.utilizador.email, assunto=f"Verificação da {organizacao.nome}: {v.get_decisao_display()}",
                   modelo="emails/verificacao_decidida.txt",
                   contexto={"org": organizacao, "v": v, "site": settings.SITE_URL})
    return v


@transaction.atomic
def expirar_pedidos_informacao(hoje=None) -> int:
    hoje = hoje or timezone.localdate()
    n = 0
    for org in Organizacao.objects.select_for_update().filter(estado_verificacao=E.PEDIDO_INFO, prazo_resposta__lt=hoje):
        antes = _foto(org)
        org.estado_verificacao = E.EXPIRADA
        org.save(update_fields=["estado_verificacao", "actualizado_em"])
        registar(actor=None, accao="verificacao_expirada", objecto=org, antes=antes, depois=_foto(org))
        n += 1
    return n


# --- Equipa da entidade (E-09) ------------------------------------------------------------------------------


def _exigir_responsavel(utilizador, organizacao: Organizacao):
    if not MembroOrganizacao.objects.filter(utilizador=utilizador, organizacao=organizacao,
                                            funcao=MembroOrganizacao.Funcao.RESPONSAVEL).exists():
        raise ErroDominio("Só o responsável da entidade pode gerir a equipa.")


@transaction.atomic
def convidar_membro(*, utilizador, organizacao: Organizacao, email: str) -> tuple[ConviteEquipa, str]:
    """Convida um colega por e-mail. Devolve o convite e o token em claro (só existe nesta chamada)."""

    _exigir_responsavel(utilizador, organizacao)
    email = email.strip().lower()
    validate_email(email)
    if Utilizador.objects.filter(email__iexact=email).exists():
        raise ErroDominio("Já existe uma conta com este e-mail. Cada conta tem um só papel: use outro e-mail.")
    if organizacao.convites_equipa.filter(email__iexact=email, estado=ConviteEquipa.Estado.PENDENTE).exists():
        raise ErroDominio(f"{email} já tem um convite pendente.")
    token = secrets.token_urlsafe(32)
    c = ConviteEquipa.objects.create(organizacao=organizacao, email=email, token_hash=hashlib.sha256(token.encode()).hexdigest(),
                                     expira_em=timezone.now() + timedelta(days=prazo("convite_dias")), enviado_por=utilizador)
    enfileirar(para=email, assunto=f"{utilizador.nome or utilizador.email} convidou-o para a equipa da {organizacao.nome} na Rasto",
               modelo="emails/convite_equipa.txt",
               contexto={"org": organizacao, "de": utilizador, "url": f"{settings.SITE_URL}/equipa/{token}/",
                         "validade": c.expira_em}, objecto=c)
    registar(actor=utilizador, accao="membro_convidado", objecto=organizacao, depois={"email": email})
    return c, token


def obter_convite_equipa(token: str):

    c = (ConviteEquipa.objects.select_related("organizacao", "enviado_por")
         .filter(token_hash=hashlib.sha256(token.encode()).hexdigest()).first())
    if c and c.estado == ConviteEquipa.Estado.PENDENTE and c.expira_em <= timezone.now():
        c.estado = ConviteEquipa.Estado.EXPIRADO
        c.save(update_fields=["estado", "actualizado_em"])
    return c


def aceitar_convite_equipa(*, token: str, nome: str, palavra_passe: str, consentiu: bool) -> Utilizador:

    c = obter_convite_equipa(token)  # fora da transacção: uma expiração detectada fica gravada
    if c is None:
        raise ErroDominio("Este convite não existe.")
    if c.estado != ConviteEquipa.Estado.PENDENTE:
        raise TransicaoInvalida("Este convite já não está disponível.")
    if not consentiu:
        raise ErroDominio("Para criar a conta, aceite o aviso de privacidade.")
    with transaction.atomic():
        c = ConviteEquipa.objects.select_for_update().get(pk=c.pk)
        if c.estado != ConviteEquipa.Estado.PENDENTE:
            raise TransicaoInvalida("Este convite já não está disponível.")
        u = Utilizador.objects.create_user(c.email, palavra_passe, nome=nome.strip(), papel_id=Papel.ENTIDADE)
        registar_consentimento(u)
        MembroOrganizacao.objects.create(utilizador=u, organizacao=c.organizacao, funcao=MembroOrganizacao.Funcao.MEMBRO)
        c.estado = ConviteEquipa.Estado.ACEITE
        c.aceite_em = timezone.now()
        c.save(update_fields=["estado", "aceite_em", "actualizado_em"])
        registar(actor=u, accao="membro_entrou", objecto=c.organizacao, depois={"email": u.email})
    return u


@transaction.atomic
def cancelar_convite_equipa(*, utilizador, convite) -> None:
    _exigir_responsavel(utilizador, convite.organizacao)
    if convite.estado != convite.Estado.PENDENTE:
        raise TransicaoInvalida("Só é possível cancelar convites pendentes.")
    convite.estado = convite.Estado.CANCELADO
    convite.save(update_fields=["estado", "actualizado_em"])
    registar(actor=utilizador, accao="convite_equipa_cancelado", objecto=convite.organizacao, depois={"email": convite.email})


@transaction.atomic
def retirar_membro(*, utilizador, organizacao: Organizacao, membro: MembroOrganizacao) -> None:
    """O membro deixa de ter acesso à entidade e a conta é desactivada (uma conta, um papel).
    As validações que fez mantêm o nome dele no registo de auditoria."""
    _exigir_responsavel(utilizador, organizacao)
    if membro.utilizador_id == utilizador.id:
        raise ErroDominio("Não pode retirar-se a si próprio.")
    if membro.funcao == MembroOrganizacao.Funcao.RESPONSAVEL and \
            organizacao.membros.filter(funcao=MembroOrganizacao.Funcao.RESPONSAVEL).count() <= 1:
        raise ErroDominio("A entidade tem de ter sempre um responsável.")
    u = membro.utilizador
    membro.delete()
    u.is_active = False
    u.save(update_fields=["is_active"])
    registar(actor=utilizador, accao="membro_retirado", objecto=organizacao, depois={"email": u.email})
