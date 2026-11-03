import secrets
from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.utils import timezone

from rasto.auditoria.services import registar
from rasto.contas.models import Papel, Utilizador, registar_consentimento
from rasto.nucleo.email import enfileirar
from rasto.nucleo.erros import ErroDominio, TransicaoInvalida
from rasto.nucleo.formatos import fmt_data, fmt_data_extenso
from rasto.nucleo.parametros import prazo
from rasto.organizacoes.models import Organizacao
from rasto.sinais.models import Sinal
from rasto.startups.models import MembroStartup, Startup, startup_do_utilizador

from .models import Convite, StartupTurma, Turma, hash_token

C = Convite.Estado


def _foto(c: Convite) -> dict:
    return {"estado": c.estado, "email": c.email, "expira_em": c.expira_em}


def frase_validacao(turma: Turma, startup_nome: str) -> str:
    """Frase exacta que a entidade confirma e que o investidor vai ler (base de UX 8.1)."""
    return f"{startup_nome} participou no {turma.programa} {turma.edicao} ({turma.periodo})."


@transaction.atomic
def criar_turma(*, utilizador, organizacao: Organizacao, programa: str, edicao: str, inicio, fim) -> Turma:
    if fim < inicio:
        raise ErroDominio(f"Erro: o fim ({fmt_data(fim)}) é antes do início ({fmt_data(inicio)}).")
    estado = Turma.Estado.ACTIVA if organizacao.verificada else Turma.Estado.RASCUNHO
    t = Turma.objects.create(organizacao=organizacao, programa=programa.strip(), edicao=edicao.strip(),
                             inicio=inicio, fim=fim, estado=estado, criada_por=utilizador)
    registar(actor=utilizador, accao="turma_criada", objecto=t,
             depois={"programa": t.programa, "edicao": t.edicao, "inicio": inicio, "fim": fim, "estado": estado})
    return t


@dataclass
class LinhaConvite:
    numero: int
    email: str
    situacao: str  # "novo" | "invalido" | "startup_existente" | "ja_convidado" | "repetido" | "outro_papel"
    mensagem: str

    @property
    def enviavel(self) -> bool:
        return self.situacao in ("novo", "startup_existente")


def validar_lista_emails(*, turma: Turma, texto: str) -> list[LinhaConvite]:
    linhas, vistos = [], set()
    activos = {e.lower() for e in turma.convites.filter(estado__in=[C.PENDENTE, C.ACEITE, C.ERRO_ENVIO])
               .values_list("email", flat=True)}
    for i, bruto in enumerate(texto.replace(",", "\n").replace(";", "\n").splitlines(), start=1):
        email = bruto.strip().lower()
        if not email:
            continue
        try:
            validate_email(email)
        except ValidationError:
            linhas.append(LinhaConvite(i, email, "invalido", "Erro: formato de e-mail inválido. Não é enviado."))
            continue
        if email in vistos:
            linhas.append(LinhaConvite(i, email, "repetido", "Repetido nesta lista. É ignorado."))
            continue
        vistos.add(email)
        if email in activos:
            linhas.append(LinhaConvite(i, email, "ja_convidado", "Já convidado para esta turma. É ignorado."))
            continue
        u = Utilizador.objects.filter(email__iexact=email).first()
        if u and u.papel_id == Papel.STARTUP:
            linhas.append(LinhaConvite(i, email, "startup_existente",
                                       "Já tem conta de startup: recebe convite para se juntar à turma."))
        elif u:
            linhas.append(LinhaConvite(i, email, "outro_papel",
                                       "Este e-mail pertence a uma conta de outro papel. Use outro e-mail."))
        else:
            linhas.append(LinhaConvite(i, email, "novo", "Válido."))
    return linhas


def _exigir_turma_activa(turma: Turma):
    if not turma.organizacao.pode_convidar_e_validar:
        raise ErroDominio("Os convites ficam disponíveis depois de a entidade ser verificada pela plataforma.")
    if turma.estado == Turma.Estado.ENCERRADA:
        raise ErroDominio("Esta turma está encerrada.")


