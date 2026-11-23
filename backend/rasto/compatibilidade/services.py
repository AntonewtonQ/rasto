"""Ligação entre os dados (Django) e a função pura `dominio.pontuar` (base técnica 5)."""

from dataclasses import dataclass
from decimal import Decimal

from rasto.catalogo.models import taxa_actual
from rasto.investidores.models import Mandato
from rasto.nucleo.formatos import fmt_dinheiro
from rasto.startups.models import Startup

from . import dominio
from .models import ConfiguracaoCompatibilidade, configuracao_activa

ROTULOS = {"sector": "Sector", "fase": "Fase", "cheque": "Valor do cheque", "geografia": "Geografia", "risco": "Risco"}


def _usd(valor: int | None, moeda: str, taxa: Decimal | None) -> int | None:
    if valor is None:
        return None
    if moeda == "USD":
        return int(valor)
    if taxa is None or taxa <= 0:
        return None  # sem taxa de referência não se compara Kz com USD
    return int(Decimal(valor) / taxa)


def configuracao_dominio(c: ConfiguracaoCompatibilidade) -> dominio.Configuracao:
    return dominio.Configuracao(versao=c.versao, peso_sector=c.peso_sector, peso_fase=c.peso_fase,
                                peso_cheque=c.peso_cheque, peso_geografia=c.peso_geografia, peso_risco=c.peso_risco,
                                parcela_minima=c.parcela_minima, limiar_compativel=c.limiar_compativel,
                                limiar_parcial=c.limiar_parcial)


def perfil_dominio(s: Startup, taxa: Decimal | None) -> dominio.PerfilStartup:
    from rasto.startups.services import ronda_aberta

    r = ronda_aberta(s)
    return dominio.PerfilStartup(sector=s.sector.codigo if s.sector else None,
                                 fase_ordem=s.fase.ordem if s.fase else None,
                                 ronda_usd=_usd(r.valor_alvo, r.moeda, taxa) if r else None,
                                 provincia=s.provincia.codigo if s.provincia else None)


def mandato_dominio(m: Mandato, taxa: Decimal | None) -> dominio.Mandato:
    return dominio.Mandato(sectores=frozenset(m.sectores.values_list("codigo", flat=True)),
                           fases_ordem=frozenset(m.fases.values_list("ordem", flat=True)),
                           cheque_min_usd=_usd(m.cheque_min, m.moeda_cheque, taxa),
                           cheque_max_usd=_usd(m.cheque_max, m.moeda_cheque, taxa),
                           geografias=frozenset(m.geografias.values_list("codigo", flat=True)))


def _frase(chave: str, c: dominio.Criterio, s: Startup, m: Mandato) -> str:
    """Explicação em linguagem simples (base técnica 5.3)."""
    from rasto.startups.services import ronda_aberta

    E = dominio.Estado
    if c.estado == E.SEM_PESO:
        return "Ainda não conta (peso 0)."
    if chave == "sector":
        return f"{s.sector.nome} está no seu mandato." if c.estado == E.TOTAL else (
            f"{s.sector.nome} não está no seu mandato." if s.sector else "A startup ainda não indicou o sector.")
    if chave == "fase":
        if c.estado == E.SEM_DADOS:
            return "A startup ainda não indicou a fase."
        return {E.TOTAL: f"{s.fase.nome} está no seu mandato.", E.PARCIAL: f"{s.fase.nome} é adjacente às fases do seu mandato.",
                E.NENHUM: f"{s.fase.nome} está fora do seu mandato."}[c.estado]
    if chave == "cheque":
        r = ronda_aberta(s)
        if c.estado == E.SEM_DADOS:
            return "A startup ainda não indicou o valor da ronda." if r is None else "Sem taxa de câmbio de referência para comparar Kz e USD."
        if c.estado == E.SEM_RESTRICAO:
            return "Não indicou limite de cheque: conta como encaixe total."
        ronda = fmt_dinheiro(r.valor_alvo, r.moeda)
        limites = " a ".join(fmt_dinheiro(v, m.moeda_cheque) for v in (m.cheque_min, m.cheque_max) if v is not None)
        return {E.TOTAL: f"A ronda pede {ronda}; o seu cheque cobre a parcela típica.",
                E.PARCIAL: f"A ronda pede {ronda}; o seu cheque vai de {limites}. Pode participar em parte.",
                E.NENHUM: f"O seu cheque ({limites}) não se sobrepõe à ronda de {ronda}."}[c.estado]
    if chave == "geografia":
        if c.estado == E.SEM_RESTRICAO:
            return "Sem preferência de geografia: conta como encaixe total."
        if c.estado == E.SEM_DADOS:
            return "A startup ainda não indicou a província."
        return f"{s.provincia.nome} está no seu mandato." if c.estado == E.TOTAL else f"{s.provincia.nome} está fora do seu mandato."
    return ""


@dataclass
class Explicacao:
    total: int
    classificacao: str
    versao: int
    criterios: list[dict]

    def como_dict(self) -> dict:
        return {"total": self.total, "classificacao": self.classificacao, "versao": self.versao, "criterios": self.criterios,
                "aviso": "Esta pontuação mede o encaixe com o seu mandato, não a qualidade da startup."}


def explicar(startup: Startup, mandato: Mandato, cfg: ConfiguracaoCompatibilidade | None = None) -> Explicacao:
    cfg = cfg or configuracao_activa()
    t = taxa_actual()
    taxa = t.aoa_por_usd if t else None
    r = dominio.pontuar(perfil_dominio(startup, taxa), mandato_dominio(mandato, taxa), configuracao_dominio(cfg))
    criterios = [{"chave": c.chave, "rotulo": ROTULOS[c.chave], "pontos": c.pontos, "peso": c.peso, "estado": c.estado.value,
                  "frase": _frase(c.chave, c, startup, mandato)} for c in r.criterios]
    return Explicacao(r.total, r.classificacao, r.versao_config, criterios)


def sugestoes(mandato: Mandato, incluir_parciais: bool = False) -> list[tuple[Startup, Explicacao]]:
    """Startups publicadas ordenadas por pontuação; empate: mais sinais validados, depois a mais recente (UI 3.4)."""
    cfg = configuracao_activa()
    resultado = []
    for s in Startup.objects.filter(estado=Startup.Estado.PUBLICADO).select_related("sector", "fase", "provincia"):
        e = explicar(s, mandato, cfg)
        if e.classificacao == "compativel" or (incluir_parciais and e.classificacao == "parcial"):
            validados = s.sinais.filter(estado="validado").count()
            resultado.append((s, e, validados))
    resultado.sort(key=lambda x: (-x[1].total, -x[2], -x[0].actualizado_em.timestamp(), x[0].nome))
    return [(s, e) for s, e, _ in resultado]
