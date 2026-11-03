import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { Cabecalho } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { Comprovativo, Organizacao } from "@/lib/tipos";
import { FormSubmeter } from "./FormSubmeter";

export const metadata: Metadata = { title: "Responsável e envio" };

export default async function PassoSubmeter() {
  await exigirPapel("entidade");
  const { organizacao: o, comprovativos } = await api<{ organizacao: Organizacao; comprovativos: Comprovativo[] }>("/api/v1/entidade");
  if (!["rascunho", "pedido_info", "recusada", "expirada"].includes(o.estado_verificacao)) redirect("/e");
  if (!comprovativos.length) redirect("/e/registo/comprovativos");
  return (
    <>
      <Cabecalho titulo="Registo da entidade" />
      <main id="conteudo" className="conteudo estreito">
        <div className="passos">
          <p className="t-label">Passo 3 de 3 · Responsável e envio</p>
          <div className="bar" role="progressbar" aria-valuemin={1} aria-valuemax={3} aria-valuenow={3} aria-label="Passo 3 de 3"><i className="p3" /></div>
        </div>
        <div className="pilha-sm">
          <h2 className="t-h2">Responsável e programa realizado</h2>
          <p className="muted">A administração confirma 4 critérios: existência legal, presença pública, responsável identificado com e-mail institucional e pelo menos um programa já realizado. Prazo indicativo: 3 dias úteis.</p>
        </div>
        <FormSubmeter o={o} />
      </main>
    </>
  );
}
