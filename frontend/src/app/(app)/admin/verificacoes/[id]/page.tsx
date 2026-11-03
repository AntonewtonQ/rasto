import type { Metadata } from "next";
import { Cabecalho, Voltar } from "@/componentes/Ui";
import { exigirPapel } from "@/lib/api-servidor";
import { Processo } from "./Processo";

export const metadata: Metadata = { title: "Processo de verificação" };

export default async function PaginaProcesso({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  await exigirPapel("admin");
  return (
    <>
      <Cabecalho titulo="Processo de verificação" voltar={<Voltar href="/admin/verificacoes" rotulo="Voltar à lista" />} />
      <main id="conteudo" className="conteudo"><Processo id={id} /></main>
    </>
  );
}
