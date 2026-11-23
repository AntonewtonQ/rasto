"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtData } from "@/lib/formatos";
import type { Quadro as Q, RelacaoPipeline } from "@/lib/tipos";

const SOFT_COMMIT = 5;

type Mudanca = { etapa?: number; valor?: number; moeda?: string } | { perder: true; motivo: string; nota: string };

function useAccoes(aoAnunciar: (t: string) => void) {
  const router = useRouter();
  const [erro, setErro] = useState<string | null>(null);
  async function aplicar(r: RelacaoPipeline, m: Mudanca): Promise<boolean> {
    setErro(null);
    try {
      if ("perder" in m) {
        await post(`/api/v1/pipeline/${r.id}/perder`, { motivo: m.motivo, nota: m.nota, versao: r.versao });
        aoAnunciar(`${r.nome} marcado como perdido. Registado. A ronda continua.`);
      } else {
        const novo = await post<RelacaoPipeline>(`/api/v1/pipeline/${r.id}/mover`, { ...m, versao: r.versao });
        aoAnunciar(`${r.nome} movido para ${novo.etapa_nome}.`);
      }
      router.refresh();
      return true;
    } catch (e) {
      const p = e as ErroPedido;
      setErro(p.message);
      if (p.codigo === "conflito") router.refresh();
      return false;
    }
  }
  async function desfazer(r: RelacaoPipeline) {
    try { await post(`/api/v1/pipeline/${r.id}/desfazer-perda`); aoAnunciar(`${r.nome} voltou a ${r.etapa_nome}.`); router.refresh(); }
    catch (e) { setErro((e as ErroPedido).message); }
  }
  return { erro, aplicar, desfazer };
}

/** Folha «Mover para…» (S-08): alternativa ao arrastar, por teclado e no telemóvel (WCAG 2.5.7). */
function Mover({ r, q, etapaInicial, aoFechar, aplicar }:
  { r: RelacaoPipeline; q: Q; etapaInicial?: number; aoFechar: () => void; aplicar: (r: RelacaoPipeline, m: Mudanca) => Promise<boolean> }) {
  const [destino, setDestino] = useState<string>(String(etapaInicial ?? r.etapa));
  const [valor, setValor] = useState(r.valor?.toString() ?? "");
  const [moeda, setMoeda] = useState(r.moeda || "USD");
  const [motivo, setMotivo] = useState("");
  const [nota, setNota] = useState("");
  const etapa = Number(destino);
  const pedeValor = destino !== "perdida" && etapa >= SOFT_COMMIT;
  const id = `mover-${r.id}`;

  async function confirmar(ev: React.FormEvent) {
    ev.preventDefault();
    const ok = destino === "perdida"
      ? await aplicar(r, { perder: true, motivo, nota })
      : await aplicar(r, pedeValor ? { etapa, valor: Number(valor.replace(/\s/g, "")) || undefined, moeda } : { etapa });
    if (ok) aoFechar();
  }

  return (
    <form className="pilha-sm" onSubmit={confirmar} noValidate>
      <div className="field">
        <label className="label" htmlFor={id}>Mover para</label>
        <select id={id} className="input" value={destino} onChange={(e) => setDestino(e.target.value)} autoFocus>
          {q.etapas.map((e) => <option key={e.n} value={e.n}>{e.nome}{e.n === r.etapa ? " (actual)" : ""}</option>)}
          <option value="perdida">Perdido…</option>
        </select>
      </div>
      {pedeValor && (
        <div className="duas">
          <div className="field">
            <label className="label" htmlFor={`${id}-v`}>Valor indicativo</label>
            <input id={`${id}-v`} className="input" inputMode="numeric" value={valor} onChange={(e) => setValor(e.target.value)} />
          </div>
          <div className="field">
            <label className="label" htmlFor={`${id}-m`}>Moeda</label>
            <select id={`${id}-m`} className="input" value={moeda} onChange={(e) => setMoeda(e.target.value)}>
              <option value="USD">USD</option><option value="AOA">Kz</option>
            </select>
          </div>
        </div>
      )}
      {destino === "perdida" && (<>
        <div className="field">
          <label className="label" htmlFor={`${id}-mot`}>Motivo (privado)</label>
          <select id={`${id}-mot`} className="input" value={motivo} onChange={(e) => setMotivo(e.target.value)}>
            <option value="">Escolha…</option>
            {q.motivos.map((m) => <option key={m.valor} value={m.valor}>{m.rotulo}</option>)}
          </select>
        </div>
        <div className="field">
          <label className="label" htmlFor={`${id}-nota`}>Nota privada <span className="req">(opcional)</span></label>
          <input id={`${id}-nota`} className="input" maxLength={300} value={nota} onChange={(e) => setNota(e.target.value)} />
        </div>
      </>)}
      <div className="linha">
        <button className="btn btn-primary" disabled={destino === "perdida" && !motivo}>Confirmar</button>
        <button type="button" className="btn btn-ghost" onClick={aoFechar}>Cancelar</button>
      </div>
    </form>
  );
}

