import type { Metadata } from "next";
import Link from "next/link";
import { Selo } from "@/componentes/Icone";
import { api } from "@/lib/api-servidor";
import { fmtDataExtenso } from "@/lib/formatos";
import type { Organizacao, Turma } from "@/lib/tipos";
import { FormConvite } from "./FormConvite";

export const metadata: Metadata = { title: "Convite" };

type ConvitePublico = {
  estado: string; email: string; expira_em: string; turma: Turma; organizacao: Organizacao;
  enviado_por: string | null; conta_existe: boolean; sessao?: { papel: string; email: string };
};

export default async function Convite({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  const c = await api<ConvitePublico>(`/api/v1/convites/publico/${encodeURIComponent(token)}`);
  const org = c.organizacao.nome;

  if (c.estado === "expirado")
    return (<><h1 className="t-h1">Este convite expirou em {fmtDataExtenso(c.expira_em)}.</h1><p className="muted">Peça um novo convite à {org}.</p></>);
  if (c.estado === "aceite")
    return (<><h1 className="t-h1">Este convite já foi aceite.</h1><p><Link className="btn btn-primary btn-lg" href="/entrar">Entrar</Link></p></>);
  if (!["pendente", "erro_envio"].includes(c.estado))
    return (<><h1 className="t-h1">Este convite já não está disponível.</h1><p className="muted">Foi cancelado ou recusado. Peça um novo convite à {org}.</p></>);

  return (
    <>
      <div className="pilha-sm">
        <h1 className="t-h1">{org} convidou a sua startup</h1>
        <p className="linha-sm muted">Turma {c.turma.nome} · {c.turma.periodo} ·{" "}
          <span className="chip chip-primary"><Selo estado="validado" tamanho={16} />Entidade verificada pela plataforma</span></p>
        {c.enviado_por && <p className="t-sm muted">Convite enviado por {c.enviado_por}, válido até {fmtDataExtenso(c.expira_em)}.</p>}
      </div>
      <div className="card pad-lg pilha-sm">
        <p className="t-label">Depois de aceitar:</p>
        <ul className="pilha-sm">
          <li>a {org} pode confirmar que a startup participou no programa; os investidores vêem essa confirmação com o nome de quem a fez e a data;</li>
          <li>o perfil fica em rascunho até decidir publicá-lo;</li>
          <li>a startup decide sempre o que partilha e com quem.</li>
        </ul>
      </div>
      <FormConvite token={token} email={c.email} contaExiste={c.conta_existe} sessao={c.sessao ?? null} />
      <p className="t-sm subtle">Se não reconhece este convite, ignore esta página.</p>
    </>
  );
}
