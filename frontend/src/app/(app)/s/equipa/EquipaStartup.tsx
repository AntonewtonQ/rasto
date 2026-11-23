"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Campo, ErroTopo } from "@/componentes/Campo";
import { Cartao } from "@/componentes/Ui";
import { ErroPedido, pedido, post } from "@/lib/api-cliente";
import { fmtData } from "@/lib/formatos";
import type { DadosEquipaStartup } from "./page";

export function EquipaStartup({ dados }: { dados: DadosEquipaStartup }) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [confirmar, setConfirmar] = useState<number | null>(null);

  async function correr(fn: () => Promise<unknown>, sucesso: string) {
    setErro(null); setOk(null);
    try { await fn(); setOk(sucesso); setConfirmar(null); router.refresh(); } catch (e) { setErro((e as ErroPedido).message); }
  }

  return (
    <Cartao titulo={`Equipa da ${dados.startup.nome}`}>
      <ErroTopo mensagem={erro} />
      {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
      <ul className="lista limpa">
        {dados.membros.map((m) => (
          <li key={m.id} className="entre">
            <div><p className="t-label">{m.nome || m.email}{m.eu && <span className="muted"> (você)</span>}</p>
              <p className="t-sm muted">{m.email} · {m.funcao_rotulo}</p></div>
            {dados.sou_fundador && !m.eu && (confirmar === m.id ? (
              <div className="linha">
                <button className="btn btn-danger" onClick={() => correr(() => pedido("DELETE", `/api/v1/startup/equipa/membros/${m.id}`), `${m.email} deixou de ter acesso.`)}>Confirmar</button>
                <button className="btn btn-ghost" onClick={() => setConfirmar(null)}>Cancelar</button>
              </div>
            ) : <button className="btn btn-ghost" onClick={() => setConfirmar(m.id)}>Retirar</button>)}
          </li>
        ))}
        {dados.convites.map((c) => (
          <li key={c.id} className="entre">
            <div><p className="t-label">{c.email}</p><p className="t-sm muted">Convite pendente · até {fmtData(c.expira_em)}</p></div>
            {dados.sou_fundador && <button className="btn btn-ghost" onClick={() => correr(() => post(`/api/v1/startup/equipa/convites/${c.id}/cancelar`), "Convite cancelado.")}>Cancelar convite</button>}
          </li>
        ))}
      </ul>
      {dados.sou_fundador ? (
        <form className="pilha" noValidate onSubmit={(e) => { e.preventDefault(); void correr(async () => { await post("/api/v1/startup/equipa", { email }); setEmail(""); }, "Convite enviado."); }}>
          <Campo rotulo="Convidar membro da equipa por e-mail" type="email" value={email} onChange={(e) => setEmail(e.target.value)}
            ajuda="O colega cria a própria conta e entra na equipa da startup." />
          <div><button className="btn btn-secondary">Enviar convite</button></div>
        </form>
      ) : <p className="t-sm muted">Só os fundadores podem convidar ou retirar membros.</p>}
    </Cartao>
  );
}
