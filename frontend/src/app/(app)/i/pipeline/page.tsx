import type { Metadata } from "next";
import Link from "next/link";
import { Quadro } from "@/componentes/Pipeline";
import { Cabecalho, Vazio } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { Quadro as Q } from "@/lib/tipos";

export const metadata: Metadata = { title: "Pipeline" };

export default async function PipelineInvestidor() {
  await exigirPapel("investidor");
  const q = await api<Q>("/api/v1/investidor/pipeline");
  return (
    <>
      <Cabecalho titulo="Pipeline" />
      <main id="conteudo" className="conteudo">
        <p className="muted">Privado: a startup não vê em que etapa a tem.</p>
        {q.relacoes.length === 0
          ? <Vazio titulo="Ainda sem startups no pipeline." accao={<Link className="btn btn-primary" href="/i/sugestoes">Ver sugestões</Link>}>
              Quando uma startup aceitar o seu pedido de acesso, entra aqui em Contactado.
            </Vazio>
          : <Quadro q={q} base="/i/pipeline" />}
      </main>
    </>
  );
}
