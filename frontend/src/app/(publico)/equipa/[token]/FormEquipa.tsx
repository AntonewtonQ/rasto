"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Caixa, Campo, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";

export function FormEquipa({ token, email }: { token: string; email: string }) {
  const router = useRouter();
  const [nome, setNome] = useState("");
  const [palavra, setPalavra] = useState("");
  const [consentimento, setConsentimento] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [campos, setCampos] = useState<Record<string, string[]>>({});

  async function aceitar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setCampos({});
    try {
      await post(`/api/v1/equipa/convites/${encodeURIComponent(token)}/aceitar`, { nome, palavra_passe: palavra, consentimento });
      router.push("/e");
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); setCampos((e as ErroPedido).campos); }
  }

  return (
    <form className="card pad-lg pilha" onSubmit={aceitar} noValidate>
      <ErroTopo mensagem={erro} />
      <Campo rotulo="E-mail" value={email} readOnly ajuda="É o e-mail do convite. Vai usá-lo para entrar." />
      <Campo rotulo="O seu nome" autoComplete="name" value={nome} onChange={(e) => setNome(e.target.value)} erros={campos.nome} />
      <Campo rotulo="Palavra-passe" type="password" autoComplete="new-password" value={palavra} onChange={(e) => setPalavra(e.target.value)}
        ajuda="Pelo menos 12 caracteres. Pode usar um gestor de palavras-passe." erros={campos.palavra_passe} />
      <Caixa rotulo="Li o aviso de privacidade." checked={consentimento} onChange={(e) => setConsentimento(e.target.checked)} erros={campos.consentimento} />
      <p className="help"><Link className="link" href="/privacidade">Aviso de privacidade</Link></p>
      <button className="btn btn-primary btn-lg btn-block">Aceitar e criar conta</button>
    </form>
  );
}
