#!/usr/bin/env python3
"""Resultados das sessões de teste para o Capítulo IV.

SUS (Brooke, 1996): itens ímpares x − 1; itens pares 5 − x; soma × 2,5. Mostra média, mínimo, máximo e n por papel,
sem conclusões estatísticas (amostras pequenas). Tarefas: taxa de sucesso sem ajuda, mediana do tempo e do SEQ.
Uso: python3 calcular.py [pasta]   (lê registo-sessoes.csv e respostas-sus.csv da pasta indicada)
"""

import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

PASTA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
ALVO_S = {"A1": 360, "A2": 120, "A3": 120, "A4": 180, "A5": 180, "A6": 120, "S1": 240, "S1b": 60}


def sus(linha: dict) -> float:
    total = 0
    for i in range(1, 11):
        x = int(linha[f"q{i}"])
        if not 1 <= x <= 5:
            raise ValueError(f"Resposta fora de 1–5 em {linha['participante']}, q{i}: {x}")
        total += (x - 1) if i % 2 else (5 - x)
    return total * 2.5


def fmt(x: float) -> str:
    return f"{x:.1f}".replace(".", ",")


def main():
    respostas = list(csv.DictReader(open(PASTA / "respostas-sus.csv", encoding="utf-8")))
    por_papel = defaultdict(list)
    for r in respostas:
        por_papel[r["papel"]].append(sus(r))
    print("SUS por papel")
    for papel, v in sorted(por_papel.items()):
        print(f"  {papel}: n = {len(v)}; média {fmt(statistics.mean(v))}; mínimo {fmt(min(v))}; máximo {fmt(max(v))}")
    if not respostas:
        print("  (sem respostas)")

    sessoes = list(csv.DictReader(open(PASTA / "registo-sessoes.csv", encoding="utf-8")))
    por_tarefa = defaultdict(list)
    for s in sessoes:
        por_tarefa[s["tarefa"]].append(s)
    print("\nTarefas")
    for t, linhas in sorted(por_tarefa.items()):
        n = len(linhas)
        sem_ajuda = sum(1 for x in linhas if x["resultado"] == "sucesso")
        tempos = [int(x["tempo_s"]) for x in linhas if x["tempo_s"]]
        seqs = [int(x["seq"]) for x in linhas if x["seq"]]
        criticos = sum(int(x["erros_criticos"] or 0) for x in linhas)
        alvo = ALVO_S.get(t)
        print(f"  {t}: n = {n}; sucesso sem ajuda {sem_ajuda}/{n} ({fmt(100 * sem_ajuda / n)}%); "
              f"mediana do tempo {statistics.median(tempos) if tempos else '—'} s (alvo {alvo or '—'} s); "
              f"mediana SEQ {statistics.median(seqs) if seqs else '—'}; erros críticos {criticos}")
    if not sessoes:
        print("  (sem registos)")


if __name__ == "__main__":
    main()
