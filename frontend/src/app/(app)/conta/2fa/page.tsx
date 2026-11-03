"use client";

import Link from "next/link";
import QRCode from "qrcode";
import { useCallback, useEffect, useState } from "react";
import { Campo, ErroTopo } from "@/componentes/Campo";
import { Aviso, Cabecalho, Cartao, Voltar } from "@/componentes/Ui";
import { mensagemAllauth, pedidoBruto } from "@/lib/api-cliente";

type Estado = "a_carregar" | "activar" | "activa";
const TOTP = "/_allauth/browser/v1/account/authenticators/totp";
const RECUPERACAO = "/_allauth/browser/v1/account/authenticators/recovery-codes";
const REAUTENTICAR = "/_allauth/browser/v1/auth/reauthenticate";

/** Activação da 2FA por TOTP (obrigatória para a administração, opcional para os restantes).
 *  O allauth exige confirmar a palavra-passe antes de activar ou de mostrar os códigos de recuperação. */
export default function DoisPassos() {
  const [estado, setEstado] = useState<Estado>("a_carregar");
  const [segredo, setSegredo] = useState("");
  const [qr, setQr] = useState("");
  const [codigo, setCodigo] = useState("");
  const [palavra, setPalavra] = useState("");
  const [codigos, setCodigos] = useState<string[] | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  const verCodigos = useCallback(async () => {
    const c = await pedidoBruto("GET", RECUPERACAO);
    setCodigos(c.estado === 200 ? (c.dados.data?.unused_codes ?? []) : null);
  }, []);

  const carregar = useCallback(async () => {
    const r = await pedidoBruto("GET", TOTP);
    if (r.estado === 200) { setEstado("activa"); await verCodigos(); return; }
    if (r.estado === 404 && r.dados?.meta?.secret) {
      setSegredo(r.dados.meta.secret);
      setQr(await QRCode.toDataURL(r.dados.meta.totp_url, { margin: 1, width: 200 }));
      setEstado("activar");
      return;
    }
    setErro(mensagemAllauth(r.dados));
  }, [verCodigos]);

  useEffect(() => {
    const id = requestAnimationFrame(() => { void carregar(); });
    return () => cancelAnimationFrame(id);
  }, [carregar]);

  async function reautenticar(): Promise<boolean> {
    const r = await pedidoBruto("POST", REAUTENTICAR, { password: palavra });
    if (r.estado === 200) return true;
    setErro("Erro: a palavra-passe não está certa.");
    return false;
  }

  async function activar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setAEnviar(true);
    try {
      if (!(await reautenticar())) return;
      const r = await pedidoBruto("POST", TOTP, { code: codigo.replace(/\s/g, "") });
      if (r.estado === 200) { setPalavra(""); await carregar(); return; }
      setErro(r.dados?.errors?.some((e: { param?: string }) => e.param === "code")
        ? "Erro: o código não está certo ou já mudou. Introduza o código que a aplicação mostra agora."
        : mensagemAllauth(r.dados));
    } finally { setAEnviar(false); }
  }

  async function mostrarCodigos(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null);
    if (await reautenticar()) { setPalavra(""); await verCodigos(); }
  }

  return (
    <>
      <Cabecalho titulo="Autenticação em dois passos" voltar={<Voltar href="/conta" rotulo="Voltar à conta" />} />
      <main id="conteudo" className="conteudo estreito">
        <ErroTopo mensagem={erro} />
        {estado === "a_carregar" && <div className="card pad-lg sk" aria-busy="true" />}
        {estado === "activar" && (
          <Cartao titulo="Activar com uma aplicação de autenticação">
            <ol className="pilha-sm">
              <li>Abra uma aplicação de autenticação no telemóvel (por exemplo, Google Authenticator ou Microsoft Authenticator).</li>
              <li>Leia o código QR, ou escreva o segredo à mão.</li>
              <li>Introduza o código de 6 dígitos que a aplicação mostra e confirme a sua palavra-passe.</li>
            </ol>
            {/* eslint-disable-next-line @next/next/no-img-element -- QR gerado no aparelho (data URI); next/image não se aplica */}
            {qr && <img className="qr" src={qr} alt="Código QR para a aplicação de autenticação" width={200} height={200} />}
            <Campo rotulo="Segredo (para escrever à mão)" value={segredo} readOnly />
            <form className="pilha" onSubmit={activar}>
              <Campo rotulo="Código da aplicação" inputMode="numeric" autoComplete="one-time-code" value={codigo} onChange={(e) => setCodigo(e.target.value)} />
              <Campo rotulo="Palavra-passe" type="password" autoComplete="current-password" value={palavra} onChange={(e) => setPalavra(e.target.value)}
                ajuda="Por segurança, confirme a palavra-passe para alterar a autenticação em dois passos." />
              <div><button className="btn btn-primary btn-lg" disabled={aEnviar} aria-busy={aEnviar}>{aEnviar ? "A activar…" : "Activar"}</button></div>
            </form>
          </Cartao>
        )}
        {estado === "activa" && (
          <>
            <Aviso tipo="ok" titulo="Autenticação em dois passos activa." />
            <Cartao titulo="Códigos de recuperação">
              <p className="muted">Cada código serve uma vez para entrar se perder o telemóvel. Guarde-os num sítio seguro.</p>
              {codigos ? (
                <ul className="copiavel mono pilha-sm limpa">{codigos.map((c) => <li key={c}>{c}</li>)}</ul>
              ) : (
                <form className="pilha" onSubmit={mostrarCodigos}>
                  <Campo rotulo="Palavra-passe" type="password" autoComplete="current-password" value={palavra} onChange={(e) => setPalavra(e.target.value)}
                    ajuda="Confirme a palavra-passe para ver os códigos." />
                  <div><button className="btn btn-secondary">Ver códigos</button></div>
                </form>
              )}
            </Cartao>
            <p><Link className="btn btn-secondary" href="/inicio">Continuar</Link></p>
          </>
        )}
      </main>
    </>
  );
}
