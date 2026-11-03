from datetime import date

from rasto.nucleo.formatos import SEP, fmt_data, fmt_data_extenso, fmt_dinheiro, fmt_int, fmt_pct, fmt_periodo


def test_milhares_com_espaco_fino_tambem_com_4_digitos():
    assert fmt_int(1850) == f"1{SEP}850"
    assert fmt_int(45000000) == f"45{SEP}000{SEP}000"
    assert fmt_int(999) == "999"


def test_moeda_antes_do_valor():
    assert fmt_dinheiro(45000000, "AOA") == f"Kz 45{SEP}000{SEP}000"
    assert fmt_dinheiro(80000, "USD") == f"USD 80{SEP}000"


def test_percentagens_e_datas():
    assert fmt_pct(37.5) == "37,5%" and fmt_pct(35.0) == "35%"
    assert fmt_data(date(2026, 7, 2)) == "02/07/2026"
    assert fmt_data_extenso(date(2026, 7, 12)) == "12 de Julho de 2026"
    assert fmt_periodo(date(2026, 3, 2), date(2026, 6, 26)) == "Mar.–Jun. 2026"
    assert fmt_periodo(date(2025, 11, 1), date(2026, 2, 1)) == "Nov. 2025–Fev. 2026"