def _novo_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    return token, hash_token(token)


def url_convite(token: str) -> str:
    """Página do Next.js que mostra o convite (C-03)."""
    return f"{settings.SITE_URL}/convite/{token}/"


def _enviar_email_convite(convite: Convite, token: str):
    t = convite.turma
    enfileirar(
        para=convite.email,
        assunto=f"{t.organizacao.nome} convida a sua startup para a turma {t.programa} {t.edicao}",
        modelo="emails/convite.txt",
        contexto={"t": t, "url": url_convite(token), "validade": fmt_data_extenso(convite.expira_em),
                  "enviado_por": convite.enviado_por},
        objecto=convite,
    )


def _criar_convite(*, utilizador, turma: Turma, email: str, canal: str) -> tuple[Convite, str]:
    token, h = _novo_token()
    expira = timezone.now() + timedelta(days=prazo("convite_dias"))
    try:
        with transaction.atomic():
            c = Convite.objects.create(turma=turma, email=email.lower(), token_hash=h, canal=canal,
                                       expira_em=expira, enviado_por=utilizador)
    except IntegrityError as exc:
        raise ErroDominio(f"{email} já foi convidado para esta turma.") from exc
    registar(actor=utilizador, accao="convite_criado", objecto=c, depois={**_foto(c), "canal": canal})
    return c, token


@transaction.atomic
def enviar_convites(*, utilizador, turma: Turma, texto: str) -> tuple[list[Convite], list[LinhaConvite]]:
    _exigir_turma_activa(turma)
    linhas = validar_lista_emails(turma=turma, texto=texto)
    enviados = []
    for linha in linhas:
        if linha.enviavel:
            c, token = _criar_convite(utilizador=utilizador, turma=turma, email=linha.email, canal=Convite.Canal.EMAIL)
            _enviar_email_convite(c, token)
            enviados.append(c)
    return enviados, linhas


@transaction.atomic
def gerar_ligacao_convite(*, utilizador, turma: Turma, email: str) -> tuple[Convite, str, str]:
    """Convite por ligação pessoal de uso único, para a entidade copiar para WhatsApp ou SMS.
    Devolve o convite, a ligação e a mensagem pronta. O token só existe em claro nesta resposta."""
    _exigir_turma_activa(turma)
    linhas = validar_lista_emails(turma=turma, texto=email)
    if not linhas or not linhas[0].enviavel:
        raise ErroDominio(linhas[0].mensagem if linhas else "Indique o e-mail da startup.")
    c, token = _criar_convite(utilizador=utilizador, turma=turma, email=linhas[0].email, canal=Convite.Canal.LIGACAO)
    url = url_convite(token)
    mensagem = (f"{turma.organizacao.nome}: convidámos a vossa startup para a turma {turma.programa} {turma.edicao} "
                f"na Rasto. Aceite até {fmt_data(c.expira_em)}: {url}")
    return c, url, mensagem


@transaction.atomic
def reenviar_convite(*, utilizador, convite: Convite, email: str | None = None) -> Convite:
    """Reenvia um convite expirado ou com erro de envio (com novo token e novo prazo); permite corrigir o e-mail."""
    _exigir_turma_activa(convite.turma)
    if convite.estado not in (C.EXPIRADO, C.ERRO_ENVIO, C.PENDENTE):
        raise TransicaoInvalida("Só é possível reenviar convites pendentes, expirados ou com erro de envio.")
    antes = _foto(convite)
    if email:
        email = email.strip().lower()
        validate_email(email)
        convite.email = email
    token, convite.token_hash = _novo_token()
    convite.estado = C.PENDENTE
    convite.expira_em = timezone.now() + timedelta(days=prazo("convite_dias"))
    convite.reenvios += 1
    convite.enviado_por = utilizador
    convite.canal = Convite.Canal.EMAIL
    try:
        with transaction.atomic():
            convite.save()
    except IntegrityError as exc:
        raise ErroDominio("Já existe um convite activo para este e-mail nesta turma.") from exc
    _enviar_email_convite(convite, token)
    registar(actor=utilizador, accao="convite_reenviado", objecto=convite, antes=antes, depois=_foto(convite))
    return convite


