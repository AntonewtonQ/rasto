"use client";

import Link from "next/link";

/** Erro inesperado num ecrã (especificação 5.9: mensagem curta, referência para suporte, «Tentar de novo»). */
export default function Erro({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="publica">
      <main id="conteudo" className="caixa pilha">
        <h1 className="t-h1">Ocorreu um erro do nosso lado.</h1>
        <p className="muted">O que escreveu nos formulários continua guardado neste aparelho. Pode tentar de novo agora ou dentro de alguns minutos.</p>
        {error.digest && <p className="t-sm subtle">Referência para o suporte: <span className="mono">{error.digest}</span></p>}
        <div className="linha">
          <button className="btn btn-primary" onClick={() => reset()}>Tentar de novo</button>
          <Link className="btn btn-ghost" href="/inicio">Ir para o início</Link>
        </div>
      </main>
    </div>
  );
}
