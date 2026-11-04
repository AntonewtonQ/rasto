"use client";

import { useCallback, useEffect, useState } from "react";

/** Rascunho guardado neste aparelho (regra 5 da base de UX: nenhum formulário perde dados por falha de rede ou
 *  por a sessão expirar). Nunca guardar palavras-passe. A reposição acontece depois da primeira pintura, para
 *  não haver diferenças entre o HTML do servidor e o do aparelho. */
export function useRascunho<T extends Record<string, unknown>>(chave: string, inicial: T) {
  const k = `rasto:${chave}`;
  const [dados, setDados] = useState<T>(inicial);
  const [guardadoAs, setGuardadoAs] = useState<string | null>(null);

  useEffect(() => {
    const id = requestAnimationFrame(() => {
      try {
        const r = JSON.parse(localStorage.getItem(k) ?? "null");
        if (r?.dados) { setDados((d) => ({ ...d, ...r.dados })); setGuardadoAs(r.hora); }
      } catch { /* sem armazenamento: o formulário funciona na mesma */ }
    });
    return () => cancelAnimationFrame(id);
  }, [k]);

  const mudar = useCallback((parcial: Partial<T>) => {
    setDados((d) => {
      const novo = { ...d, ...parcial };
      const hora = new Date().toISOString();
      try { localStorage.setItem(k, JSON.stringify({ hora, dados: novo })); setGuardadoAs(hora); } catch { /* idem */ }
      return novo;
    });
  }, [k]);

  const limpar = useCallback(() => {
    try { localStorage.removeItem(k); } catch { /* idem */ }
    setGuardadoAs(null);
  }, [k]);

  return { dados, mudar, guardadoAs, limpar };
}
