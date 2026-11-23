"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { AreaTexto, ErroTopo, Opcoes } from "@/componentes/Campo";
import { Cartao } from "@/componentes/Ui";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtData, fmtHora } from "@/lib/formatos";
import type { RelacaoPipeline } from "@/lib/tipos";

const TIPOS = [{ valor: "contacto", rotulo: "Contacto" }, { valor: "reuniao", rotulo: "Reunião" }, { valor: "nota", rotulo: "Nota" }];

/** Histórico da relação (movimentos e registos), registar contacto e adiar o lembrete (HU20). */
export function DetalheRelacao({ r }: { r: RelacaoPipeline }) {
  const router = useRouter();
  const [tipo, setTipo] = useState("contacto");
  const [texto, setTexto] = useState("");
  const [data, setData] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);

  async function enviar(caminho: string, corpo: object | undefined, mensagem: string) {
    setErro(null); setOk(null);
    try { await post(`/api/v1/pipeline/${r.id}/${caminho}`, corpo); setOk(mensagem); router.refresh(); return true; }
    catch (e) { setErro((e as ErroPedido).message); return false; }
  }

  return (
    <>
      {r.parada && !r.perdida && (
        <div className="aviso aviso-warn" role="status">
          <div className="pilha-sm">
            <p><strong>Relação parada.</strong> Sem movimento nem contacto há mais de 21 dias.</p>
            <div><button type="button" className="btn btn-secondary" onClick={() => enviar("adiar", undefined, "Lembrete adiado 7 dias.")}>Adiar lembrete 7 dias</button></div>
          </div>
        </div>
      )}
      {r.adiado_ate && <p className="t-sm muted">Lembrete adiado até {fmtData(r.adiado_ate)}.</p>}
      <ErroTopo mensagem={erro} />
      {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
      <Cartao titulo="Registar">
        <form className="pilha" noValidate onSubmit={async (ev) => {
          ev.preventDefault();
          const quando = data ? new Date(`${data.split("/").reverse().join("-")}T12:00:00`).toISOString() : undefined;
          if (await enviar("interaccoes", { tipo, texto, ocorreu_em: quando }, "Registado.")) { setTexto(""); setData(""); }
        }}>
          <Opcoes legenda="Tipo" nome={`tipo-${r.id}`} opcoes={TIPOS} valor={tipo} aoMudar={setTipo} />
          <AreaTexto rotulo="O que aconteceu" opcional rows={2} maxLength={600} value={texto} onChange={(e) => setTexto(e.target.value)} />
          <div className="field">
            <label className="label" htmlFor={`data-${r.id}`}>Data <span className="req">(opcional, hoje por defeito)</span></label>
            <input id={`data-${r.id}`} className="input" placeholder="dd/mm/aaaa" inputMode="numeric" value={data} onChange={(e) => setData(e.target.value)} />
          </div>
          <div><button className="btn btn-primary">Registar</button></div>
        </form>
      </Cartao>
      <Cartao titulo="Histórico">
        <ul className="lista limpa">
          {[...(r.interaccoes ?? []).map((i) => ({ chave: `i${i.id}`, em: i.em, texto: `${i.tipo_rotulo}${i.texto ? `: ${i.texto}` : ""}`, autor: i.autor })),
            ...(r.movimentos ?? []).map((m, n) => ({ chave: `m${n}`, em: m.em, texto: m.de ? `${m.de} → ${m.para}` : `Entrou em ${m.para}`, autor: m.autor }))]
            .sort((a, b) => b.em.localeCompare(a.em))
            .map((x) => <li key={x.chave}><p>{x.texto}</p><p className="t-sm subtle">{fmtData(x.em)} {fmtHora(x.em)}{x.autor ? ` · ${x.autor}` : ""}</p></li>)}
        </ul>
        {r.perdida && <p className="t-sm muted">Perdida a {fmtData(r.perdida_em)} · {r.motivo_perda}{r.nota_perda ? ` · «${r.nota_perda}»` : ""} (só a sua equipa vê).</p>}
      </Cartao>
    </>
  );
}
