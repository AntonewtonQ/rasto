"""Formatos locais (especificação de interface, secção 5): Kz antes do valor, espaço fino como separador de
milhares, vírgula decimal, datas dd/mm/aaaa e meses por extenso com maiúscula."""

from datetime import date, datetime

from django.utils import timezone

SEP = " "  # espaço fino inquebrável
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro",
         "Outubro", "Novembro", "Dezembro"]
MESES_ABREV = ["Jan.", "Fev.", "Mar.", "Abr.", "Maio", "Jun.", "Jul.", "Ago.", "Set.", "Out.", "Nov.", "Dez."]
MOEDAS = {"AOA": "Kz", "USD": "USD"}


def fmt_int(n: int | float) -> str:
    s = str(abs(round(n)))
    grupos = []
    while len(s) > 3:
        grupos.insert(0, s[-3:])
        s = s[:-3]
    grupos.insert(0, s)
    return ("-" if n < 0 else "") + SEP.join(grupos)


def fmt_dinheiro(valor: int, moeda: str) -> str:
    return f"{MOEDAS.get(moeda, moeda)} {fmt_int(valor)}"


def fmt_pct(x: float, casas: int = 1) -> str:
    if float(x).is_integer():
        return f"{int(x)}%"
    return f"{x:.{casas}f}".replace(".", ",") + "%"


def _data(d: date | datetime) -> date:
    if isinstance(d, datetime):
        return timezone.localtime(d).date() if timezone.is_aware(d) else d.date()
    return d


def fmt_data(d: date | datetime | None) -> str:
    if d is None:
        return ""
    d = _data(d)
    return f"{d.day:02d}/{d.month:02d}/{d.year}"


def fmt_data_extenso(d: date | datetime | None) -> str:
    if d is None:
        return ""
    d = _data(d)
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def fmt_periodo(inicio: date, fim: date) -> str:
    """'Mar.–Jun. 2026' ou 'Nov. 2025–Fev. 2026'."""
    a, b = MESES_ABREV[inicio.month - 1], MESES_ABREV[fim.month - 1]
    if inicio.year == fim.year:
        if inicio.month == fim.month:
            return f"{a} {inicio.year}"
        return f"{a}–{b} {fim.year}"
    return f"{a} {inicio.year}–{b} {fim.year}"
