"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { Campo, ErroTopo } from "@/componentes/Campo";
import { mensagemAllauth, pedidoBruto } from "@/lib/api-cliente";

type Passo = "credenciais" | "codigo";

/** C-01: e-mail e palavra-passe pelo allauth headless; se a conta tiver 2FA, pede o código da aplicação. */
export function FormEntrar() {
  const router = useRouter();
  const seguinte = useSearchParams().get("seguinte");
  const [passo, setPasso] = useState<Passo>("credenciais");
  const [email, setEmail] = useState("");
  const [palavra, setPalavra] = useState("");
  const [codigo, setCodigo] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  function concluir() {
    // Só caminhos internos (evita redireccionamentos abertos).
    const destino = seguinte && seguinte.startsWith("/") && !seguinte.startsWith("//") ? seguinte : "/inicio";
    router.replace(destino);
    router.refresh();
  }

  async function entrar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null);
    setAEnviar(true);
    const { estado, dados } = passo === "credenciais"
      ? await pedidoBruto("POST", "/_allauth/browser/v1/auth/login", { email, password: palavra })
      : await pedidoBruto("POST", "/_allauth/browser/v1/auth/2fa/authenticate", { code: codigo.replace(/\s/g, "") });
    setAEnviar(false);
    if (estado === 200 || estado === 409) return concluir();
    if (estado === 401 && dados?.data?.flows?.some((f: { id: string; is_pending?: boolean }) => f.id === "mfa_authenticate" && f.is_pending)) {
      setPasso("codigo");
      return;
    }
    if (estado === 429) return setErro(mensagemAllauth(dados));
    setErro(passo === "credenciais"
      ? "Erro: e-mail ou palavra-passe incorrectos. Confirme os dois e tente de novo."
      : "Erro: o código não está certo ou já expirou. Use o código que a aplicação mostra agora, ou um código de recuperação.");
  }

  return (
    <form className="card pad-lg pilha" onSubmit={entrar} noValidate>
      <ErroTopo mensagem={erro} />
      {passo === "credenciais" ? (
        <>
          <Campo rotulo="E-mail" type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
          <Campo rotulo="Palavra-passe" type="password" autoComplete="current-password" required value={palavra}
            onChange={(e) => setPalavra(e.target.value)}
            ajuda={<Link className="link" href="/recuperar">Esqueci-me da palavra-passe</Link>} />
        </>
      ) : (
        <>
          <p className="t-body">Introduza o código de 6 dígitos da sua aplicação de autenticação.</p>
          <Campo rotulo="Código" inputMode="numeric" autoComplete="one-time-code" required value={codigo}
            onChange={(e) => setCodigo(e.target.value)} ajuda="Se perdeu o telemóvel, use um dos códigos de recuperação." />
        </>
      )}
      <button className="btn btn-primary btn-lg btn-block" type="submit" aria-busy={aEnviar} disabled={aEnviar}>
        {aEnviar ? "A entrar…" : passo === "credenciais" ? "Entrar" : "Confirmar código"}
      </button>
      <p className="t-body">É uma aceleradora ou universidade? <Link className="link" href="/registo/entidade">Registe a entidade</Link>.</p>
    </form>
  );
}
