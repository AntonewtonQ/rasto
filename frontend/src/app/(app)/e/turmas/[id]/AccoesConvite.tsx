"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ErroPedido, post } from "@/lib/api-cliente";
import type { Convite } from "@/lib/tipos";

/** Reenviar, corrigir o e-mail (erro de envio) ou cancelar (E-05). */
export function AccoesConvite({ c }: { c: Convite }) {
  const router = useRouter();
  const [email, setEmail] = useState(c.email);
  const [erro, setErro] = useState<string | null>(null);

  async function accao(nome: "reenviar" | "cancelar") {
    setErro(null);
    try {
      await post(`/api/v1/convites/${c.id}/${nome}`, nome === "reenviar" && email !== c.email ? { email } : {});
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); }
  }

  return (
    <div className="pilha-sm">
      <div className="linha">
        {c.estado === "erro_envio" && (<>
          <label className="sr-only" htmlFor={`email-${c.id}`}>Corrigir e-mail</label>
          <input className="input" id={`email-${c.id}`} type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <button className="btn btn-secondary" onClick={() => accao("reenviar")}>Corrigir e reenviar</button>
        </>)}
        {c.estado === "expirado" && <button className="btn btn-secondary" onClick={() => accao("reenviar")}>Reenviar</button>}
        <button className="btn btn-ghost" onClick={() => accao("cancelar")}>Cancelar convite</button>
      </div>
      {erro && <p className="err" role="alert">Erro: {erro}</p>}
    </div>
  );
}
