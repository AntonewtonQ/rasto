"""Diagramas do Capítulo III (arquitectura, casos de uso, modelo de dados, estados), desenhados a partir do código.
Uso: cd docs/relatorio && .venv/bin/python figuras/diagramas.py   (gera PNG a 300 dpi em figuras/)"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch  # noqa: E402

plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 9})
AQUI = Path(__file__).parent
TINTA, CINZA, FUNDO = "#2E2A85", "#555555", "#F2F0EA"


def novo(l, a):
    fig, ax = plt.subplots(figsize=(l, a))
    ax.set_xlim(0, l * 10)
    ax.set_ylim(0, a * 10)
    ax.axis("off")
    return fig, ax


def caixa(ax, x, y, w, h, texto, cor=FUNDO, borda=TINTA, negrito=False, tam=9, tracejado=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=cor, ec=borda, lw=1,
                                ls="--" if tracejado else "-"))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=tam, weight="bold" if negrito else "normal",
            linespacing=1.3)
    return (x, y, w, h)


def seta(ax, a, b, texto="", dupla=False, cor=CINZA, curva=0.0, desloc=(0, 1.2)):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="<|-|>" if dupla else "-|>", mutation_scale=9, color=cor, lw=0.9,
                                 connectionstyle=f"arc3,rad={curva}", shrinkA=2, shrinkB=2))
    if texto:
        ax.text((a[0] + b[0]) / 2 + desloc[0], (a[1] + b[1]) / 2 + desloc[1], texto, ha="center", va="bottom",
                fontsize=7.5, color="#333333", style="italic")


def guardar(fig, nome):
    fig.savefig(AQUI / nome, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("ok", nome)


def arquitectura():
    fig, ax = novo(16, 8.6)
    caixa(ax, 2, 38, 22, 10, "Navegador\n(telemóvel ou computador)")
    caixa(ax, 36, 38, 20, 10, "Caddy\nHTTPS, mesma origem", negrito=True)
    caixa(ax, 72, 58, 30, 14, "Next.js 16 (App Router)\necrãs desenhados no servidor;\ncomponentes interactivos")
    caixa(ax, 72, 20, 30, 16, "Django 5.2 + DRF\nAPI JSON /api/v1, allauth headless,\nserviços (regras de negócio),\npermissões, auditoria")
    caixa(ax, 122, 20, 30, 16, "PostgreSQL 16\nrestrições CHECK, índices\nparciais, triggers")
    caixa(ax, 122, 58, 30, 14, "Cron (contentor)\nexpirar_pendentes · enviar_lembretes\n· enviar_emails")
    caixa(ax, 72, 0, 30, 10, "Servidor SMTP externo\n(a partir da fila EmailSaida)")
    seta(ax, (24, 43), (36, 43), "HTTPS", dupla=True)
    seta(ax, (56, 46), (72, 64), "páginas")
    seta(ax, (56, 40), (72, 28), "/api, /_allauth")
    seta(ax, (87, 58), (87, 36), "pedidos do servidor\ncom o cookie de sessão", desloc=(12, -4))
    seta(ax, (102, 28), (122, 28), "ORM", dupla=True)
    seta(ax, (137, 58), (137, 36), "comandos de\ngestão", desloc=(8, -4))
    seta(ax, (87, 20), (87, 10), "e-mails", desloc=(6, -2))
    ax.add_patch(FancyBboxPatch((32, 15), 124, 62, boxstyle="round,pad=0.5,rounding_size=2", fc="none", ec="#999999",
                                lw=0.8, ls="--"))
    ax.text(154, 74, "Docker Compose num servidor Linux", ha="right", fontsize=8, color="#666666")
    guardar(fig, "fig09_arquitectura.png")


def actor(ax, x, y, nome):
    ax.add_patch(plt.Circle((x, y + 7), 1.6, fc="white", ec="black", lw=0.9))
    ax.plot([x, x], [y + 5.4, y + 1.5], color="black", lw=0.9)
    ax.plot([x - 2.5, x + 2.5], [y + 4, y + 4], color="black", lw=0.9)
    ax.plot([x, x - 2], [y + 1.5, y - 1.5], color="black", lw=0.9)
    ax.plot([x, x + 2], [y + 1.5, y - 1.5], color="black", lw=0.9)
    ax.text(x, y - 4, nome, ha="center", va="top", fontsize=9, weight="bold")


def caso(ax, x, y, texto, w=34):
    ax.add_patch(Ellipse((x, y), w, 7.5, fc=FUNDO, ec=TINTA, lw=0.9))
    ax.text(x, y, texto, ha="center", va="center", fontsize=8)
    return (x, y, w)


def liga(ax, a, c):
    x, y, w = c
    alvo = (x - w / 2 if a[0] < x else x + w / 2, y)
    ax.plot([a[0], alvo[0]], [a[1], alvo[1]], color=CINZA, lw=0.7)


def casos_de_uso():
    fig, ax = novo(16, 12)
    ax.add_patch(FancyBboxPatch((24, 2), 112, 114, boxstyle="round,pad=0.5,rounding_size=2", fc="none", ec="black", lw=0.9))
    ax.text(80, 113, "Rasto", ha="center", fontsize=10, weight="bold")
    s = [caso(ax, 50, 104, "Criar conta e convidar a equipa"), caso(ax, 50, 94, "Pedir o selo à aceleradora"),
         caso(ax, 50, 84, "Editar e publicar o perfil"), caso(ax, 50, 74, "Decidir pedido de acesso"),
         caso(ax, 50, 64, "Publicar actualização mensal")]
    comum = caso(ax, 52, 50, "Gerir o pipeline e os indicadores", w=40)
    i = [caso(ax, 50, 36, "Definir o mandato"), caso(ax, 50, 26, "Ver sugestões explicadas"),
         caso(ax, 50, 16, "Pedir acesso"), caso(ax, 50, 6, "Abrir documentos (camada 2)")]
    e = [caso(ax, 110, 104, "Registar a entidade"), caso(ax, 110, 94, "Criar turma e convidar"),
         caso(ax, 110, 84, "Validar ou recusar sinais"), caso(ax, 110, 74, "Gerir a equipa da entidade")]
    a = [caso(ax, 110, 26, "Verificar entidades"), caso(ax, 110, 16, "Configurar pesos, listas e taxa")]
    actor(ax, 10, 82, "Startup")
    actor(ax, 10, 20, "Investidor")
    actor(ax, 150, 88, "Entidade\nvalidadora")
    actor(ax, 150, 20, "Administração")
    for c in s + [comum]:
        liga(ax, (12.5, 86), c)
    for c in i + [comum]:
        liga(ax, (12.5, 24), c)
    for c in e:
        liga(ax, (147.5, 92), c)
    for c in a:
        liga(ax, (147.5, 24), c)
    guardar(fig, "fig10_casos_uso.png")


def modelo_dados():
    fig, ax = novo(16, 11.5)
    B = {}

    def ent(nome, x, y, campos, w=30):
        h = 4 + 3.1 * len(campos)
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc="white", ec=TINTA, lw=0.9))
        ax.add_patch(FancyBboxPatch((x, y + h - 4), w, 4, boxstyle="square,pad=0", fc=TINTA, ec=TINTA, lw=0.9))
        ax.text(x + w / 2, y + h - 2, nome, ha="center", va="center", color="white", fontsize=8.5, weight="bold")
        for k, c in enumerate(campos):
            ax.text(x + 1.2, y + h - 6 - 3.1 * k, c, ha="left", va="center", fontsize=7)
        B[nome] = (x, y, w, h)

    def rel(a, b, texto, lado_a="r", lado_b="l"):
        def ponto(n, lado):
            x, y, w, h = B[n]
            return {"r": (x + w, y + h / 2), "l": (x, y + h / 2), "t": (x + w / 2, y + h), "b": (x + w / 2, y)}[lado]
        p, q = ponto(a, lado_a), ponto(b, lado_b)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=CINZA, lw=0.8)
        ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.8, texto, ha="center", va="bottom", fontsize=6.5, color="#333333")

    ent("Utilizador", 2, 94, ["email, nome", "papel", "palavra-passe (Argon2)"])
    ent("Organizacao", 44, 92, ["nome_legal, nif, tipo", "estado_verificacao", "verificada_em"])
    ent("Turma", 86, 94, ["programa, edicao", "inicio, fim, estado"])
    ent("Convite", 128, 94, ["email, canal, estado", "token (hash), expira_em"])
    ent("Startup", 44, 60, ["nome, estado", "sector, fase, provincia", "resumo, contacto_fundador"])
    ent("Sinal", 128, 62, ["tipo, estado", "frase_validada", "validador, validado_em"])
    ent("Ronda", 2, 62, ["valor_alvo, moeda", "data_inicio, estado"])
    ent("DocumentoLigacao", 2, 44, ["titulo, url (https)"])
    ent("Actualizacao", 86, 42, ["periodo, metricas", "estado, corrige"])
    ent("Investidor", 2, 14, ["tipo, organizacao", "estado_conta"])
    ent("Mandato", 2, 0, ["sectores, fases, geografias", "cheque_min/max, moeda"])
    ent("PedidoAcesso", 44, 22, ["nota, estado, expira_em", "pontuacao, decomposicao", "config_versao"])
    ent("Relacao", 86, 22, ["lado, etapa (1-7)", "valor_indicativo, moeda", "perdida_em, versao"])
    ent("MovimentoEtapa", 128, 32, ["etapa_de, etapa_para"])
    ent("Interaccao", 128, 16, ["tipo, texto, ocorreu_em"])
    ent("RegistoAuditoria", 86, 0, ["actor, accao, objecto", "hash_anterior, hash"], w=34)
    ent("ItemCatalogo", 44, 2, ["tipo, codigo, nome", "activo"])

    rel("Utilizador", "Organizacao", "membro N:1")
    rel("Organizacao", "Turma", "1:N")
    rel("Turma", "Convite", "1:N")
    rel("Turma", "Startup", "N:M (StartupTurma)", "b", "r")
    rel("Startup", "Sinal", "1:N")
    rel("Organizacao", "Sinal", "valida 1:N", "b", "t")
    rel("Startup", "Ronda", "1:N", "l", "r")
    rel("Startup", "DocumentoLigacao", "1:N", "l", "r")
    rel("Startup", "Actualizacao", "1:N", "r", "l")
    rel("Utilizador", "Startup", "membro N:M", "b", "t")
    rel("Investidor", "Mandato", "1:1", "b", "t")
    rel("Investidor", "PedidoAcesso", "1:N", "r", "l")
    rel("Startup", "PedidoAcesso", "1:N", "b", "t")
    rel("PedidoAcesso", "Relacao", "cria 1:N")
    rel("Relacao", "MovimentoEtapa", "1:N", "r", "l")
    rel("Relacao", "Interaccao", "1:N", "r", "l")
    rel("Mandato", "ItemCatalogo", "N:M", "r", "l")
    guardar(fig, "fig11_modelo_dados.png")


def estados():
    fig, ax = novo(19, 8)

    def est(x, y, t, final=False):
        return caixa(ax, x, y, 20, 6, t, cor="white" if not final else FUNDO, tam=8.5)

    ax.text(2, 76, "a) Sinal", fontsize=10, weight="bold")
    ax.add_patch(plt.Circle((12, 62), 1.4, color="black"))
    est(2, 40, "pendente")
    est(40, 52, "validado")
    est(40, 36, "recusado", True)
    est(40, 20, "expirado", True)
    est(78, 52, "retirado", True)
    seta(ax, (12, 60.5), (12, 46.5), "")
    ax.text(14, 52, "convite aceite ou\npedido de selo", fontsize=7, style="italic")
    seta(ax, (22, 45), (40, 55), "validar (entidade)", desloc=(-2, 1))
    seta(ax, (22, 43), (40, 39), "recusar com motivo", desloc=(0, 0.3))
    seta(ax, (22, 41), (40, 23), "30 dias sem resposta", desloc=(-6, -3))
    seta(ax, (60, 55), (78, 55), "retirar com motivo")

    ax.text(104, 76, "b) Pedido de acesso", fontsize=10, weight="bold")
    est(104, 48, "pendente")
    est(136, 64, "aceite")
    est(136, 48, "recusado", True)
    est(136, 32, "expirado", True)
    est(104, 24, "retirado", True)
    est(166, 64, "revogado", True)
    seta(ax, (124, 53), (136, 66), "startup aceita", desloc=(-4, 1))
    seta(ax, (124, 51), (136, 51), "recusa", desloc=(0, 0.2))
    seta(ax, (124, 49), (136, 35), "14 dias", desloc=(-2, -2))
    seta(ax, (114, 48), (114, 30), "investidor retira", desloc=(8, -2))
    seta(ax, (156, 67), (166, 67), "revoga", desloc=(0, 3.5))
    ax.text(104, 2, "Recusado e expirado: novo pedido do mesmo investidor só ao fim de 90 dias.", fontsize=7.5,
            style="italic")
    guardar(fig, "fig12_estados.png")


if __name__ == "__main__":
    arquitectura()
    casos_de_uso()
    modelo_dados()
    estados()
