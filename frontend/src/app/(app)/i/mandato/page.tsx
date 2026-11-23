import type { Metadata } from "next";
import { Cabecalho } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { Catalogo, Mandato } from "@/lib/tipos";
import { FormMandato } from "./FormMandato";

export const metadata: Metadata = { title: "Mandato" };

export default async function PaginaMandato() {
  await exigirPapel("investidor");
  const [catalogo, m] = await Promise.all([
    api<Catalogo>("/api/v1/catalogo"),
    api<{ mandato: Mandato; compativeis: number; publicadas: number }>("/api/v1/investidor/mandato"),
  ]);
  return (
    <>
      <Cabecalho titulo="Mandato" />
      <main id="conteudo" className="conteudo estreito">
        <p className="muted">O que procura. Usamos isto para ordenar as startups e explicar porque cada uma aparece. Pode mudar quando quiser.</p>
        <FormMandato catalogo={catalogo} inicial={m.mandato} compativeis={m.compativeis} publicadas={m.publicadas} />
      </main>
    </>
  );
}
