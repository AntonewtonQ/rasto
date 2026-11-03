import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { Aviso, Cabecalho } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData } from "@/lib/formatos";
import type { Comprovativo, Organizacao } from "@/lib/tipos";
import { Comprovativos } from "./Comprovativos";

export const metadata: Metadata = { title: "Comprovativos" };
const EDITAVEL = ["rascunho", "pedido_info", "recusada", "expirada"];

export default async function PassoComprovativos() {
  await exigirPapel("entidade");
  const { organizacao: o, comprovativos } = await api<{ organizacao: Organizacao; comprovativos: Comprovativo[] }>("/api/v1/entidade");
  if (!EDITAVEL.includes(o.estado_verificacao)) redirect("/e");
  return (
    <>
      <Cabecalho titulo="Registo da entidade" />
      <main id="conteudo" className="conteudo estreito">
        <div className="passos">
          <p className="t-label">Passo 2 de 3 · Comprovativos</p>
          <div className="bar" role="progressbar" aria-valuemin={1} aria-valuemax={3} aria-valuenow={2} aria-label="Passo 2 de 3"><i className="p2" /></div>
        </div>
        {o.estado_verificacao === "pedido_info" && (
          <Aviso tipo="warn" titulo={`A plataforma pediu mais informação até ${fmtData(o.prazo_resposta)}.`}>
            <p className="pre">{o.motivo}</p><p>Anexe o que falta aqui e reenvie no passo seguinte. Não precisa de recomeçar.</p>
          </Aviso>
        )}
        {o.estado_verificacao === "recusada" && <Aviso tipo="err" titulo="A verificação foi recusada."><p>Motivo: {o.motivo}</p><p>Pode corrigir e submeter de novo.</p></Aviso>}
        <div className="pilha-sm">
          <h2 className="t-h2">Comprovativos da {o.nome}</h2>
          <p className="muted">Servem só para a verificação. Apenas a administração da plataforma os vê. Anexe pelo menos um: a certidão ou registo comercial e uma evidência de um programa já realizado ajudam a decidir mais depressa.</p>
        </div>
        <Comprovativos iniciais={comprovativos} />
      </main>
    </>
  );
}
