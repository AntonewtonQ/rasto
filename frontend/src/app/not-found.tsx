import Link from "next/link";

export default function NaoEncontrado() {
  return (
    <div className="publica">
      <main id="conteudo" className="caixa">
        <h1 className="t-h1">Página não encontrada</h1>
        <p className="muted">A ligação pode estar errada, ou esta página não pertence à sua conta.</p>
        <p><Link className="btn btn-primary" href="/inicio">Ir para o início</Link></p>
      </main>
    </div>
  );
}
