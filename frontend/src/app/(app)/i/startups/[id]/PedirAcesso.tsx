"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { AreaTexto, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";

export function PedirAcesso({ id, origem, posicao }: { id: string; origem: string; posicao?: string }) {
  const router = useRouter();
  const [nota, setNota] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  async function pedir(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setAEnviar(true);
    try {
      await post(`/api/v1/startups/${id}/pedir-acesso`, { nota, origem, posicao });
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); } finally { setAEnviar(false); }
  }

  return (
    <form className="pilha" onSubmit={pedir} noValidate>
      <p className="muted">Se a startup aceitar, vê o contacto do fundador e os documentos. Até lá, nada é partilhado.</p>
      <ErroTopo mensagem={erro} />
      <AreaTexto rotulo="Nota para a startup" rows={3} maxLength={300} value={nota} onChange={(e) => setNota(e.target.value)}
        ajuda="Quem é e porque esta startup. Ex.: «Invisto em agritech em fase seed; o vosso modelo de recolha interessa-me.»" />
      <div><button className="btn btn-primary" disabled={aEnviar || !nota.trim()} aria-busy={aEnviar}>{aEnviar ? "A enviar…" : "Pedir acesso"}</button></div>
    </form>
  );
}

export function RetirarPedido({ id }: { id: string }) {
  const router = useRouter();
  const [erro, setErro] = useState<string | null>(null);
  return (
    <div className="pilha-sm">
      <ErroTopo mensagem={erro} />
      <div><button type="button" className="btn btn-secondary" onClick={async () => {
        try { await post(`/api/v1/investidor/pedidos-acesso/${id}/retirar`); router.refresh(); }
        catch (e) { setErro((e as ErroPedido).message); }
      }}>Retirar pedido</button></div>
    </div>
  );
}
