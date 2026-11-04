"use client";

import { useSyncExternalStore } from "react";

function subscrever(aviso: () => void) {
  window.addEventListener("online", aviso);
  window.addEventListener("offline", aviso);
  return () => {
    window.removeEventListener("online", aviso);
    window.removeEventListener("offline", aviso);
  };
}

/** Aviso fixo enquanto não houver rede (especificação 2.4, «Aviso em linha · sem rede»). */
export function AvisoRede() {
  const online = useSyncExternalStore(subscrever, () => navigator.onLine, () => true);
  if (online) return null;
  return (
    <div className="aviso aviso-warn aviso-rede" role="status">
      <p><strong>Sem ligação.</strong> O que escreveu está guardado neste aparelho e pode enviá-lo quando houver rede.</p>
    </div>
  );
}
