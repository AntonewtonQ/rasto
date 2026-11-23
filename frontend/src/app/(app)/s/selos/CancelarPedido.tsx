"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ErroPedido, pedido } from "@/lib/api-cliente";

export function CancelarPedido({ id }: { id: string }) {
  const router = useRouter();
  const [erro, setErro] = useState<string | null>(null);
  return (
    <div className="linha">
      <button className="btn btn-ghost" onClick={async () => {
        try { await pedido("DELETE", `/api/v1/startup/selos/${id}`); router.refresh(); } catch (e) { setErro((e as ErroPedido).message); }
      }}>Cancelar pedido</button>
      {erro && <span className="err" role="alert">Erro: {erro}</span>}
    </div>
  );
}
