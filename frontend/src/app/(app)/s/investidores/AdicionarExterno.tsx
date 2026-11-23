"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Campo, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";

/** HU18: investidor de fora da plataforma, em Identificado. */
export function AdicionarExterno() {
  const router = useRouter();
  const [aberto, setAberto] = useState(false);
  const [nome, setNome] = useState("");
  const [organizacao, setOrganizacao] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  if (!aberto) return <button type="button" className="btn btn-secondary" onClick={() => setAberto(true)}>Adicionar investidor de fora</button>;
  return (
    <form className="card pad-lg pilha-sm" noValidate onSubmit={async (ev) => {
      ev.preventDefault();
      setErro(null);
      try { await post("/api/v1/startup/pipeline", { nome, organizacao }); setNome(""); setOrganizacao(""); setAberto(false); router.refresh(); }
      catch (e) { setErro((e as ErroPedido).message); }
    }}>
      <ErroTopo mensagem={erro} />
      <Campo rotulo="Nome do investidor" value={nome} onChange={(e) => setNome(e.target.value)} autoFocus />
      <Campo rotulo="Organização" opcional value={organizacao} onChange={(e) => setOrganizacao(e.target.value)} />
      <p className="help">Fica só no seu pipeline, marcado «fora da plataforma». Ele não recebe nada.</p>
      <div className="linha">
        <button className="btn btn-primary" disabled={!nome.trim()}>Adicionar</button>
        <button type="button" className="btn btn-ghost" onClick={() => setAberto(false)}>Cancelar</button>
      </div>
    </form>
  );
}
