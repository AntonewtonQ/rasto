"use client";

import Link from "next/link";
import { use, useState } from "react";
import { Campo, ErroTopo } from "@/componentes/Campo";
import { Aviso } from "@/componentes/Ui";
import { mensagemAllauth, pedidoBruto } from "@/lib/api-cliente";

export default function NovaPalavraPasse({ params }: { params: Promise<{ chave: string }> }) {
  const { chave } = use(params);
  const [palavra, setPalavra] = useState("");
  const [estado, setEstado] = useState<"form" | "feito" | "expirada">("form");
  const [erro, setErro] = useState<string | null>(null);

  async function guardar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null);
    const r = await pedidoBruto("POST", "/_allauth/browser/v1/auth/password/reset", { key: decodeURIComponent(chave), password: palavra });
    // 401 = alterada (o allauth não inicia sessão: ACCOUNT_LOGIN_ON_PASSWORD_RESET = False)
    if (r.estado === 200 || r.estado === 401) return setEstado("feito");
    if (r.dados?.errors?.some((e: { param?: string }) => e.param === "key")) return setEstado("expirada");
    setErro(mensagemAllauth(r.dados));
  }

  if (estado === "expirada")
    return (<>
      <h1 className="t-h1">Esta ligação expirou</h1>
      <p className="muted">A ligação já foi usada ou passou mais de 1 hora.</p>
      <p><Link className="btn btn-primary btn-lg" href="/recuperar">Pedir nova ligação</Link></p>
    </>);
  if (estado === "feito")
    return (<>
      <Aviso tipo="ok" titulo="Palavra-passe alterada."><p>As outras sessões da conta terminaram. Já pode entrar.</p></Aviso>
      <p><Link className="btn btn-primary btn-lg" href="/entrar">Entrar</Link></p>
    </>);
  return (
    <>
      <h1 className="t-h1">Definir nova palavra-passe</h1>
      <form className="card pad-lg pilha" onSubmit={guardar}>
        <ErroTopo mensagem={erro} />
        <Campo rotulo="Nova palavra-passe" type="password" autoComplete="new-password" required minLength={12} value={palavra}
          onChange={(e) => setPalavra(e.target.value)} ajuda="Pelo menos 12 caracteres. Pode usar um gestor de palavras-passe." />
        <button className="btn btn-primary btn-lg btn-block">Guardar palavra-passe</button>
      </form>
    </>
  );
}
