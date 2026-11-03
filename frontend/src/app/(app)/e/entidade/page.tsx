import type { Metadata } from "next";
import { Cabecalho, Cartao, EstadoVerificacao } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData } from "@/lib/formatos";
import type { Organizacao } from "@/lib/tipos";
import { Equipa } from "./Equipa";

export const metadata: Metadata = { title: "Entidade" };

export type DadosEquipa = {
  organizacao: Organizacao; sou_responsavel: boolean;
  membros: { id: number; nome: string; email: string; funcao: string; funcao_rotulo: string; eu: boolean }[];
  convites: { id: string; email: string; expira_em: string; criado_em: string }[];
};

/** E-09: perfil da entidade tal como os investidores o vêem e membros da equipa. */
export default async function PaginaEntidade() {
  await exigirPapel("entidade");
  const d = await api<DadosEquipa>("/api/v1/entidade/equipa");
  const o = d.organizacao;
  return (
    <>
      <Cabecalho titulo="Entidade" />
      <main id="conteudo" className="conteudo estreito">
        <Cartao titulo={o.nome} accao={<EstadoVerificacao estado={o.estado_verificacao} rotulo={o.estado_rotulo} />}>
          <dl className="pilha-sm">
            <div><dt className="t-caption muted">Tipo</dt><dd>{o.tipo_rotulo}</dd></div>
            <div><dt className="t-caption muted">Nome legal</dt><dd>{o.nome_legal}</dd></div>
            <div><dt className="t-caption muted">NIF</dt><dd className="num">{o.nif}</dd></div>
            <div><dt className="t-caption muted">Site</dt><dd>{o.site || "—"}</dd></div>
            {o.verificada_em && <div><dt className="t-caption muted">Verificada pela plataforma</dt><dd>{fmtData(o.verificada_em)}</dd></div>}
          </dl>
          <p className="t-sm muted">Os investidores vêem o nome, o tipo e a data da verificação junto de cada sinal que a entidade validar.</p>
        </Cartao>
        <Equipa dados={d} />
      </main>
    </>
  );
}
