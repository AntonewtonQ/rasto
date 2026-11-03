import type { Metadata } from "next";
import { Cabecalho, Voltar } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { Sinal } from "@/lib/tipos";
import { Decidir } from "./Decidir";

export const metadata: Metadata = { title: "Validar" };

export default async function Validacao({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const e = await exigirPapel("entidade");
  const s = await api<Sinal>(`/api/v1/validacoes/${id}`);
  return (
    <>
      <Cabecalho titulo={s.startup.nome} voltar={<Voltar href="/e/validacoes" rotulo="Voltar às validações" />} />
      <main id="conteudo" className="conteudo estreito">
        <Decidir s={s} entidade={e.organizacao?.nome ?? "entidade"} verificada={e.organizacao?.estado_verificacao === "verificada"} />
      </main>
    </>
  );
}
