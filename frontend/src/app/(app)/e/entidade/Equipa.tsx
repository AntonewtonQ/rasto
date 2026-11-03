"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Campo, ErroTopo } from "@/componentes/Campo";
import { Cartao } from "@/componentes/Ui";
import { ErroPedido, pedido, post } from "@/lib/api-cliente";
import { fmtData } from "@/lib/formatos";
import type { DadosEquipa } from "./page";

export function Equipa({ dados }: { dados: DadosEquipa }) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [confirmar, setConfirmar] = useState<number | null>(null);

  async function correr(fn: () => Promise<unknown>, sucesso: string) {
    setErro(null); setOk(null);
    try { await fn(); setOk(sucesso); router.refresh(); } catch (e) { setErro((e as ErroPedido).message); }
  }

  return (
    <Cartao titulo="Equipa">
      <ErroTopo mensagem={erro} />
      {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
      <ul className="lista limpa">
        {dados.membros.map((m) => (
          <li key={m.id} className="entre">
            <div><p className="t-label">{m.nome || m.email}{m.eu && <span className="muted"> (você)</span>}</p>
              <p className="t-sm muted">{m.email} · {m.funcao_rotulo}</p></div>
            {dados.sou_responsavel && !m.eu && (confirmar === m.id ? (
              <div className="linha">
                <button className="btn btn-danger" onClick={() => correr(() => pedido("DELETE", `/api/v1/entidade/equipa/membros/${m.id}`), `${m.email} deixou de ter acesso.`)}>Confirmar</button>
                <button className="btn btn-ghost" onClick={() => setConfirmar(null)}>Cancelar</button>
              </div>
            ) : <button className="btn btn-ghost" onClick={() => setConfirmar(m.id)}>Retirar</button>)}
          </li>
        ))}
        {dados.convites.map((c) => (
          <li key={c.id} className="entre">
            <div><p className="t-label">{c.email}</p><p className="t-sm muted">Convite pendente · até {fmtData(c.expira_em)}</p></div>
            {dados.sou_responsavel && <button className="btn btn-ghost" onClick={() => correr(() => post(`/api/v1/entidade/equipa/convites/${c.id}/cancelar`), "Convite cancelado.")}>Cancelar convite</button>}
          </li>
        ))}
      </ul>
      {confirmar !== null && <p className="t-sm muted">Ao retirar, a pessoa deixa de entrar na plataforma. As validações que fez continuam no registo, com o nome dela.</p>}
      {dados.sou_responsavel ? (
        <form className="pilha" noValidate onSubmit={(e) => { e.preventDefault(); void correr(async () => { await post("/api/v1/entidade/equipa", { email }); setEmail(""); }, "Convite enviado."); }}>
          <Campo rotulo="Convidar colega por e-mail" type="email" value={email} onChange={(e) => setEmail(e.target.value)}
            ajuda="O colega cria a própria conta e passa a poder criar turmas, convidar startups e validar participações." />
          <div><button className="btn btn-secondary">Enviar convite</button></div>
        </form>
      ) : <p className="t-sm muted">Só o responsável da entidade pode convidar ou retirar membros.</p>}
    </Cartao>
  );
}
