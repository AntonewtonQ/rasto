"use client";

import { useRouter } from "next/navigation";
import { Icone } from "@/componentes/Icone";
import { pedidoBruto } from "@/lib/api-cliente";

export function BotaoSair() {
  const router = useRouter();
  return (
    <div>
      <button className="btn btn-ghost" onClick={async () => {
        await pedidoBruto("DELETE", "/_allauth/browser/v1/auth/session");
        router.replace("/entrar");
        router.refresh();
      }}><Icone nome="sair" /> Sair</button>
    </div>
  );
}
