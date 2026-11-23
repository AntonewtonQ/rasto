import { fmtInt, fmtPct } from "@/lib/formatos";
import type { Metrica } from "@/lib/tipos";

const UNIDADE: Record<string, (v: number) => string> = {
  kz: (v) => `Kz ${fmtInt(v)}`, pct: (v) => fmtPct(v), meses: (v) => `${String(v).replace(".", ",")} meses`, n: (v) => fmtInt(v),
};

export const fmtMetrica = (m: Metrica, v: number) => (UNIDADE[m.unidade] ?? UNIDADE.n)(v);

export function ListaMetricas({ m }: { m: Metrica[] }) {
  if (!m.length) return null;
  return (
    <dl className="metricas">
      {m.map((x) => <div key={x.codigo}><dt className="t-caption muted">{x.rotulo}</dt><dd className="t-label">{fmtMetrica(x, x.valor ?? 0)}</dd></div>)}
    </dl>
  );
}
