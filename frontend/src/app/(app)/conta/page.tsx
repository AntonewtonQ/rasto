import type { Metadata } from "next";
import Link from "next/link";
import { Aviso, Cabecalho, Cartao } from "@/componentes/Ui";
import { eu } from "@/lib/api-servidor";
import { BotaoSair } from "./BotaoSair";

export const metadata: Metadata = { title: "Conta" };
const PAPEIS: Record<string, string> = { startup: "Startup", investidor: "Investidor", entidade: "Entidade validadora", admin: "Administração" };

export default async function Conta() {
  const e = await eu();
  if (!e.autenticado) return null;
  const u = e.utilizador;
  return (
    <>
      <Cabecalho titulo="Conta" />
      <main id="conteudo" className="conteudo estreito">
        <Cartao titulo="Os seus dados">
          <dl className="pilha-sm">
            <div><dt className="t-caption muted">Nome</dt><dd>{u.nome || "—"}</dd></div>
            <div><dt className="t-caption muted">E-mail</dt><dd>{u.email}</dd></div>
            <div><dt className="t-caption muted">Papel</dt><dd>{PAPEIS[u.papel]}</dd></div>
          </dl>
        </Cartao>
        {u.papel === "startup" && (
          <Cartao titulo="Equipa da startup">
            <p className="muted">Convide quem trabalha consigo. Todos gerem o perfil e respondem aos investidores.</p>
            <div><Link className="btn btn-secondary" href="/s/equipa">Gerir a equipa</Link></div>
          </Cartao>
        )}
        <Cartao titulo="Segurança">
          {e.mfa_activa
            ? <Aviso tipo="ok"><p>Autenticação em dois passos activa.</p></Aviso>
            : <p className="muted">A autenticação em dois passos pede um código da aplicação do telemóvel ao entrar. É opcional{u.papel === "admin" ? ", excepto para a administração" : ""}.</p>}
          <div className="linha"><Link className="btn btn-secondary" href="/conta/2fa">{e.mfa_activa ? "Ver códigos de recuperação" : "Activar autenticação em dois passos"}</Link></div>
        </Cartao>
        <Cartao titulo="Privacidade e dados">
          <p className="muted">Pode pedir acesso, rectificação ou eliminação dos seus dados (Lei n.º 22/11).</p>
          <p><Link className="link" href="/privacidade">Ler o aviso de privacidade</Link></p>
        </Cartao>
        <BotaoSair />
      </main>
    </>
  );
}
