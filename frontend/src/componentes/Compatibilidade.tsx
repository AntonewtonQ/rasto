import { decil, fmtData, fmtDinheiro } from "@/lib/formatos";
import type { Compatibilidade, PerfilStartup } from "@/lib/tipos";

const CLASSE = { compativel: "chip-primary", parcial: "chip-neutral", incompativel: "chip-neutral" } as const;
const ROTULO = { compativel: "Compatível", parcial: "Compatibilidade parcial", incompativel: "Fora do mandato" } as const;

/** Pontuação com o rótulo; o número nunca aparece sozinho (base técnica 5.3). */
export function ChipPontuacao({ c }: { c: Compatibilidade }) {
  return <span className={`chip ${CLASSE[c.classificacao]}`}><strong>{c.total}</strong>/100 · {ROTULO[c.classificacao]}</span>;
}

/** «Porque esta startup»: a decomposição por critério, com a frase em linguagem simples. */
export function Decomposicao({ c, titulo = "Porque esta startup" }: { c: Compatibilidade; titulo?: string }) {
  return (
    <section className="pilha" aria-label={titulo}>
      <div className="entre"><h2 className="t-h3">{titulo}</h2><ChipPontuacao c={c} /></div>
      <ul className="lista limpa">
        {c.criterios.filter((x) => x.peso > 0).map((x) => (
          <li key={x.chave}>
            <div className="entre"><p className="t-label">{x.rotulo}</p><p className="t-sm muted">{x.pontos} de {x.peso}</p></div>
            <div className="crit" role="img" aria-label={`${x.rotulo}: ${x.pontos} de ${x.peso} pontos`}><i className={decil((x.pontos / x.peso) * 100)} /></div>
            <p className="t-sm">{x.frase}</p>
          </li>
        ))}
      </ul>
      <p className="t-sm muted">{c.aviso} Versão {c.versao} dos pesos.</p>
    </section>
  );
}

export function ResumoStartup({ p }: { p: Pick<PerfilStartup, "sector" | "fase" | "provincia" | "cidade" | "ronda"> }) {
  const partes = [p.sector?.nome, p.fase?.nome, [p.cidade, p.provincia?.nome].filter(Boolean).join(", ")].filter(Boolean);
  return (
    <p className="t-sm muted">
      {partes.join(" · ")}
      {p.ronda && <> · Ronda de <strong>{fmtDinheiro(p.ronda.valor_alvo, p.ronda.moeda)}</strong> desde {fmtData(p.ronda.data_inicio)}</>}
    </p>
  );
}
