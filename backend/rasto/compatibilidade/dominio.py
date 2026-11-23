"""Compatibilidade explicável (base técnica 5): função pura, sem Django. Pesos vêm da configuração activa."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum


class Estado(StrEnum):
    TOTAL = "total"
    PARCIAL = "parcial"
    NENHUM = "nenhum"
    SEM_DADOS = "sem_dados"
    SEM_RESTRICAO = "sem_restricao"
    SEM_PESO = "sem_peso"


@dataclass(frozen=True)
class Configuracao:
    versao: int
    peso_sector: int
    peso_fase: int
    peso_cheque: int
    peso_geografia: int
    peso_risco: int
    parcela_minima: Decimal = Decimal("0.10")
    limiar_compativel: int = 60
    limiar_parcial: int = 30

    def __post_init__(self) -> None:
        soma = self.peso_sector + self.peso_fase + self.peso_cheque + self.peso_geografia + self.peso_risco
        if soma != 100:
            raise ValueError(f"Os pesos têm de somar 100 (soma actual: {soma}).")
        if not (Decimal(0) <= self.parcela_minima < Decimal(1)):
            raise ValueError("A parcela mínima tem de estar em [0, 1).")


@dataclass(frozen=True)
class PerfilStartup:
    sector: str | None
    fase_ordem: int | None
    ronda_usd: int | None
    provincia: str | None


@dataclass(frozen=True)
class Mandato:
    sectores: frozenset[str]
    fases_ordem: frozenset[int]
    cheque_min_usd: int | None = None
    cheque_max_usd: int | None = None
    geografias: frozenset[str] = frozenset()  # "AO" = Angola (todas)


@dataclass(frozen=True)
class Criterio:
    chave: str
    peso: int
    fraccao: Decimal | None
    pontos: int
    estado: Estado


@dataclass(frozen=True)
class Resultado:
    total: int
    criterios: tuple[Criterio, ...]
    versao_config: int
    classificacao: str  # "compativel" | "parcial" | "fora"


def _arred(x: Decimal) -> int:
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def _sector(s: PerfilStartup, m: Mandato) -> tuple[Decimal | None, Estado]:
    if s.sector is None:
        return None, Estado.SEM_DADOS
    return (Decimal(1), Estado.TOTAL) if s.sector in m.sectores else (Decimal(0), Estado.NENHUM)


def _fase(s: PerfilStartup, m: Mandato) -> tuple[Decimal | None, Estado]:
    if s.fase_ordem is None:
        return None, Estado.SEM_DADOS
    if s.fase_ordem in m.fases_ordem:
        return Decimal(1), Estado.TOTAL
    if any(abs(s.fase_ordem - f) == 1 for f in m.fases_ordem):
        return Decimal("0.5"), Estado.PARCIAL
    return Decimal(0), Estado.NENHUM


def _cheque(s: PerfilStartup, m: Mandato, alfa: Decimal) -> tuple[Decimal | None, Estado]:
    if s.ronda_usd is None or s.ronda_usd <= 0:
        return None, Estado.SEM_DADOS
    if m.cheque_min_usd is None and m.cheque_max_usd is None:
        return Decimal(1), Estado.SEM_RESTRICAO
    p_lo, p_hi = alfa * s.ronda_usd, Decimal(s.ronda_usd)
    c_lo = Decimal(m.cheque_min_usd or 0)
    c_hi = Decimal(m.cheque_max_usd) if m.cheque_max_usd is not None else p_hi
    if p_hi == p_lo:  # alfa = 1 não é permitido; defesa extra
        return (Decimal(1), Estado.TOTAL) if c_lo <= p_hi <= c_hi else (Decimal(0), Estado.NENHUM)
    f = max(Decimal(0), min(p_hi, c_hi) - max(p_lo, c_lo)) / (p_hi - p_lo)
    if f >= 1:
        return Decimal(1), Estado.TOTAL
    return (f, Estado.PARCIAL) if f > 0 else (Decimal(0), Estado.NENHUM)


def _geografia(s: PerfilStartup, m: Mandato) -> tuple[Decimal | None, Estado]:
    if not m.geografias:
        return Decimal(1), Estado.SEM_RESTRICAO
    if s.provincia is None:
        return None, Estado.SEM_DADOS
    ok = "AO" in m.geografias or s.provincia in m.geografias
    return (Decimal(1), Estado.TOTAL) if ok else (Decimal(0), Estado.NENHUM)


def pontuar(s: PerfilStartup, m: Mandato, cfg: Configuracao) -> Resultado:
    avaliacoes = [
        ("sector", cfg.peso_sector, _sector(s, m)),
        ("fase", cfg.peso_fase, _fase(s, m)),
        ("cheque", cfg.peso_cheque, _cheque(s, m, cfg.parcela_minima)),
        ("geografia", cfg.peso_geografia, _geografia(s, m)),
        ("risco", cfg.peso_risco, (None, Estado.SEM_PESO)),  # não calculado no MVP
    ]
    criterios = []
    for chave, peso, (fraccao, estado) in avaliacoes:
        if peso == 0:
            criterios.append(Criterio(chave, 0, None, 0, Estado.SEM_PESO))
            continue
        pontos = 0 if fraccao is None else _arred(peso * fraccao)
        criterios.append(Criterio(chave, peso, fraccao, pontos, estado))
    total = sum(c.pontos for c in criterios)
    sector_ok = criterios[0].estado is Estado.TOTAL
    if sector_ok and total >= cfg.limiar_compativel:
        classe = "compativel"
    elif total >= cfg.limiar_parcial:
        classe = "parcial"
    else:
        classe = "fora"
    return Resultado(total, tuple(criterios), cfg.versao, classe)
