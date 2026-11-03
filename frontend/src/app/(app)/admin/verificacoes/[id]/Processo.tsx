"use client";

import { useEffect, useState } from "react";
import { AreaTexto, ErroTopo } from "@/componentes/Campo";
import { Cartao } from "@/componentes/Ui";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtData, fmtHora } from "@/lib/formatos";
import type { Comprovativo, Organizacao } from "@/lib/tipos";

type Avaliacao = { estado: string; nota: string };
type Dados = {
  organizacao: Organizacao; comprovativos: Comprovativo[];
  criterios: { chave: string; rotulo: string; ajuda: string; avaliacao: Avaliacao | null }[];
  estados_criterio: { valor: string; rotulo: string }[];
  historico: { decisao: string; rotulo: string; motivo: string; criado_em: string; decidido_por: string | null }[];
};

/** D-02: abrir o processo (passa a «em análise»), 4 critérios com evidência e nota, decisão e registo. */
export function Processo({ id }: { id: string }) {
  const [d, setD] = useState<Dados | null>(null);
  const [aval, setAval] = useState<Record<string, Avaliacao>>({});
  const [motivo, setMotivo] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);

  function aplicar(x: Dados) {
    setD(x);
    setAval(Object.fromEntries(x.criterios.map((c) => [c.chave, c.avaliacao ?? { estado: "", nota: "" }])));
  }

  useEffect(() => {
    // Abrir o processo é uma escrita (fica no registo), por isso é um POST e não acontece só por ler a lista.
    post<Dados>(`/api/v1/admin/verificacoes/${id}/abrir`).then(aplicar).catch((e: ErroPedido) => setErro(e.message));
  }, [id]);

  async function decidir(decisao: string) {
    setErro(null); setOk(null);
    try {
      aplicar(await post<Dados>(`/api/v1/admin/verificacoes/${id}/decisao`, { decisao, criterios: aval, motivo }));
      setOk("Decisão registada."); setMotivo("");
    } catch (e) { setErro((e as ErroPedido).message); }
  }

  if (!d) return <><ErroTopo mensagem={erro} /><div className="card pad-lg sk" aria-busy="true" /></>;
  const o = d.organizacao;
  const todos = d.criterios.every((c) => aval[c.chave]?.estado === "cumpre");
  const aDecidir = ["submetida", "em_analise"].includes(o.estado_verificacao);

  return (
    <div className="duas">
      <div className="pilha-lg">
        <Cartao titulo={o.nome_legal ?? o.nome} accao={<span className="chip chip-neutral">{o.estado_rotulo}</span>}>
          <dl className="pilha-sm">
            <div><dt className="t-caption muted">Tipo</dt><dd>{o.tipo_rotulo}</dd></div>
            <div><dt className="t-caption muted">Nome público</dt><dd>{o.nome}</dd></div>
            <div><dt className="t-caption muted">NIF</dt><dd className="num">{o.nif}</dd></div>
            <div><dt className="t-caption muted">Site</dt><dd>{o.site ? <a className="link" href={o.site} target="_blank" rel="noopener noreferrer">{o.site}</a> : "—"}</dd></div>
            <div><dt className="t-caption muted">Responsável</dt><dd>{o.responsavel_nome}{o.responsavel_cargo ? `, ${o.responsavel_cargo}` : ""} · {o.responsavel_email}</dd></div>
            <div><dt className="t-caption muted">Programas realizados</dt><dd className="pre">{o.descricao_programa || "—"}</dd></div>
          </dl>
          <h3 className="t-label">Comprovativos</h3>
          <ul className="lista limpa">{d.comprovativos.length ? d.comprovativos.map((c) => (
            <li key={c.id} className="entre"><span>{c.descricao} <span className="t-sm muted">· {c.nome_original}</span></span>
              <a className="link" href={`/api/v1/comprovativos/${c.id}/ficheiro`}>Descarregar</a></li>
          )) : <li className="muted">Sem comprovativos.</li>}</ul>
        </Cartao>
        <Cartao titulo="Registo do processo">
          <ul className="lista limpa">{d.historico.map((h, i) => (
            <li key={i}><span className="t-label">{h.rotulo}</span><span className="t-sm muted">{fmtData(h.criado_em)} {fmtHora(h.criado_em)} · {h.decidido_por}</span>
              {h.motivo && <span className="t-sm pre">{h.motivo}</span>}</li>
          ))}</ul>
        </Cartao>
      </div>
      <section className="card pad-lg pilha">
        <ErroTopo mensagem={erro} />
        {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
        <h2 className="t-h3">Critérios</h2>
        {d.criterios.map((c, i) => (
          <fieldset key={c.chave} className="pilha-sm">
            <legend>{i + 1}. {c.rotulo} <span className="t-sm muted">· {c.ajuda}</span></legend>
            <div className="linha-sm">{d.estados_criterio.map((e) => (
              <label key={e.valor} className="opcao"><input type="radio" name={c.chave} value={e.valor} checked={aval[c.chave]?.estado === e.valor}
                disabled={!aDecidir} onChange={() => setAval({ ...aval, [c.chave]: { ...aval[c.chave], estado: e.valor } })} /><span>{e.rotulo}</span></label>
            ))}</div>
            <label className="sr-only" htmlFor={`nota-${c.chave}`}>Nota e evidência de {c.rotulo}</label>
            <textarea className="input" id={`nota-${c.chave}`} rows={2} maxLength={500} disabled={!aDecidir}
              placeholder="Evidência ou o que falta (vai para a entidade se pedir informação)"
              value={aval[c.chave]?.nota ?? ""} onChange={(ev) => setAval({ ...aval, [c.chave]: { ...aval[c.chave], nota: ev.target.value } })} />
          </fieldset>
        ))}
        <AreaTexto rotulo="Motivo (obrigatório para recusar ou suspender)" rows={2} maxLength={500} value={motivo} onChange={(e) => setMotivo(e.target.value)} />
        <div className="pilha-sm">
          {aDecidir && (<>
            <button className="btn btn-primary btn-lg" disabled={!todos} aria-describedby="ajuda-verificar" onClick={() => decidir("verificar")}>Verificar entidade</button>
            <p className="help" id="ajuda-verificar">Fica activo com os 4 critérios em «Cumpre».</p>
            <button className="btn btn-secondary" onClick={() => decidir("pedir_info")}>Pedir informação (14 dias)</button>
            <button className="btn btn-danger" onClick={() => decidir("recusar")}>Recusar</button>
          </>)}
          {o.estado_verificacao === "verificada" && <button className="btn btn-danger" onClick={() => decidir("suspender")}>Suspender</button>}
          {o.estado_verificacao === "suspensa" && <button className="btn btn-secondary" onClick={() => decidir("reactivar")}>Reactivar</button>}
          {!aDecidir && !["verificada", "suspensa"].includes(o.estado_verificacao) && <p className="muted">À espera da entidade.</p>}
        </div>
      </section>
    </div>
  );
}
