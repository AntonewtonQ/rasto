"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Caixa, Campo, ErroTopo, Opcoes } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtHora } from "@/lib/formatos";
import { useRascunho } from "@/lib/rascunho";

const TIPOS = [
  { valor: "anjo", rotulo: "Investidor anjo" },
  { valor: "fundo", rotulo: "Fundo" },
  { valor: "corporate", rotulo: "Empresa (corporate)" },
];

/** Registo do investidor. A conta fica activa logo; o passo seguinte é definir o mandato. */
export default function RegistoInvestidor() {
  const router = useRouter();
  const { dados: d, mudar, guardadoAs, limpar } = useRascunho("registo-investidor", { nome: "", tipo: "anjo", organizacao: "", email: "" });
  const [palavra, setPalavra] = useState("");
  const [consentimento, setConsentimento] = useState(false);
  const [campos, setCampos] = useState<Record<string, string[]>>({});
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  async function enviar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setCampos({}); setAEnviar(true);
    try {
      await post("/api/v1/registo/investidor", { ...d, palavra_passe: palavra, consentimento });
      limpar();
      router.push("/i/mandato");
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); setCampos((e as ErroPedido).campos); } finally { setAEnviar(false); }
  }

  return (
    <>
      <div className="pilha-sm">
        <h1 className="t-h1">Criar conta de investidor</h1>
        <p className="t-body muted">Depois, diga o que procura. Mostramos as startups que encaixam e porquê.</p>
      </div>
      <form className="card pad-lg pilha" onSubmit={enviar} noValidate>
        <ErroTopo mensagem={erro} />
        <Campo rotulo="O seu nome" autoComplete="name" value={d.nome} onChange={(e) => mudar({ nome: e.target.value })} erros={campos.nome} />
        <Opcoes legenda="Como investe" nome="tipo" opcoes={TIPOS} valor={d.tipo} aoMudar={(v) => mudar({ tipo: v })} erros={campos.tipo} />
        {d.tipo !== "anjo" && (
          <Campo rotulo="Nome do fundo ou da empresa" autoComplete="organization" value={d.organizacao}
            onChange={(e) => mudar({ organizacao: e.target.value })} erros={campos.organizacao} />
        )}
        <Campo rotulo="E-mail" type="email" autoComplete="email" value={d.email} onChange={(e) => mudar({ email: e.target.value })} erros={campos.email} />
        <Campo rotulo="Palavra-passe" type="password" autoComplete="new-password" value={palavra} onChange={(e) => setPalavra(e.target.value)}
          ajuda="Pelo menos 12 caracteres. Pode usar um gestor de palavras-passe." erros={campos.palavra_passe} />
        <Caixa rotulo="Li o aviso de privacidade. Só vejo os documentos de uma startup depois de ela aceitar o meu pedido." checked={consentimento}
          onChange={(e) => setConsentimento(e.target.checked)} erros={campos.consentimento} />
        <p className="help"><Link className="link" href="/privacidade">Aviso de privacidade</Link>{guardadoAs && ` · Rascunho guardado neste aparelho às ${fmtHora(guardadoAs)}.`}</p>
        <button className="btn btn-primary btn-lg btn-block" disabled={aEnviar} aria-busy={aEnviar}>{aEnviar ? "A criar conta…" : "Criar conta"}</button>
      </form>
      <p className="t-sm">Já tem conta? <Link className="link" href="/entrar">Entrar</Link> · É uma startup? <Link className="link" href="/registo/startup">Crie a conta da startup</Link></p>
    </>
  );
}
