import type { Metadata } from "next";
import Link from "next/link";
import { Selo } from "@/componentes/Icone";
import { Aviso, Cabecalho, Vazio } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData } from "@/lib/formatos";
import type { Sinal } from "@/lib/tipos";
import { FilaLote } from "./FilaLote";

export const metadata: Metadata = { title: "Validações" };

export default async function Validacoes({ searchParams }: { searchParams: Promise<{ ver?: string }> }) {
  const { ver } = await searchParams;
  const e = await exigirPapel("entidade");
  const historico = ver === "historico";
  const { sinais } = await api<{ sinais: Sinal[] }>(`/api/v1/validacoes${historico ? "?ver=historico" : ""}`);
  const verificada = e.organizacao?.estado_verificacao === "verificada";
  return (
    <>
      <Cabecalho titulo="Validações" />
      <main id="conteudo" className="conteudo">
        <nav className="separadores" aria-label="Validações">
          <Link href="/e/validacoes" aria-current={!historico ? "page" : undefined}>Pendentes{!historico ? ` (${sinais.length})` : ""}</Link>
          <Link href="/e/validacoes?ver=historico" aria-current={historico ? "page" : undefined}>Histórico</Link>
        </nav>
        {!verificada && <Aviso tipo="warn"><p>As validações estão bloqueadas enquanto a entidade não estiver verificada.</p></Aviso>}
        {!historico ? (
          sinais.length ? <FilaLote sinais={sinais} podeValidar={verificada} />
            : <Vazio titulo="Nenhum pedido à espera">Quando uma startup aceitar um convite, a participação aparece aqui para confirmar.</Vazio>
        ) : sinais.length ? (
          <ul className="card lista limpa">{sinais.map((s) => (
            <li key={s.id}>
              <div className="entre"><span className="t-label">{s.startup.nome}</span>
                {s.estado === "validado"
                  ? <span className="chip chip-primary"><Selo estado="validado" tamanho={16} />Validado a {fmtData(s.validado_em)}</span>
                  : <span className="chip chip-neutral">{s.estado_rotulo} a {fmtData(s.actualizado_em)}</span>}</div>
              <p className="t-sm">«{s.frase_validada || s.descricao}»</p>
              {(s.validado_por || s.motivo) && <p className="t-sm muted">{s.validado_por && `Por ${s.validado_por}`}{s.motivo && ` · motivo: ${s.motivo}`}</p>}
              {s.estado === "validado" && <div className="linha"><Link className="btn btn-ghost" href={`/e/validacoes/${s.id}`}>Retirar validação</Link></div>}
            </li>
          ))}</ul>
        ) : <p className="muted">Ainda sem decisões.</p>}
      </main>
    </>
  );
}
