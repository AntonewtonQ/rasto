import type { Metadata } from "next";
import Link from "next/link";
import { Indicadores } from "@/componentes/Indicadores";
import { Quadro } from "@/componentes/Pipeline";
import { Cabecalho, Vazio } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { Quadro as Q } from "@/lib/tipos";
import { AdicionarExterno } from "./AdicionarExterno";
import { Pedidos, type RespostaPedidos } from "./Pedidos";

export const metadata: Metadata = { title: "Investidores" };

export default async function Investidores({ searchParams }: { searchParams: Promise<{ ver?: string }> }) {
  await exigirPapel("startup");
  const verPedidos = (await searchParams).ver === "pedidos";
  const [q, pedidos] = await Promise.all([
    api<Q>("/api/v1/startup/pipeline"),
    verPedidos ? api<RespostaPedidos>("/api/v1/startup/pedidos-acesso") : Promise.resolve(null),
  ]);
  return (
    <>
      <Cabecalho titulo="Investidores" accoes={!verPedidos && <AdicionarExterno />} />
      <main id="conteudo" className={`conteudo${verPedidos ? " estreito" : ""}`}>
        <nav className="separadores" aria-label="Secções">
          <Link href="/s/investidores" aria-current={!verPedidos ? "page" : undefined}>Pipeline</Link>
          <Link href="/s/investidores?ver=pedidos" aria-current={verPedidos ? "page" : undefined}>Pedidos ({q.pedidos_pendentes ?? 0})</Link>
        </nav>
        {verPedidos && pedidos ? <Pedidos d={pedidos} /> : (<>
          {q.indicadores && <Indicadores d={q.indicadores} />}
          {q.relacoes.length === 0
            ? <Vazio titulo="Ainda sem investidores no pipeline.">Quando aceitar um pedido de acesso, o investidor entra em Contactado. Também pode adicionar investidores de fora da plataforma.</Vazio>
            : <Quadro q={q} base="/s/investidores" />}
        </>)}
      </main>
    </>
  );
}
