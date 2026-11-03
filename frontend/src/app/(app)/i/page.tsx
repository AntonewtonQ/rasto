import type { Metadata } from "next";
import { Cabecalho, Vazio } from "@/componentes/Ui";
import { exigirPapel } from "@/lib/api-servidor";

export const metadata: Metadata = { title: "Início" };

export default async function InicioInvestidor() {
  await exigirPapel("investidor");
  return (
    <>
      <Cabecalho titulo="Início" />
      <main id="conteudo" className="conteudo">
        <Vazio titulo="A área do investidor chega no Sprint 2.">O mandato e as sugestões de startups compatíveis ainda não estão disponíveis nesta versão.</Vazio>
      </main>
    </>
  );
}
