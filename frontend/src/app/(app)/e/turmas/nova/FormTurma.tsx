"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Campo, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtHora } from "@/lib/formatos";
import { useRascunho } from "@/lib/rascunho";
import type { Turma } from "@/lib/tipos";

const MESES = ["Jan.", "Fev.", "Mar.", "Abr.", "Maio", "Jun.", "Jul.", "Ago.", "Set.", "Out.", "Nov.", "Dez."];

function periodo(inicio: string, fim: string): string {
  const a = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(inicio), b = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(fim);
  if (!a || !b) return "{período}";
  const [ma, ya, mb, yb] = [Number(a[2]) - 1, a[3], Number(b[2]) - 1, b[3]];
  if (!MESES[ma] || !MESES[mb]) return "{período}";
  if (ya === yb) return ma === mb ? `${MESES[ma]} ${ya}` : `${MESES[ma]}–${MESES[mb]} ${yb}`;
  return `${MESES[ma]} ${ya}–${MESES[mb]} ${yb}`;
}

/** E-04: 3 campos e a frase que a entidade vai assinar, actualizada ao escrever. */
export function FormTurma({ entidade }: { entidade: string }) {
  const router = useRouter();
  const { dados: d, mudar: m, guardadoAs, limpar } = useRascunho("nova-turma", { programa: "", edicao: "", inicio: "", fim: "" });
  const [campos, setCampos] = useState<Record<string, string[]>>({});
  const [erro, setErro] = useState<string | null>(null);
  const mudar = (k: keyof typeof d) => (e: React.ChangeEvent<HTMLInputElement>) => m({ [k]: e.target.value });

  async function criar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setCampos({});
    try {
      const t = await post<Turma>("/api/v1/turmas", d);
      limpar();
      router.push(`/e/turmas/${t.id}`);
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); setCampos((e as ErroPedido).campos); }
  }

  return (
    <form className="card pad-lg pilha" onSubmit={criar} noValidate>
      <ErroTopo mensagem={erro} />
      <Campo rotulo="Programa" value={d.programa} onChange={mudar("programa")} ajuda="Ex.: Programa de Aceleração" erros={campos.programa} />
      <Campo rotulo="Edição" value={d.edicao} onChange={mudar("edicao")} ajuda="Ex.: 2026 · Turma 3" erros={campos.edicao} />
      <Campo rotulo="Início" inputMode="numeric" placeholder="dd/mm/aaaa" value={d.inicio} onChange={mudar("inicio")} ajuda="dd/mm/aaaa" erros={campos.inicio} />
      <Campo rotulo="Fim" inputMode="numeric" placeholder="dd/mm/aaaa" value={d.fim} onChange={mudar("fim")} ajuda="dd/mm/aaaa" erros={campos.fim} />
      <div className="field">
        <p className="label">É isto que vai confirmar, para cada startup, quando validar a participação:</p>
        <p className="copiavel" aria-live="polite">«{"{Startup}"} participou no {d.programa || "{Programa}"} {d.edicao || "{Edição}"} ({periodo(d.inicio, d.fim)}).»</p>
        <p className="help">Os investidores vão ler esta frase com o nome da {entidade} e a data da validação.</p>
      </div>
      {guardadoAs && <p className="help">Rascunho guardado neste aparelho às {fmtHora(guardadoAs)}.</p>}
      <div className="linha"><button className="btn btn-primary btn-lg btn-movel-cheio">Criar turma</button></div>
    </form>
  );
}
