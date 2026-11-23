import type { Metadata } from "next";
import { Cabecalho } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { EquipaStartup } from "./EquipaStartup";

export const metadata: Metadata = { title: "Equipa" };

export type DadosEquipaStartup = {
  startup: { id: string; nome: string }; sou_fundador: boolean;
  membros: { id: number; nome: string; email: string; funcao: string; funcao_rotulo: string; eu: boolean }[];
  convites: { id: string; email: string; expira_em: string }[];
};

export default async function Equipa() {
  await exigirPapel("startup");
  const d = await api<DadosEquipaStartup>("/api/v1/startup/equipa");
  return (
    <>
      <Cabecalho titulo="Equipa" />
      <main id="conteudo" className="conteudo estreito"><EquipaStartup dados={d} /></main>
    </>
  );
}
