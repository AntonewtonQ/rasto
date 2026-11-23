import type { Metadata } from "next";
import Link from "next/link";
import { Decomposicao } from "@/componentes/Compatibilidade";
import { Cabecalho, Cartao, Vazio } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData, fmtDinheiro } from "@/lib/formatos";
import type { PedidoRecebido } from "@/lib/tipos";
import { DecidirPedido, Revogar } from "./DecidirPedido";

export const metadata: Metadata = { title: "Investidores" };

type Resposta = { pendentes: PedidoRecebido[]; com_acesso: PedidoRecebido[]; historico: PedidoRecebido[]; perfil_publicado: boolean };

function Investidor({ p }: { p: PedidoRecebido }) {
  const m = p.investidor.mandato;
  const cheque = [m.cheque_min, m.cheque_max].filter((v) => v != null).map((v) => fmtDinheiro(v as number, m.moeda)).join(" a ");
  return (
    <div className="pilha-sm">
      <p className="t-label">{p.investidor.nome} <span className="muted">· {p.investidor.tipo}{p.investidor.organizacao ? ` · ${p.investidor.organizacao}` : ""}</span></p>
      <p className="t-sm muted">Procura {m.sectores.join(", ")} · {m.fases.join(", ")}{cheque ? ` · cheque de ${cheque}` : ""}{m.geografias.length ? ` · ${m.geografias.join(", ")}` : ""}</p>
    </div>
  );
}

export default async function PedidosInvestidores() {
  await exigirPapel("startup");
  const d = await api<Resposta>("/api/v1/startup/pedidos-acesso");
  return (
    <>
      <Cabecalho titulo="Investidores" />
      <main id="conteudo" className="conteudo estreito">
        {!d.perfil_publicado && d.pendentes.length === 0 && (
          <Vazio titulo="O perfil ainda não está publicado." accao={<Link className="btn btn-primary" href="/s/perfil">Completar e publicar</Link>}>
            Os investidores só encontram a startup e pedem acesso depois de publicar.
          </Vazio>
        )}
        <section className="pilha" aria-labelledby="pend-t">
          <h2 className="t-h3" id="pend-t">Pedidos por responder</h2>
          {d.pendentes.length === 0 ? <p className="muted">Sem pedidos por responder.</p> : d.pendentes.map((p) => (
            <article key={p.id} className="card pad-lg pilha">
              <div className="entre"><Investidor p={p} /><span className="chip chip-neutral">Até {fmtData(p.expira_em)}</span></div>
              <p className="copiavel">«{p.nota}»</p>
              {p.encaixe && <details><summary className="link">Porque este investidor encaixa ({p.encaixe.total}/100)</summary><Decomposicao c={p.encaixe} titulo="Encaixe com o mandato" /></details>}
              <p className="t-sm muted">Se aceitar, passa a ver o contacto do fundador e os documentos. Pode retirar o acesso depois.</p>
              <DecidirPedido id={p.id} />
            </article>
          ))}
        </section>
        <Cartao titulo="Com acesso">
          {d.com_acesso.length === 0 ? <p className="muted">Nenhum investidor tem acesso.</p> : (
            <ul className="lista limpa">{d.com_acesso.map((p) => (
              <li key={p.id} className="entre"><div><Investidor p={p} /><p className="t-sm subtle">Desde {fmtData(p.decidido_em)}</p></div><Revogar id={p.id} /></li>
            ))}</ul>
          )}
        </Cartao>
        {d.historico.length > 0 && (
          <Cartao titulo="Histórico">
            <ul className="lista limpa">{d.historico.map((p) => (
              <li key={p.id} className="entre"><Investidor p={p} /><span className="chip chip-neutral">{p.estado_rotulo}</span></li>
            ))}</ul>
          </Cartao>
        )}
      </main>
    </>
  );
}
