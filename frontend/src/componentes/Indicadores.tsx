import Link from "next/link";
import { fmtData, fmtPct, plural } from "@/lib/formatos";
import type { Indicadores as Ind } from "@/lib/tipos";

/** S-13 / HU19: quanto já está comprometido e o que está parado, em 1 minuto. Nada é introduzido duas vezes. */
export function Indicadores({ d, ligacao }: { d: Ind; ligacao?: string }) {
  const c = d.comprometido;
  return (
    <section className="card pad-lg pilha" aria-labelledby="ind-t">
      <div className="entre"><h2 className="t-h3" id="ind-t">Ronda</h2>{ligacao && <Link className="link" href={ligacao}>Ver pipeline</Link>}</div>
      <div className="grelha-3">
        <div className="kpi">
          <span className="t-caption muted">Comprometido</span>
          {!d.ronda || !c ? <span className="t-sm muted">Defina o valor da ronda no perfil para ver este indicador.</span>
            : c.pct === null ? <span className="t-sm">Falta a taxa de referência USD/Kz.</span>
              : <><span className="valor">{fmtPct(c.pct)}</span><span className="t-sm muted">≈ {c.texto}{c.taxa_data ? ` · taxa de ${fmtData(c.taxa_data)}` : ""}</span></>}
        </div>
        <div className="kpi">
          <span className="t-caption muted">Até ao 1.º soft commit</span>
          {d.dias_ate_soft_commit === null ? <span className="t-sm muted">Ainda sem soft commits.</span>
            : <><span className="valor">{d.dias_ate_soft_commit}</span><span className="t-sm muted">{d.dias_ate_soft_commit === 1 ? "dia" : "dias"} desde o início da ronda</span></>}
        </div>
        <div className="kpi">
          <span className="t-caption muted">Relações</span>
          <span className="valor">{d.activas}</span>
          <span className="t-sm muted">{d.paradas ? plural(d.paradas, "parada", "paradas") : "Nenhuma relação parada"}{d.perdidas ? ` · ${plural(d.perdidas, "perdida", "perdidas")}` : ""}</span>
        </div>
      </div>
      {d.conversao ? (
        <details>
          <summary className="link">Conversão por etapa</summary>
          <div className="tbl-wrap"><table className="tbl">
            <thead><tr><th>Etapa</th><th className="num">Chegaram</th><th className="num">Passaram</th><th className="num">Conversão</th></tr></thead>
            <tbody>{d.conversao.map((x) => (
              <tr key={x.etapa}><td>{x.nome}</td><td className="num">{x.chegaram}</td><td className="num">{x.passaram}</td><td className="num">{x.pct === null ? "—" : fmtPct(x.pct)}</td></tr>
            ))}</tbody>
          </table></div>
        </details>
      ) : <p className="t-sm muted">Conversão por etapa: ainda sem dados suficientes (são precisas pelo menos 3 relações).</p>}
    </section>
  );
}
