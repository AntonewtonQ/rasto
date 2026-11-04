"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Caixa, Campo, ErroTopo } from "@/componentes/Campo";
import { Aviso } from "@/componentes/Ui";
import { ErroPedido, pedidoBruto, post } from "@/lib/api-cliente";
import { useRascunho } from "@/lib/rascunho";

export function FormConvite({ token, email, contaExiste, sessao }:
  { token: string; email: string; contaExiste: boolean; sessao: { papel: string; email: string } | null }) {
  const router = useRouter();
  const { dados: r, mudar, limpar } = useRascunho(`convite-${token.slice(0, 12)}`, { nome: "", startup: "" });
  const { nome, startup } = r;
  const setNome = (v: string) => mudar({ nome: v });
  const setStartup = (v: string) => mudar({ startup: v });
  const [palavra, setPalavra] = useState("");
  const [consentimento, setConsentimento] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [campos, setCampos] = useState<Record<string, string[]>>({});
  const [recusado, setRecusado] = useState(false);
  const base = `/api/v1/convites/publico/${encodeURIComponent(token)}`;

  async function aceitar(corpo?: object) {
    setErro(null); setCampos({});
    try {
      await post(`${base}/aceitar`, corpo ?? {});
      limpar();
      router.push("/s");
      router.refresh();
    } catch (e) {
      setErro((e as ErroPedido).message); setCampos((e as ErroPedido).campos);
    }
  }

  async function recusar() {
    try { await post(`${base}/recusar`); setRecusado(true); } catch (e) { setErro((e as ErroPedido).message); }
  }

  async function sair() {
    await pedidoBruto("DELETE", "/_allauth/browser/v1/auth/session");
    router.refresh();
  }

  if (recusado) return <Aviso tipo="info" titulo="Convite recusado."><p>A entidade foi avisada. Se mudar de ideias, peça um novo convite.</p></Aviso>;

  if (sessao && sessao.papel !== "startup")
    return (<>
      <Aviso tipo="warn" alerta><p>Tem sessão iniciada com uma conta que não é de startup. Cada conta tem um só papel: para aceitar este convite, saia e crie a conta da startup com o e-mail {email}.</p></Aviso>
      <button className="btn btn-secondary" onClick={sair}>Sair desta conta</button>
    </>);

  if (sessao)
    return (<div className="pilha-sm">
      <ErroTopo mensagem={erro} />
      <button className="btn btn-primary btn-lg btn-block" onClick={() => aceitar()}>Juntar a startup à turma</button>
      <button className="btn btn-ghost" onClick={recusar}>Recusar convite</button>
    </div>);

  if (contaExiste)
    return (<>
      <Aviso tipo="info"><p>Já existe uma conta com {email}. Entre para juntar a startup a esta turma.</p></Aviso>
      <Link className="btn btn-primary btn-lg btn-block" href={`/entrar?seguinte=/convite/${token}`}>Entrar para aceitar</Link>
    </>);

  return (
    <form className="card pad-lg pilha" noValidate onSubmit={(e) => { e.preventDefault(); aceitar({ nome, nome_startup: startup, palavra_passe: palavra, consentimento }); }}>
      <ErroTopo mensagem={erro} />
      <Campo rotulo="E-mail" value={email} readOnly autoComplete="email" ajuda="É o e-mail do convite. Vai usá-lo para entrar." />
      <Campo rotulo="O seu nome" autoComplete="name" value={nome} onChange={(e) => setNome(e.target.value)} erros={campos.nome} />
      <Campo rotulo="Nome da startup" autoComplete="organization" value={startup} onChange={(e) => setStartup(e.target.value)} erros={campos.nome_startup} />
      <Campo rotulo="Palavra-passe" type="password" autoComplete="new-password" value={palavra} onChange={(e) => setPalavra(e.target.value)}
        ajuda="Pelo menos 12 caracteres. Pode usar um gestor de palavras-passe." erros={campos.palavra_passe} />
      <Caixa rotulo="Li o aviso de privacidade. A startup decide sempre o que partilha e com quem." checked={consentimento}
        onChange={(e) => setConsentimento(e.target.checked)} erros={campos.consentimento} />
      <p className="help"><Link className="link" href="/privacidade">Aviso de privacidade</Link></p>
      <div className="pilha-sm">
        <button className="btn btn-primary btn-lg btn-block" type="submit">Aceitar e criar conta</button>
        <button className="btn btn-ghost" type="button" onClick={recusar}>Recusar convite</button>
      </div>
    </form>
  );
}
