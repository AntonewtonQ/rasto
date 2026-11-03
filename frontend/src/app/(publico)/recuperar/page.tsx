"use client";

import Link from "next/link";
import { useState } from "react";
import { Campo } from "@/componentes/Campo";
import { Aviso } from "@/componentes/Ui";
import { pedidoBruto } from "@/lib/api-cliente";

/** C-02: a resposta é sempre a mesma, exista ou não o e-mail. */
export default function Recuperar() {
  const [email, setEmail] = useState("");
  const [enviado, setEnviado] = useState(false);
  const [aEnviar, setAEnviar] = useState(false);

  async function enviar(ev: React.FormEvent) {
    ev.preventDefault();
    setAEnviar(true);
    await pedidoBruto("POST", "/_allauth/browser/v1/auth/password/request", { email });
    setAEnviar(false);
    setEnviado(true);
  }

  return (
    <>
      <div className="pilha-sm">
        <h1 className="t-h1">Recuperar palavra-passe</h1>
        <p className="t-body muted">Indique o e-mail da sua conta. Enviamos uma ligação para definir uma nova palavra-passe, válida durante 1 hora.</p>
      </div>
      {enviado ? (
        <Aviso tipo="info" titulo="Verifique o seu e-mail.">
          <p>Se o e-mail existir na plataforma, enviámos uma ligação para definir uma nova palavra-passe.</p>
        </Aviso>
      ) : (
        <form className="card pad-lg pilha" onSubmit={enviar}>
          <Campo rotulo="E-mail" type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
          <button className="btn btn-primary btn-lg btn-block" disabled={aEnviar} aria-busy={aEnviar}>{aEnviar ? "A enviar…" : "Enviar ligação"}</button>
        </form>
      )}
      <p><Link className="link" href="/entrar">Voltar a entrar</Link></p>
    </>
  );
}
