from django.conf import settings
from django.db import models

from rasto.nucleo.models import ModeloBase

# Os 4 critérios fixos da verificação (base de UX 5.2).
CRITERIOS = [
    ("existencia_legal", "Existência legal", "NIF e certidão ou registo comercial."),
    ("presenca_publica", "Presença pública", "Site ou redes sociais com actividade da entidade."),
    ("responsavel", "Responsável identificado", "Pessoa responsável com e-mail institucional."),
    ("programa_realizado", "Programa realizado", "Evidência de pelo menos um programa ou turma realizado."),
]
ESTADOS_CRITERIO = [("cumpre", "Cumpre"), ("falta", "Falta"), ("nao_cumpre", "Não cumpre")]


class Organizacao(ModeloBase):
    class Tipo(models.TextChoices):
        ACELERADORA = "aceleradora", "Aceleradora ou incubadora"
        UNIVERSIDADE = "universidade", "Universidade ou centro de empreendedorismo"
        FUNDO = "fundo", "Fundo de investimento"
        CORPORATE = "corporate", "Empresa (corporate)"

    class Estado(models.TextChoices):
        RASCUNHO = "rascunho", "Rascunho"
        SUBMETIDA = "submetida", "Submetida"
        EM_ANALISE = "em_analise", "Em análise"
        PEDIDO_INFO = "pedido_info", "Pedido de informação"
        VERIFICADA = "verificada", "Verificada"
        RECUSADA = "recusada", "Recusada"
        SUSPENSA = "suspensa", "Suspensa"
        EXPIRADA = "expirada", "Expirada"

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    nome_legal = models.CharField(max_length=160)
    nome_publico = models.CharField(max_length=120, blank=True)
    nif = models.CharField(max_length=20)
    site = models.URLField(blank=True)
    cidade = models.CharField(max_length=80, blank=True)
    descricao_programa = models.TextField(blank=True, help_text="Programas ou turmas já realizados.")
    responsavel_nome = models.CharField(max_length=120, blank=True)
    responsavel_cargo = models.CharField(max_length=120, blank=True)
    responsavel_email = models.EmailField(blank=True)
    estado_verificacao = models.CharField(max_length=20, choices=Estado.choices, default=Estado.RASCUNHO)
    passo_registo = models.PositiveSmallIntegerField(default=1)
    submetida_em = models.DateTimeField(null=True, blank=True)
    prazo_resposta = models.DateField(null=True, blank=True)
    verificada_em = models.DateTimeField(null=True, blank=True)
    verificada_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name="+")
    motivo = models.TextField(blank=True, help_text="Motivo da recusa ou suspensão, ou o que falta.")

    class Meta:
        verbose_name = "organização"
        verbose_name_plural = "organizações"

    def __str__(self) -> str:
        return self.nome

    @property
    def nome(self) -> str:
        return self.nome_publico or self.nome_legal

    @property
    def verificada(self) -> bool:
        return self.estado_verificacao == self.Estado.VERIFICADA

    @property
    def pode_convidar_e_validar(self) -> bool:
        return self.verificada


class MembroOrganizacao(models.Model):
    class Funcao(models.TextChoices):
        RESPONSAVEL = "responsavel", "Responsável"
        MEMBRO = "membro", "Membro"

    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="membros_org")
    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, related_name="membros")
    funcao = models.CharField(max_length=20, choices=Funcao.choices, default=Funcao.MEMBRO)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["utilizador", "organizacao"], name="membro_org_unico")]


class VerificacaoEntidade(ModeloBase):
    """Cada decisão da administração sobre uma entidade, com os critérios avaliados (histórico)."""

    class Decisao(models.TextChoices):
        ABERTA = "abrir", "Processo aberto"
        VERIFICAR = "verificar", "Verificada"
        PEDIR_INFO = "pedir_info", "Pedido de informação"
        RECUSAR = "recusar", "Recusada"
        SUSPENDER = "suspender", "Suspensa"
        REACTIVAR = "reactivar", "Reactivada"

    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, related_name="verificacoes")
    criterios = models.JSONField(default=dict)
    decisao = models.CharField(max_length=20, choices=Decisao.choices)
    motivo = models.TextField(blank=True)
    decidido_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")

    class Meta:
        ordering = ["-criado_em"]


def caminho_comprovativo(instancia, nome_ficheiro):
    extensao = nome_ficheiro.rsplit(".", 1)[-1].lower()[:5]
    return f"comprovativos/{instancia.organizacao_id}/{instancia.id}.{extensao}"


class Comprovativo(ModeloBase):
    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, related_name="comprovativos")
    descricao = models.CharField(max_length=120)
    ficheiro = models.FileField(upload_to=caminho_comprovativo)
    nome_original = models.CharField(max_length=200)
    tipo_mime = models.CharField(max_length=40)
    tamanho_bytes = models.PositiveIntegerField()
    sha256 = models.CharField(max_length=64)


class ConviteEquipa(ModeloBase):
    """Convite a um colega para entrar na equipa da entidade (E-09). Uso único; só o hash do token é guardado."""

    class Estado(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ACEITE = "aceite", "Aceite"
        EXPIRADO = "expirado", "Expirado"
        CANCELADO = "cancelado", "Cancelado"

    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, related_name="convites_equipa")
    email = models.EmailField()
    token_hash = models.CharField(max_length=64, unique=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDENTE)
    expira_em = models.DateTimeField()
    enviado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    aceite_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-criado_em"]
        constraints = [models.UniqueConstraint(models.functions.Lower("email"), "organizacao",
                                               condition=models.Q(estado="pendente"), name="convite_equipa_pendente_unico")]
