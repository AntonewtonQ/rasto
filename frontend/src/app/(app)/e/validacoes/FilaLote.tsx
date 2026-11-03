"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { ErroTopo } from "@/componentes/Campo";
import { Icone } from "@/componentes/Icone";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtData } from "@/lib/formatos";
import type { Sinal } from "@/lib/tipos";

/** E-07: selecção em lote só para participações; cada item mostra a frase exacta e o prazo. */
export function FilaLote({ sinais, podeValidar }: { sinais: Sinal[]; podeValidar: boolean }) {
  const router = useRouter();
  const [sel, setSel] = useState<Set<string>>(new Set());
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  function alternar(id: string) {
    const s = new Set(sel);
    if (s.has(id)) s.delete(id); else s.add(id);
    setSel(s);
  }

  async function validar() {
    setErro(null); setAEnviar(true);
    try {
      await post("/api/v1/validacoes/lote", { sinais: [...sel] });
      setSel(new Set());
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); } finally { setAEnviar(false); }
  }

  return (
    <div className="pilha">
      <ErroTopo mensagem={erro} />
      <p className="muted">Seleccione as participações a confirmar. Só as participações podem ser validadas em lote; os marcos validam-se um a um. Antes de confirmar, leia a frase exacta que o investidor vai ver.</p>
      <ul className="card lista limpa">
        {sinais.map((s) => {
          const urgente = s.dias_restantes !== undefined && s.dias_restantes <= 3;
          return (
            <li key={s.id}>
              <div className="entre">
                <label className="caixa-check">
                  <input type="checkbox" checked={sel.has(s.id)} onChange={() => alternar(s.id)}
                    disabled={!podeValidar || !s.validavel_em_lote} aria-describedby={!s.validavel_em_lote ? `um-${s.id}` : undefined} />
                  <span className="t-label">{s.startup.nome}</span>
                </label>
                <span className={`chip ${urgente ? "chip-warn" : "chip-neutral"}`}><Icone nome={urgente ? "aviso" : "relogio"} pequeno />
                  Expira a {fmtData(s.expira_em)}{urgente ? ` · faltam ${s.dias_restantes} dia${s.dias_restantes === 1 ? "" : "s"}` : ""}</span>
              </div>
              <p className="t-sm"><span className="muted">Vai confirmar:</span> «{s.frase}»</p>
              <p className="t-sm muted">{s.tipo_rotulo} · pedido a {fmtData(s.pedido_em)}{!s.validavel_em_lote && <span id={`um-${s.id}`}> · Marcos validam-se um a um.</span>}</p>
              <div className="linha"><Link className="btn btn-ghost" href={`/e/validacoes/${s.id}`}>Ver e decidir</Link></div>
            </li>
          );
        })}
      </ul>
      {podeValidar && (
        <div className="linha">
          <button className="btn btn-primary btn-lg btn-movel-cheio" onClick={validar} disabled={!sel.size || aEnviar} aria-busy={aEnviar}>
            {sel.size ? `Validar ${sel.size} participaç${sel.size === 1 ? "ão" : "ões"}` : "Validar participações seleccionadas"}
          </button>
          {!sel.size && <span className="help">Seleccione pelo menos uma participação.</span>}
        </div>
      )}
    </div>
  );
}