@transaction.atomic
def cancelar_convite(*, utilizador, convite: Convite) -> Convite:
    if convite.estado not in (C.PENDENTE, C.ERRO_ENVIO, C.EXPIRADO):
        raise TransicaoInvalida("Só é possível cancelar convites que ainda não foram aceites nem recusados.")
    antes = _foto(convite)
    convite.estado = C.CANCELADO
    convite.save(update_fields=["estado", "actualizado_em"])
    registar(actor=utilizador, accao="convite_cancelado", objecto=convite, antes=antes, depois=_foto(convite))
    return convite


def obter_convite(token: str) -> Convite | None:
    c = Convite.objects.select_related("turma__organizacao", "enviado_por").filter(token_hash=hash_token(token)).first()
    if c and c.estado == C.PENDENTE and c.expira_em <= timezone.now():
        _expirar(c)
    return c


def _expirar(c: Convite):
    antes = _foto(c)
    c.estado = C.EXPIRADO
    c.save(update_fields=["estado", "actualizado_em"])
    registar(actor=None, accao="convite_expirado", objecto=c, antes=antes, depois=_foto(c))


def _exigir_aceitavel(c: Convite | None):
    if c is None:
        raise ErroDominio("Este convite não existe.")
    if c.estado == C.ACEITE:
        raise TransicaoInvalida("Este convite já foi aceite.")
    if c.estado == C.EXPIRADO or c.expira_em <= timezone.now():
        raise TransicaoInvalida(f"Este convite expirou em {fmt_data(c.expira_em)}.")
    if c.estado not in (C.PENDENTE, C.ERRO_ENVIO):
        raise TransicaoInvalida("Este convite já não está disponível.")
    if not c.turma.organizacao.pode_convidar_e_validar:
        raise TransicaoInvalida("A entidade que enviou este convite não está verificada neste momento.")


def _ligar_a_turma(*, startup: Startup, convite: Convite, actor) -> StartupTurma:
    t = convite.turma
    st, _ = StartupTurma.objects.get_or_create(startup=startup, turma=t, defaults={"convite": convite})
    sinal, criado = Sinal.objects.get_or_create(
        startup=startup, turma=t, tipo=Sinal.Tipo.PARTICIPACAO,
        defaults={"descricao": f"Participou no {t.programa} {t.edicao} ({t.periodo})", "data_facto": t.fim,
                  "validador": t.organizacao, "estado": Sinal.Estado.PENDENTE, "pedido_em": timezone.now(),
                  "expira_em": timezone.now() + timedelta(days=prazo("validacao_sinal_dias"))},
    )
    if criado:
        registar(actor=actor, accao="sinal_participacao_criado", objecto=sinal, depois={"estado": sinal.estado})
    antes = _foto(convite)
    convite.estado = C.ACEITE
    convite.aceite_em = timezone.now()
    convite.save(update_fields=["estado", "aceite_em", "actualizado_em"])
    registar(actor=actor, accao="convite_aceite", objecto=convite, antes=antes, depois=_foto(convite))
    return st


def aceitar_convite_nova_conta(*, token: str, nome: str, nome_startup: str, palavra_passe: str,
                               consentiu: bool) -> tuple[Utilizador, StartupTurma]:
    c = obter_convite(token)  # fora da transacção: uma expiração detectada aqui fica gravada
    _exigir_aceitavel(c)
    with transaction.atomic():
        return _criar_conta_e_ligar(c, nome=nome, nome_startup=nome_startup, palavra_passe=palavra_passe,
                                    consentiu=consentiu)


