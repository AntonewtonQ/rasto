"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Caixa, ErroTopo, Opcoes } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";

const MOTIVOS = [
  { valor: "nao_captar", rotulo: "Não estamos a captar agora" },
  { valor: "cheque", rotulo: "O cheque não encaixa" },
  { valor: "fase_sector", rotulo: "Fase ou sector diferente" },
  { valor: "sem_motivo", rotulo: "Prefiro não dizer" },
];

export function DecidirPedido({ id }: { id: string }) {
  const router = useRouter();
  const [aRecusar, setARecusar] = useState(false);
  const [motivo, setMotivo] = useState("sem_motivo");
  const [partilhar, setPartilhar] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  async function decidir(accao: string, corpo?: object) {
    setErro(null); setAEnviar(true);
    try { await post(`/api/v1/startup/pedidos-acesso/${id}/${accao}`, corpo); router.refresh(); }
    catch (e) { setErro((e as ErroPedido).message); } finally { setAEnviar(false); }
  }

  return (
    <div className="pilha">
      <ErroTopo mensagem={erro} />
      {aRecusar ? (<>
        <Opcoes legenda="Motivo (só para si, a não ser que o partilhe)" nome={`motivo-${id}`} opcoes={MOTIVOS} valor={motivo} aoMudar={setMotivo} />
        {motivo !== "sem_motivo" && <Caixa rotulo="Partilhar o motivo com o investidor" checked={partilhar} onChange={(e) => setPartilhar(e.target.checked)} />}
        <p className="t-sm muted">O investidor só pode voltar a pedir daqui a 90 dias.</p>
        <div className="linha">
          <button type="button" className="btn btn-danger" disabled={aEnviar} onClick={() => decidir("recusar", { motivo, partilhar })}>Confirmar recusa</button>
          <button type="button" className="btn btn-ghost" onClick={() => setARecusar(false)}>Cancelar</button>
        </div>
      </>) : (
        <div className="linha">
          <button type="button" className="btn btn-primary" disabled={aEnviar} onClick={() => decidir("aceitar")}>Aceitar</button>
          <button type="button" className="btn btn-secondary" disabled={aEnviar} onClick={() => setARecusar(true)}>Recusar</button>
        </div>
      )}
    </div>
  );
}

export function Revogar({ id }: { id: string }) {
  const router = useRouter();
  const [confirmar, setConfirmar] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  if (!confirmar) return <button type="button" className="btn btn-ghost" onClick={() => setConfirmar(true)}>Retirar acesso</button>;
  return (
    <div className="pilha-sm">
      <ErroTopo mensagem={erro} />
      <p className="t-sm">Deixa de ver os documentos e o contacto.</p>
      <div className="linha">
        <button type="button" className="btn btn-danger" onClick={async () => {
          try { await post(`/api/v1/startup/pedidos-acesso/${id}/revogar`); router.refresh(); } catch (e) { setErro((e as ErroPedido).message); }
        }}>Retirar</button>
        <button type="button" className="btn btn-ghost" onClick={() => setConfirmar(false)}>Cancelar</button>
      </div>
    </div>
  );
}
