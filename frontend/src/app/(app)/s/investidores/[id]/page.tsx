import type { Metadata } from "next";
import { DetalheRelacao } from "@/componentes/DetalheRelacao";
import { Cabecalho, Voltar } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { RelacaoPipeline } from "@/lib/tipos";

export const metadata: Metadata = { title: "Relação" };

export default async function RelacaoStartup({ params }: { params: Promise<{ id: string }> }) {
  await exigirPapel("startup");
  const r = await api<RelacaoPipeline>(`/api/v1/pipeline/${(await params).id}`);
  return (
    <>
      <Cabecalho titulo={r.nome} voltar={<Voltar href="/s/investidores" rotulo="Voltar ao pipeline" />} />
      <main id="conteudo" className="conteudo estreito">
        <p className="muted">{r.sub} · {r.perdida ? "Perdida" : r.etapa_nome}{r.valor_texto ? ` · ${r.valor_texto}` : ""}</p>
        <DetalheRelacao r={r} />
      </main>
    </>
  );
}
