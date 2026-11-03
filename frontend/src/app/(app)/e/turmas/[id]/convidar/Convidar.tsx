"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { AreaTexto, Campo, ErroTopo } from "@/componentes/Campo";
import { Icone } from "@/componentes/Icone";
import { Aviso } from "@/componentes/Ui";
import { ErroPedido, post } from "@/lib/api-cliente";

type Linha = { numero: number; email: string; situacao: string; mensagem: string; enviavel: boolean };

/** E-06: por e-mail (verificação linha a linha antes de enviar) ou por ligação de uso único para copiar. */
export function Convidar({ turmaId, podeConvidar }: { turmaId: string; podeConvidar: boolean }) {
  const router = useRouter();
  const [separador, setSeparador] = useState<"email" | "ligacao">("email");
  const [texto, setTexto] = useState("");
  const [linhas, setLinhas] = useState<Linha[] | null>(null);
  const [email, setEmail] = useState("");
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [copiado, setCopiado] = useState("");
  const [erro, setErro] = useState<string | null>(null);

  if (!podeConvidar) return <Aviso><p>Os convites ficam disponíveis depois da verificação da entidade.</p></Aviso>;
  const enviaveis = linhas?.filter((l) => l.enviavel).length ?? 0;

  async function verificar(ev?: React.FormEvent) {
    ev?.preventDefault();
    setErro(null);
    try { setLinhas((await post<{ linhas: Linha[] }>(`/api/v1/turmas/${turmaId}/convites/verificar`, { texto })).linhas); }
    catch (e) { setErro((e as ErroPedido).message); }
  }

  async function enviar() {
    setErro(null);
    try {
      await post(`/api/v1/turmas/${turmaId}/convites`, { texto });
      router.push(`/e/turmas/${turmaId}`);
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); }
  }

  async function criarLigacao(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setCopiado("");
    try {
      const r = await post<{ mensagem: string }>(`/api/v1/turmas/${turmaId}/convites/ligacao`, { email });
      setMensagem(r.mensagem); setEmail("");
    } catch (e) { setErro((e as ErroPedido).message); }
  }

  return (
    <>
      <div className="separadores" role="tablist" aria-label="Forma de convite">
        <button role="tab" aria-selected={separador === "email"} aria-current={separador === "email" ? "page" : undefined} onClick={() => setSeparador("email")}>Por e-mail</button>
        <button role="tab" aria-selected={separador === "ligacao"} aria-current={separador === "ligacao" ? "page" : undefined} onClick={() => setSeparador("ligacao")}>Por ligação</button>
      </div>
      <ErroTopo mensagem={erro} />
      {separador === "email" ? (
        <form className="card pad-lg pilha" onSubmit={verificar} noValidate>
          <AreaTexto rotulo="E-mails das startups" rows={6} value={texto} spellCheck={false} ajuda="Um e-mail por linha."
            onChange={(e) => { setTexto(e.target.value); setLinhas(null); }} />
          {linhas && (
            <div className="field" aria-live="polite">
              <p className="label">Verificação, linha a linha</p>
              <ul className="lista limpa">{linhas.map((l) => (
                <li key={l.numero} className="entre"><span className="mono">{l.email}</span>
                  <span className={`t-sm ${["invalido", "outro_papel"].includes(l.situacao) ? "err" : l.enviavel ? "muted" : "subtle"}`}>{l.mensagem}</span></li>
              ))}</ul>
            </div>
          )}
          <div className="linha">
            {linhas ? (<>
              <button className="btn btn-ghost" type="submit">Verificar de novo</button>
              {enviaveis
                ? <button className="btn btn-primary btn-lg btn-movel-cheio" type="button" onClick={enviar}>Enviar {enviaveis} convite{enviaveis === 1 ? "" : "s"}</button>
                : <span className="help">Nenhum e-mail válido para enviar.</span>}
            </>) : <button className="btn btn-primary btn-lg btn-movel-cheio" type="submit">Verificar e-mails</button>}
          </div>
        </form>
      ) : (
        <div className="card pad-lg pilha">
          <p className="muted">Crie uma ligação pessoal de uso único e envie-a pelo WhatsApp ou SMS. A plataforma não envia mensagens por si.</p>
          {mensagem && (
            <div className="field">
              <p className="label">Mensagem pronta para copiar</p>
              <p className="copiavel">{mensagem}</p>
              <div className="linha">
                <button className="btn btn-secondary" type="button" onClick={async () => { await navigator.clipboard?.writeText(mensagem); setCopiado("Mensagem copiada."); }}>
                  <Icone nome="copiar" /> Copiar mensagem</button>
                <span className="t-sm muted" role="status" aria-live="polite">{copiado}</span>
              </div>
              <p className="help">A ligação só aparece agora. Se a perder, cancele este convite e crie outro.</p>
              <hr className="sep" />
            </div>
          )}
          <form className="pilha" onSubmit={criarLigacao} noValidate>
            <Campo rotulo="E-mail da startup" type="email" value={email} onChange={(e) => setEmail(e.target.value)}
              ajuda="A ligação é pessoal e só serve para este e-mail. Usa-se uma vez." />
            <div className="linha"><button className="btn btn-primary btn-lg btn-movel-cheio">Criar ligação</button></div>
          </form>
        </div>
      )}
    </>
  );
}
