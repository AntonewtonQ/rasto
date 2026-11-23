"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Caixa, Campo, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtHora } from "@/lib/formatos";
import { useRascunho } from "@/lib/rascunho";

/** Registo da startup: conta da fundadora e da startup. Depois, convida a equipa e pede o selo à aceleradora. */
export default function RegistoStartup() {
  const router = useRouter();
  const { dados: d, mudar, guardadoAs, limpar } = useRascunho("registo-startup", { nome: "", nome_startup: "", email: "" });
  const [palavra, setPalavra] = useState("");
  const [consentimento, setConsentimento] = useState(false);
  const [campos, setCampos] = useState<Record<string, string[]>>({});
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  async function enviar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setCampos({}); setAEnviar(true);
    try {
      await post("/api/v1/registo/startup", { ...d, palavra_passe: palavra, consentimento });
      limpar();
      router.push("/s");
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); setCampos((e as ErroPedido).campos); } finally { setAEnviar(false); }
  }

  return (
    <>
      <div className="pilha-sm">
        <h1 className="t-h1">Criar conta da startup</h1>
        <p className="t-body muted">Depois, convide a sua equipa e peça à sua aceleradora o selo de participação.</p>
      </div>
      <form className="card pad-lg pilha" onSubmit={enviar} noValidate>
        <ErroTopo mensagem={erro} />
        <Campo rotulo="Nome da startup" autoComplete="organization" value={d.nome_startup} onChange={(e) => mudar({ nome_startup: e.target.value })} erros={campos.nome_startup} />
        <Campo rotulo="O seu nome" autoComplete="name" value={d.nome} onChange={(e) => mudar({ nome: e.target.value })} erros={campos.nome} />
        <Campo rotulo="E-mail" type="email" autoComplete="email" value={d.email} onChange={(e) => mudar({ email: e.target.value })} erros={campos.email} />
        <Campo rotulo="Palavra-passe" type="password" autoComplete="new-password" value={palavra} onChange={(e) => setPalavra(e.target.value)}
          ajuda="Pelo menos 12 caracteres. Pode usar um gestor de palavras-passe." erros={campos.palavra_passe} />
        <Caixa rotulo="Li o aviso de privacidade. A startup decide sempre o que partilha e com quem." checked={consentimento}
          onChange={(e) => setConsentimento(e.target.checked)} erros={campos.consentimento} />
        <p className="help"><Link className="link" href="/privacidade">Aviso de privacidade</Link>{guardadoAs && ` · Rascunho guardado neste aparelho às ${fmtHora(guardadoAs)}.`}</p>
        <button className="btn btn-primary btn-lg btn-block" disabled={aEnviar} aria-busy={aEnviar}>{aEnviar ? "A criar conta…" : "Criar conta"}</button>
      </form>
      <p className="t-sm">Já tem conta? <Link className="link" href="/entrar">Entrar</Link> · É uma aceleradora? <Link className="link" href="/registo/entidade">Registe a entidade</Link></p>
    </>
  );
}
