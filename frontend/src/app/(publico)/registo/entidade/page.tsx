"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Caixa, Campo, ErroTopo, Opcoes } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtHora } from "@/lib/formatos";

const CHAVE = "rasto:registo-entidade";
const VAZIO = { tipo: "", nome_legal: "", nif: "", site: "", cidade: "Luanda", nome: "", email: "" };

/** E-01, passo 1 de 3. Rascunho guardado neste aparelho (sem a palavra-passe). */
export default function RegistoEntidade() {
  const router = useRouter();
  const [d, setD] = useState(VAZIO);
  const [palavra, setPalavra] = useState("");
  const [consentimento, setConsentimento] = useState(false);
  const [campos, setCampos] = useState<Record<string, string[]>>({});
  const [erro, setErro] = useState<string | null>(null);
  const [guardadoAs, setGuardadoAs] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  // Repõe o rascunho depois da primeira pintura (a página é pré-gerada; localStorage só existe no aparelho).
  useEffect(() => {
    const id = requestAnimationFrame(() => {
      try {
        const r = JSON.parse(localStorage.getItem(CHAVE) ?? "null");
        if (r) { setD({ ...VAZIO, ...r.dados }); setGuardadoAs(r.hora); }
      } catch { /* sem armazenamento: o formulário funciona na mesma */ }
    });
    return () => cancelAnimationFrame(id);
  }, []);

  function mudar(campo: keyof typeof VAZIO, valor: string) {
    const novo = { ...d, [campo]: valor };
    setD(novo);
    const hora = new Date().toISOString();
    try { localStorage.setItem(CHAVE, JSON.stringify({ hora, dados: novo })); setGuardadoAs(hora); } catch { /* idem */ }
  }

  async function enviar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setCampos({}); setAEnviar(true);
    try {
      await post("/api/v1/registo/entidade", { ...d, site: d.site && !/^https?:\/\//.test(d.site) ? `https://${d.site}` : d.site, palavra_passe: palavra, consentimento });
      try { localStorage.removeItem(CHAVE); } catch { /* idem */ }
      router.push("/e/registo/comprovativos");
      router.refresh();
    } catch (e) {
      const err = e as ErroPedido;
      setErro(err.message); setCampos(err.campos);
    } finally { setAEnviar(false); }
  }

  return (
    <>
      <div className="passos">
        <p className="t-label">Passo 1 de 3 · Entidade</p>
        <div className="bar" role="progressbar" aria-valuemin={1} aria-valuemax={3} aria-valuenow={1} aria-label="Passo 1 de 3"><i className="p1" /></div>
      </div>
      <div className="pilha-sm">
        <h1 className="t-h1">Registar aceleradora ou universidade</h1>
        <p className="t-body muted">Depois de verificada pela plataforma, a entidade pode convidar as startups das suas turmas e confirmar a participação delas. Os investidores vêem cada confirmação com o nome da entidade e a data.</p>
      </div>
      <form className="card pad-lg pilha" onSubmit={enviar} noValidate>
        <ErroTopo mensagem={erro} />
        <h2 className="t-h3">A entidade</h2>
        <Opcoes legenda="Tipo de entidade" nome="tipo" valor={d.tipo} aoMudar={(v) => mudar("tipo", v)} erros={campos.tipo}
          opcoes={[{ valor: "aceleradora", rotulo: "Aceleradora ou incubadora" }, { valor: "universidade", rotulo: "Universidade ou centro de empreendedorismo" }]} />
        <Campo rotulo="Nome legal" autoComplete="organization" value={d.nome_legal} onChange={(e) => mudar("nome_legal", e.target.value)} erros={campos.nome_legal} />
        <Campo rotulo="NIF" inputMode="numeric" value={d.nif} onChange={(e) => mudar("nif", e.target.value)} ajuda="Só dígitos, como consta na certidão." erros={campos.nif} />
        <Campo rotulo="Site ou página pública" opcional value={d.site} onChange={(e) => mudar("site", e.target.value)} ajuda="Ajuda a verificação (presença pública)." erros={campos.site} />
        <Campo rotulo="Cidade" value={d.cidade} onChange={(e) => mudar("cidade", e.target.value)} erros={campos.cidade} />
        <hr className="sep" />
        <h2 className="t-h3">A sua conta</h2>
        <Campo rotulo="O seu nome" autoComplete="name" value={d.nome} onChange={(e) => mudar("nome", e.target.value)} erros={campos.nome} />
        <Campo rotulo="E-mail institucional" type="email" autoComplete="email" value={d.email} onChange={(e) => mudar("email", e.target.value)}
          ajuda="Usado para entrar e para a verificação." erros={campos.email} />
        <Campo rotulo="Palavra-passe" type="password" autoComplete="new-password" value={palavra} onChange={(e) => setPalavra(e.target.value)}
          ajuda="Pelo menos 12 caracteres. Pode usar um gestor de palavras-passe." erros={campos.palavra_passe} />
        <Caixa rotulo="Li o aviso de privacidade e aceito o tratamento dos dados para a verificação da entidade." checked={consentimento}
          onChange={(e) => setConsentimento(e.target.checked)} erros={campos.consentimento} />
        <p className="help"><Link className="link" href="/privacidade">Aviso de privacidade</Link>{guardadoAs && ` · Rascunho guardado neste aparelho às ${fmtHora(guardadoAs)}.`}</p>
        <div className="linha"><button className="btn btn-primary btn-lg btn-movel-cheio" disabled={aEnviar} aria-busy={aEnviar}>{aEnviar ? "A criar conta…" : "Continuar para os comprovativos"}</button></div>
      </form>
      <p className="t-sm">Já tem conta? <Link className="link" href="/entrar">Entrar</Link></p>
    </>
  );
}
