"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { AreaTexto, ErroTopo } from "@/componentes/Campo";
import { Cartao } from "@/componentes/Ui";
import { ErroPedido, pedido, post } from "@/lib/api-cliente";
import { fmtMetrica as fmt } from "@/componentes/Metricas";
import { fmtPct, plural } from "@/lib/formatos";
import type { Metrica } from "@/lib/tipos";
import type { DadosActualizacoes } from "./page";

function variacao(m: Metrica, valor: string): string | null {
  const v = Number(valor.replace(/\s/g, "").replace(",", "."));
  if (!valor.trim() || Number.isNaN(v) || m.anterior == null) return null;
  if (m.anterior === 0) return v === 0 ? "igual ao anterior" : null;
  const p = ((v - m.anterior) / m.anterior) * 100;
  return `${p >= 0 ? "+" : ""}${fmtPct(Math.round(p * 10) / 10)} face a ${fmt(m, m.anterior)}`;
}

/** S-12: métricas da fase pré-preenchidas com o mês anterior; publicada não se edita, corrige-se. */
export function FormActualizacao({ d }: { d: DadosActualizacoes }) {
  const router = useRouter();
  const r = d.rascunho;
  const [periodo, setPeriodo] = useState((r?.periodo ?? d.periodo_sugerido).slice(0, 7));
  const [corrige, setCorrige] = useState<string>(r?.corrige?.id ?? "");
  const [valores, setValores] = useState<Record<string, string>>(() => Object.fromEntries(d.modelo.map((m) => [
    m.codigo, String(r?.metricas_brutas?.[m.codigo] ?? m.anterior ?? "")])));
  const [destaques, setDestaques] = useState(r?.destaques ?? "");
  const [ajuda, setAjuda] = useState(r?.pedidos_ajuda ?? "");
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  async function guardar(publicar: boolean) {
    setErro(null); setOk(null); setAEnviar(true);
    try {
      await pedido("PUT", "/api/v1/startup/actualizacoes", { periodo: `${periodo}-01`, metricas: valores, destaques, pedidos_ajuda: ajuda, corrige: corrige || null });
      if (publicar) {
        await post("/api/v1/startup/actualizacoes");
        setOk(d.destinatarios ? `Publicada e enviada a ${plural(d.destinatarios, "investidor", "investidores")}.` : "Publicada.");
        setDestaques(""); setAjuda(""); setCorrige("");
      } else setOk("Rascunho guardado.");
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); } finally { setAEnviar(false); }
  }

  const corrigivel = d.publicadas.filter((a) => !a.corrige);
  return (
    <Cartao titulo="Nova actualização">
      <form className="pilha" noValidate onSubmit={(ev) => { ev.preventDefault(); guardar(true); }}>
        <ErroTopo mensagem={erro} />
        <div className="duas">
          <div className="field">
            <label className="label" htmlFor="periodo">Mês</label>
            <input id="periodo" className="input" type="month" value={periodo} disabled={!!corrige} onChange={(e) => setPeriodo(e.target.value)} />
          </div>
          {corrigivel.length > 0 && (
            <div className="field">
              <label className="label" htmlFor="corrige">É uma correcção?</label>
              <select id="corrige" className="input" value={corrige} onChange={(e) => {
                setCorrige(e.target.value);
                const a = corrigivel.find((x) => x.id === e.target.value);
                if (a) setPeriodo(a.periodo.slice(0, 7));
              }}>
                <option value="">Não, é nova</option>
                {corrigivel.map((a) => <option key={a.id} value={a.id}>Correcção à de {a.mes}</option>)}
              </select>
            </div>
          )}
        </div>
        <fieldset className="pilha-sm">
          <legend className="label">Métricas da fase</legend>
          <p className="help">Sugeridas para a fase da startup, com o valor da última actualização. Deixe em branco o que não quer mostrar.</p>
          <div className="metricas">
            {d.modelo.map((m) => {
              const v = variacao(m, valores[m.codigo] ?? "");
              return (
                <div key={m.codigo} className="field">
                  <label className="label" htmlFor={`m-${m.codigo}`}>{m.rotulo}{m.unidade === "kz" ? " (Kz)" : m.unidade === "pct" ? " (%)" : ""}</label>
                  <input id={`m-${m.codigo}`} className="input" inputMode="decimal" value={valores[m.codigo] ?? ""}
                    onChange={(e) => setValores({ ...valores, [m.codigo]: e.target.value })} aria-describedby={v ? `v-${m.codigo}` : undefined} />
                  {v && <p className="help" id={`v-${m.codigo}`}>{v}</p>}
                </div>
              );
            })}
          </div>
        </fieldset>
        <AreaTexto rotulo="Destaques do mês" rows={3} maxLength={600} value={destaques} onChange={(e) => setDestaques(e.target.value)}
          ajuda="O que mudou: clientes, produto, equipa. Ex.: «Dois restaurantes novos em Benguela.»" />
        <AreaTexto rotulo="Onde precisamos de ajuda" opcional rows={2} maxLength={300} value={ajuda} onChange={(e) => setAjuda(e.target.value)} />
        <p className="t-sm muted">
          {d.destinatarios ? `${plural(d.destinatarios, "investidor com acesso vai", "investidores com acesso vão")} receber por e-mail.`
            : "Ninguém recebe ainda; fica visível a quem tiver acesso no futuro."} Depois de publicada não se edita: corrige-se com uma nova.
        </p>
        {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
        <div className="linha">
          <button className="btn btn-primary" disabled={aEnviar} aria-busy={aEnviar}>Publicar</button>
          <button type="button" className="btn btn-secondary" disabled={aEnviar} onClick={() => guardar(false)}>Guardar rascunho</button>
        </div>
      </form>
    </Cartao>
  );
}
