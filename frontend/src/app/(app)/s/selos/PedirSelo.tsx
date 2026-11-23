"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { AreaTexto, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";
import type { EntidadeComTurmas } from "./page";

export function PedirSelo({ entidades }: { entidades: EntidadeComTurmas[] }) {
  const router = useRouter();
  const [entidade, setEntidade] = useState("");
  const [turma, setTurma] = useState("");
  const [nota, setNota] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const escolhida = entidades.find((e) => e.id === entidade);
  const turmaEscolhida = escolhida?.turmas.find((t) => t.id === turma);

  if (!entidades.length)
    return <p className="aviso aviso-info">Ainda não há aceleradoras verificadas com turmas na plataforma. Peça à sua aceleradora que se registe.</p>;

  async function pedir(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setOk(null);
    try {
      await post("/api/v1/startup/selos", { turma, nota });
      setOk(`Pedido enviado à ${escolhida?.nome}. Avisamos por e-mail quando responder.`);
      setTurma(""); setNota("");
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); }
  }

  return (
    <form className="pilha" onSubmit={pedir} noValidate>
      <ErroTopo mensagem={erro} />
      {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
      <div className="field">
        <label className="label" htmlFor="entidade">Aceleradora ou universidade</label>
        <select id="entidade" className="input" value={entidade} onChange={(e) => { setEntidade(e.target.value); setTurma(""); }}>
          <option value="">Escolha…</option>
          {entidades.map((e) => <option key={e.id} value={e.id}>{e.nome}</option>)}
        </select>
      </div>
      {escolhida && (
        <div className="field">
          <label className="label" htmlFor="turma">Turma em que participou</label>
          <select id="turma" className="input" value={turma} onChange={(e) => setTurma(e.target.value)}>
            <option value="">Escolha…</option>
            {escolhida.turmas.map((t) => <option key={t.id} value={t.id} disabled={t.ja_pedido}>{t.nome} · {t.periodo}{t.ja_pedido ? " (já pedido)" : ""}</option>)}
          </select>
          <p className="help">Não encontra a turma? Peça à aceleradora que a crie na plataforma.</p>
        </div>
      )}
      {turmaEscolhida && (<>
        <p className="copiavel">A aceleradora vai confirmar: «{"{"}a sua startup{"}"} participou no {turmaEscolhida.programa} {turmaEscolhida.edicao} ({turmaEscolhida.periodo}).»</p>
        <AreaTexto rotulo="Nota para a aceleradora" opcional rows={2} maxLength={300} value={nota} onChange={(e) => setNota(e.target.value)}
          ajuda="Ajuda a aceleradora a reconhecer a startup. Ex.: nome da mentora, mês do demo day." />
      </>)}
      <div><button className="btn btn-primary" disabled={!turma}>Pedir selo</button></div>
    </form>
  );
}
