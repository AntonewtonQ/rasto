import type { Metadata } from "next";
import Link from "next/link";
import { api } from "@/lib/api-servidor";
import { fmtDataExtenso } from "@/lib/formatos";
import { FormEquipa } from "./FormEquipa";

export const metadata: Metadata = { title: "Convite para a equipa" };

type ConviteEquipa = { tipo: "entidade" | "startup"; nome: string; estado: string; email: string; expira_em: string; enviado_por: string | null };

export default async function ConviteEquipaPagina({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  const c = await api<ConviteEquipa>(`/api/v1/equipa/convites/${encodeURIComponent(token)}`);
  if (c.estado === "aceite")
    return (<><h1 className="t-h1">Este convite já foi aceite.</h1><p><Link className="btn btn-primary btn-lg" href="/entrar">Entrar</Link></p></>);
  if (c.estado !== "pendente")
    return (<><h1 className="t-h1">Este convite já não está disponível.</h1><p className="muted">Peça um novo convite à equipa da {c.nome}.</p></>);
  return (
    <>
      <div className="pilha-sm">
        <h1 className="t-h1">Equipa da {c.nome}</h1>
        <p className="muted">{c.enviado_por ? `${c.enviado_por} convidou-o` : "Foi convidado"} para a equipa. Válido até {fmtDataExtenso(c.expira_em)}.</p>
      </div>
      <FormEquipa token={token} email={c.email} destino={c.tipo === "startup" ? "/s" : "/e"} />
    </>
  );
}
