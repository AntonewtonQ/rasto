import type { Metadata } from "next";
import { Cabecalho, Voltar } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { Turma } from "@/lib/tipos";
import { Convidar } from "./Convidar";

export const metadata: Metadata = { title: "Convidar startups" };

export default async function PaginaConvidar({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  await exigirPapel("entidade");
  const { turma, pode_convidar } = await api<{ turma: Turma; pode_convidar: boolean }>(`/api/v1/turmas/${id}`);
  return (
    <>
      <Cabecalho titulo="Convidar startups" voltar={<Voltar href={`/e/turmas/${id}`} rotulo="Voltar à turma" />} />
      <main id="conteudo" className="conteudo estreito">
        <p className="muted">{turma.nome} · os convites expiram em 14 dias.</p>
        <Convidar turmaId={id} podeConvidar={pode_convidar} />
      </main>
    </>
  );
}
