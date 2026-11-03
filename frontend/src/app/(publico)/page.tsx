import Link from "next/link";
import { redirect } from "next/navigation";
import { eu } from "@/lib/api-servidor";

export default async function Entrada() {
  const e = await eu();
  if (e.autenticado) redirect("/inicio");
  return (
    <>
      <div className="trilho" aria-hidden="true" />
      <div className="pilha-sm">
        <h1 className="t-display">Confiança que se verifica.</h1>
        <p className="t-body-lg muted">Startups aceleradas e investidores em Angola a decidir com a mesma informação. Cada sinal mostra quem o confirmou e quando.</p>
      </div>
      <div className="pilha-sm">
        <Link className="btn btn-primary btn-lg btn-block" href="/entrar">Entrar</Link>
        <Link className="btn btn-secondary btn-lg btn-block" href="/registo/entidade">Registar aceleradora ou universidade</Link>
      </div>
      <p className="t-sm muted">As startups entram por convite da sua aceleradora ou universidade.</p>
    </>
  );
}