function Cartao({ r, q, base, aberto, etapaInicial, abrir, fechar, aplicar, desfazer }:
  { r: RelacaoPipeline; q: Q; base: string; aberto: boolean; etapaInicial?: number; abrir: () => void; fechar: () => void;
    aplicar: (r: RelacaoPipeline, m: Mudanca) => Promise<boolean>; desfazer: (r: RelacaoPipeline) => void }) {
  return (
    <article className={`cartao-rel${r.parada ? " parada" : ""}${r.perdida ? " perdida" : ""}`} draggable={!r.perdida && !aberto}
      onDragStart={(e) => { e.dataTransfer.setData("text/plain", r.id); e.dataTransfer.effectAllowed = "move"; }}>
      <p className="t-label"><Link className="link" href={`${base}/${r.id}`}>{r.nome}</Link></p>
      {r.sub && <p className="t-sm muted">{r.sub}</p>}
      <div className="linha-sm">
        {r.externa && <span className="chip chip-neutral">Fora da plataforma</span>}
        {r.parada && <span className="chip chip-warn">Parada</span>}
        {r.valor_texto && <span className="chip chip-laterite">{r.valor_texto}</span>}
      </div>
      {r.perdida ? (
        <p className="t-sm muted">Perdida em {r.etapa_nome} · {r.motivo_perda} <button type="button" className="btn btn-ghost" onClick={() => desfazer(r)}>Desfazer</button></p>
      ) : (<>
        <p className="t-sm subtle">Última actividade a {fmtData(r.ultima_actividade)}</p>
        {aberto ? <Mover r={r} q={q} etapaInicial={etapaInicial} aoFechar={fechar} aplicar={aplicar} />
          : <div><button type="button" className="btn btn-secondary" onClick={abrir} aria-label={`Mover ${r.nome}`}>Mover</button></div>}
      </>)}
    </article>
  );
}

/** Pipeline privado (S-08 / I-06): lista por etapa no telemóvel, Kanban com arrastar no computador. */
export function Quadro({ q, base }: { q: Q; base: string }) {
  const [anuncio, setAnuncio] = useState("");
  const [aberto, setAberto] = useState<{ id: string; etapa?: number } | null>(null);
  const [alvo, setAlvo] = useState<number | null>(null);
  const [verPerdidas, setVerPerdidas] = useState(false);
  const { erro, aplicar, desfazer } = useAccoes(setAnuncio);
  const activas = q.relacoes.filter((r) => !r.perdida);
  const perdidas = q.relacoes.filter((r) => r.perdida);

  async function largar(etapa: number, id: string) {
    setAlvo(null);
    const r = activas.find((x) => x.id === id);
    if (!r || r.etapa === etapa) return;
    if (etapa >= SOFT_COMMIT && r.valor === null) setAberto({ id, etapa }); // pede o valor antes de mover
    else await aplicar(r, { etapa });
  }

  const cartao = (r: RelacaoPipeline) => (
    <Cartao key={r.id} r={r} q={q} base={base} aberto={aberto?.id === r.id} etapaInicial={aberto?.id === r.id ? aberto.etapa : undefined}
      abrir={() => setAberto({ id: r.id })} fechar={() => setAberto(null)} aplicar={aplicar} desfazer={desfazer} />
  );

  return (
    <div className="pilha">
      <p className="sr-only" aria-live="polite">{anuncio}</p>
      {anuncio && <p className="aviso aviso-ok" role="status">{anuncio}</p>}
      <ErroTopo mensagem={erro} />
      <div className="kanban">
        {q.etapas.map((e) => {
          const nesta = activas.filter((r) => r.etapa === e.n);
          return (
            <section key={e.n} className={`kanban-col${alvo === e.n ? " alvo" : ""}`} aria-label={`${e.nome}: ${nesta.length}`}
              onDragOver={(ev) => { ev.preventDefault(); setAlvo(e.n); }} onDragLeave={() => setAlvo(null)}
              onDrop={(ev) => { ev.preventDefault(); largar(e.n, ev.dataTransfer.getData("text/plain")); }}>
              <h3><span>{e.nome}</span><span>{nesta.length}</span></h3>
              {nesta.length ? nesta.map(cartao) : <p className="t-sm subtle">Sem relações.</p>}
            </section>
          );
        })}
      </div>
      {perdidas.length > 0 && (
        <div className="pilha-sm">
          <div><button type="button" className="btn btn-ghost" aria-expanded={verPerdidas} onClick={() => setVerPerdidas(!verPerdidas)}>Perdidos ({perdidas.length})</button></div>
          {verPerdidas && perdidas.map(cartao)}
        </div>
      )}
    </div>
  );
}
