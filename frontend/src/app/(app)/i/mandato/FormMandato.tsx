"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Campo, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, pedido } from "@/lib/api-cliente";
import { fmtData, plural } from "@/lib/formatos";
import type { Catalogo, Item, Mandato } from "@/lib/tipos";

function Escolhas({ legenda, ajuda, itens, valor, aoMudar }:
  { legenda: string; ajuda?: string; itens: Item[]; valor: string[]; aoMudar: (v: string[]) => void }) {
  return (
    <fieldset className="pilha-sm">
      <legend className="label">{legenda}</legend>
      {ajuda && <p className="help">{ajuda}</p>}
      <div className="linha-sm">
        {itens.map((i) => {
          const on = valor.includes(i.id);
          return (
            <button key={i.id} type="button" className="pick" aria-pressed={on} title={i.descricao || undefined}
              onClick={() => aoMudar(on ? valor.filter((x) => x !== i.id) : [...valor, i.id])}>{i.nome}</button>
          );
        })}
      </div>
    </fieldset>
  );
}

export function FormMandato({ catalogo, inicial, compativeis, publicadas }:
  { catalogo: Catalogo; inicial: Mandato; compativeis: number; publicadas: number }) {
  const router = useRouter();
  const [m, setM] = useState(inicial);
  const [min, setMin] = useState(inicial.cheque_min?.toString() ?? "");
  const [max, setMax] = useState(inicial.cheque_max?.toString() ?? "");
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [aGuardar, setAGuardar] = useState(false);
  const mudar = (p: Partial<Mandato>) => { setM({ ...m, ...p }); setOk(null); };
  const numero = (s: string) => (s.trim() ? Number(s.replace(/\s/g, "")) : null);

  async function guardar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setOk(null); setAGuardar(true);
    try {
      const r = await pedido<{ compativeis: number; publicadas: number; mandato: Mandato }>("PUT", "/api/v1/investidor/mandato", {
        sectores: m.sectores, fases: m.fases, geografias: m.geografias, risco: m.risco,
        cheque_min: numero(min), cheque_max: numero(max), moeda_cheque: m.moeda_cheque,
      });
      setM(r.mandato);
      setOk(r.mandato.minimo_completo
        ? `Mandato guardado. ${plural(r.compativeis, "startup compatível", "startups compatíveis")} de ${r.publicadas} publicadas.`
        : "Mandato guardado. Escolha pelo menos um sector e uma fase para ver sugestões.");
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); } finally { setAGuardar(false); }
  }

  const ao = catalogo.geografia.find((g) => g.codigo === "AO");
  const provincias = catalogo.geografia.filter((g) => g.codigo !== "AO");
  return (
    <form className="card pad-lg pilha-lg" onSubmit={guardar} noValidate>
      <ErroTopo mensagem={erro} />
      <Escolhas legenda="Sectores" ajuda="Obrigatório. Escolha um ou mais." itens={catalogo.sector} valor={m.sectores} aoMudar={(v) => mudar({ sectores: v })} />
      <Escolhas legenda="Fases" ajuda="Obrigatório. Uma fase vizinha da sua conta em parte." itens={catalogo.fase} valor={m.fases} aoMudar={(v) => mudar({ fases: v })} />
      <fieldset className="pilha-sm">
        <legend className="label">Valor do cheque <span className="req">(opcional)</span></legend>
        <div className="linha">
          <select className="input" aria-label="Moeda do cheque" value={m.moeda_cheque} onChange={(e) => mudar({ moeda_cheque: e.target.value })}>
            <option value="USD">USD</option><option value="AOA">Kz</option>
          </select>
        </div>
        <div className="duas">
          <Campo rotulo="Mínimo" inputMode="numeric" value={min} onChange={(e) => { setMin(e.target.value); setOk(null); }} />
          <Campo rotulo="Máximo" inputMode="numeric" value={max} onChange={(e) => { setMax(e.target.value); setOk(null); }} />
        </div>
        <p className="help">Sem limites, o cheque conta como encaixe total.
          {catalogo.taxa && ` Kz e USD comparam-se com a taxa de referência de ${fmtData(catalogo.taxa.data)} (1 USD = ${catalogo.taxa.aoa_por_usd.replace(".", ",")} Kz).`}</p>
      </fieldset>
      <Escolhas legenda="Geografia (opcional)" ajuda="Sem escolha, todas as províncias contam."
        itens={[...(ao ? [ao] : []), ...provincias]} valor={m.geografias} aoMudar={(v) => mudar({ geografias: v })} />
      {ok && <p className="aviso aviso-ok" role="status">{ok} {m.minimo_completo && <Link className="link" href="/i/sugestoes">Ver sugestões</Link>}</p>}
      {!ok && inicial.minimo_completo && <p className="t-sm muted">Agora: {plural(compativeis, "startup compatível", "startups compatíveis")} de {publicadas} publicadas.</p>}
      <div><button className="btn btn-primary" disabled={aGuardar} aria-busy={aGuardar}>{aGuardar ? "A guardar…" : "Guardar mandato"}</button></div>
    </form>
  );
}
