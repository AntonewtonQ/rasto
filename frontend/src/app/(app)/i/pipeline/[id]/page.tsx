import type { Metadata } from "next";
import Link from "next/link";
import { DetalheRelacao } from "@/componentes/DetalheRelacao";
import { Cabecalho, Voltar } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { RelacaoPipeline } from "@/lib/tipos";

export const metadata: Metadata = { title: "Relação" };

export default async function RelacaoInvestidor({ params }: { params: Promise<{ id: string }> }) {
  await exigirPapel("investidor");
  const r = await api<RelacaoPipeline>(`/api/v1/pipeline/${(await params).id}`);
  return (
    <>
      <Cabecalho titulo={r.nome} voltar={<Voltar href="/i/pipeline" rotulo="Voltar ao pipeline" />} />
      <main id="conteudo" className="conteudo estreito">
        <p className="muted">{r.sub} · {r.perdida ? "Perdida" : r.etapa_nome}{r.valor_texto ? ` · ${r.valor_texto}` : ""} · <Link className="link" href={`/i/startups/${r.startup_id}`}>Ver perfil</Link></p>
        <DetalheRelacao r={r} />
      </main>
    </>
  );
}
