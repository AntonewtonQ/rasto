"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { AreaTexto, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtDataExtenso } from "@/lib/formatos";
import type { Sinal } from "@/lib/tipos";

/** E-08: a entidade vê a frase exacta antes de confirmar; recusar e retirar exigem motivo. */
export function Decidir({ s, entidade, verificada }: { s: Sinal; entidade: string; verificada: boolean }) {
  const router = useRouter();
  const [motivo, setMotivo] = useState("");
  const [erro, setErro] = useState<string | null>(null);

  async function decidir(accao: "validar" | "recusar" | "retirar") {
    setErro(null);
    try {
      await post(`/api/v1/validacoes/${s.id}/${accao}`, { motivo });
      router.push(accao === "retirar" ? "/e/validacoes?ver=historico" : "/e/validacoes");
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); }
  }

  return (
    <section className="card pad-lg pilha">
      <ErroTopo mensagem={erro} />
      <p className="t-caption muted">{s.tipo_rotulo} · {s.estado_rotulo}</p>
      {s.estado === "pendente" ? (<>
        <p className="t-label">Vai confirmar:</p>
        <p className="t-body-lg">«{s.frase}»</p>
        <p className="muted">Os investidores vão ver esta frase com o nome da {entidade} e a data de hoje. Pode retirar a validação mais tarde; a retirada fica registada.</p>
        <div className="linha">
          <button className="btn btn-primary btn-lg btn-movel-cheio" disabled={!verificada} onClick={() => decidir("validar")}>
            {s.tipo === "participacao" ? "Confirmar participação" : "Validar marco"}</button>
        </div>
        <hr className="sep" />
        <AreaTexto rotulo="Recusar, com motivo" rows={3} maxLength={300} value={motivo} onChange={(e) => setMotivo(e.target.value)}
          ajuda="O motivo vai só para a startup; o investidor nunca o vê." />
        <div className="linha"><button className="btn btn-danger" onClick={() => decidir("recusar")}>Recusar</button></div>
      </>) : s.estado === "validado" || s.estado === "validado_com_aviso" ? (<>
        <p className="t-body-lg">«{s.frase}»</p>
        <p className="muted">Validado por {s.validado_por} a {fmtDataExtenso(s.validado_em)}.</p>
        <AreaTexto rotulo="Retirar a validação? Motivo (obrigatório)" rows={3} maxLength={300} value={motivo} onChange={(e) => setMotivo(e.target.value)}
          ajuda="A startup vê o motivo. O investidor passa a ver o sinal como declarado. A retirada fica no registo de auditoria." />
        <div className="linha"><button className="btn btn-danger" onClick={() => decidir("retirar")}>Retirar validação</button></div>
      </>) : (<>
        <p>«{s.frase}»</p>
        {s.motivo && <p className="muted">Motivo: {s.motivo}</p>}
      </>)}
    </section>
  );
}