def _criar_conta_e_ligar(c: Convite, *, nome, nome_startup, palavra_passe, consentiu):
    c = Convite.objects.select_for_update(of=("self",)).select_related("turma__organizacao").get(pk=c.pk)
    _exigir_aceitavel(c)
    if not consentiu:
        raise ErroDominio("Para criar a conta, aceite o aviso de privacidade.")
    if Utilizador.objects.filter(email__iexact=c.email).exists():
        raise ErroDominio("Já existe uma conta com este e-mail. Entre para aceitar o convite.")
    u = Utilizador.objects.create_user(c.email, palavra_passe, nome=nome.strip(), papel_id=Papel.STARTUP)
    registar_consentimento(u)
    s = Startup.objects.create(nome=nome_startup.strip())
    MembroStartup.objects.create(utilizador=u, startup=s, funcao=MembroStartup.Funcao.FUNDADOR)
    registar(actor=u, accao="conta_startup_criada", objecto=s, depois={"nome": s.nome})
    return u, _ligar_a_turma(startup=s, convite=c, actor=u)


def aceitar_convite_conta_existente(*, token: str, utilizador) -> StartupTurma:
    c = obter_convite(token)
    _exigir_aceitavel(c)
    with transaction.atomic():
        return _juntar_conta_existente(c, utilizador)


def _juntar_conta_existente(c: Convite, utilizador) -> StartupTurma:
    c = Convite.objects.select_for_update(of=("self",)).select_related("turma__organizacao").get(pk=c.pk)
    _exigir_aceitavel(c)
    if utilizador.papel_id != Papel.STARTUP:
        raise ErroDominio("Este convite é para uma conta de startup. Saia desta conta e entre (ou crie conta) "
                          "com o e-mail do convite.")
    if utilizador.email.lower() != c.email.lower():
        raise ErroDominio(f"Este convite foi enviado para {c.email}. Entre com essa conta.")
    s = startup_do_utilizador(utilizador)
    if s is None:
        raise ErroDominio("A sua conta não está ligada a nenhuma startup.")
    return _ligar_a_turma(startup=s, convite=c, actor=utilizador)


def recusar_convite(*, token: str) -> Convite:
    c = obter_convite(token)
    _exigir_aceitavel(c)
    with transaction.atomic():
        return _recusar(c)


def _recusar(c: Convite) -> Convite:
    antes = _foto(c)
    c.estado = C.RECUSADO
    c.save(update_fields=["estado", "actualizado_em"])
    registar(actor=None, accao="convite_recusado", objecto=c, antes=antes, depois=_foto(c))
    return c


def expirar_convites() -> int:
    n = 0
    for c in Convite.objects.filter(estado=C.PENDENTE, expira_em__lte=timezone.now()):
        with transaction.atomic():
            _expirar(c)
        n += 1
    return n


def lembrar_convite(convite: Convite):
    """Lembrete ao 7.º dia (RF09, HU06). O token antigo não existe em claro, por isso:
    - convite por e-mail: gera-se uma ligação nova (a anterior deixa de valer) e envia-se ao destinatário;
    - convite por ligação (WhatsApp/SMS): avisa-se a entidade, que partilhou a ligação e a pode reenviar."""
    t = convite.turma
    if convite.canal == Convite.Canal.EMAIL:
        token, convite.token_hash = _novo_token()
        convite.save(update_fields=["token_hash"])
        enfileirar(para=convite.email,
                   assunto=f"Lembrete: {t.organizacao.nome} convida a sua startup para a turma {t.programa} {t.edicao}",
                   modelo="emails/lembrete_convite.txt",
                   contexto={"t": t, "url": url_convite(token), "validade": fmt_data_extenso(convite.expira_em)},
                   objecto=convite)
    else:
        for m in t.organizacao.membros.select_related("utilizador"):
            enfileirar(para=m.utilizador.email, assunto=f"Convite por ligação ainda por aceitar: {convite.email}",
                       modelo="emails/lembrete_convite_ligacao.txt",
                       contexto={"t": t, "c": convite, "validade": fmt_data_extenso(convite.expira_em),
                                 "site": settings.SITE_URL})
    registar(actor=None, accao="lembrete_convite", objecto=convite, depois={"canal": convite.canal})
