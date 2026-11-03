// Ícones de traço 2 (grelha 24) e selos da marca (rasto-marca-v1/sinais), com currentColor.

const ICONES = {
  casa: <><path d="M3 11 12 4l9 7" /><path d="M5 10v10h14V10" /></>,
  turmas: <><circle cx="8" cy="9" r="3" /><circle cx="16" cy="9" r="3" /><path d="M2 20c0-3 3-5 6-5s6 2 6 5" /><path d="M14 15c3 0 8 1 8 5" /></>,
  selo: <><path d="M12 3l2.4 2.1 3.2.2.2 3.2L20 12l-2.2 2.5-.2 3.2-3.2.2L12 20l-2.4-2.1-3.2-.2-.2-3.2L4 12l2.2-2.5.2-3.2 3.2-.2z" /><path d="m9 12 2 2 4-4" /></>,
  pessoa: <><circle cx="12" cy="8" r="4" /><path d="M4 21c0-4 4-6 8-6s8 2 8 6" /></>,
  voltar: <path d="M15 5l-7 7 7 7" />,
  erro: <><circle cx="12" cy="12" r="9" /><path d="M12 7v6M12 16.5v.5" /></>,
  info: <><circle cx="12" cy="12" r="9" /><path d="M12 11v6M12 7.5v.5" /></>,
  aviso: <><path d="M12 3 2 20h20z" /><path d="M12 10v4M12 17v.5" /></>,
  relogio: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
  visto: <path d="m5 12 5 5 9-10" />,
  copiar: <><rect x="9" y="9" width="11" height="11" rx="2" /><path d="M5 15V5a1 1 0 0 1 1-1h9" /></>,
  mais: <path d="M12 5v14M5 12h14" />,
  sair: <><path d="M15 4h4v16h-4" /><path d="M10 8l-4 4 4 4M6 12h10" /></>,
  investidores: <><path d="M4 19h16" /><path d="M6 16V9M11 16V5M16 16v-5" /></>,
  documento: <><path d="M6 3h8l4 4v14H6z" /><path d="M14 3v4h4" /></>,
  sino: <><path d="M6 16V11a6 6 0 1 1 12 0v5l2 2H4z" /><path d="M10 20a2 2 0 0 0 4 0" /></>,
  procurar: <><circle cx="11" cy="11" r="6" /><path d="m16 16 4 4" /></>,
} as const;

export type NomeIcone = keyof typeof ICONES;

export function Icone({ nome, pequeno = false }: { nome: NomeIcone; pequeno?: boolean }) {
  return (
    <svg className={pequeno ? "ic ic-16" : "ic"} viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      {ICONES[nome]}
    </svg>
  );
}

const CARIMBO = "M12 1.1 15.29 4.05 19.71 4.29 19.95 8.71 22.9 12 19.95 15.29 19.71 19.71 15.29 19.95 12 22.9 8.71 19.95 4.29 19.71 4.05 15.29 1.1 12 4.05 8.71 4.29 4.29 8.71 4.05Z";

export type EstadoSelo = "validado" | "validado_com_aviso" | "declarado" | "pendente" | "retirado" | "expirado" | "recusado";

export function Selo({ estado, tamanho = 24 }: { estado: EstadoSelo | string; tamanho?: number }) {
  const validado = estado === "validado" || estado === "validado_com_aviso";
  let forma;
  if (validado)
    forma = <><path d={CARIMBO} fill="currentColor" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
      <path d="M7.6 12.3 10.6 15.2 16.4 9" fill="none" stroke="var(--seal-knock, #fff)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
      {estado === "validado_com_aviso" && <path d="M18 14l4 7h-8z" fill="var(--seal-warn)" />}</>;
  else if (estado === "pendente")
    forma = <><path d={CARIMBO} fill="none" stroke="currentColor" strokeWidth="1.6" strokeDasharray="2.4 2" strokeLinejoin="round" />
      <path d="M12 7.5V12l3 2" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></>;
  else if (estado === "retirado")
    forma = <><path d={CARIMBO} fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
      <path d="M8.5 8.5l7 7M15.5 8.5l-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></>;
  else if (estado === "expirado")
    forma = <><path d={CARIMBO} fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
      <path d="M7.5 16.5l9-9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></>;
  else
    forma = <><circle cx="12" cy="12" r="9.2" fill="none" stroke="currentColor" strokeWidth="2" strokeDasharray="3.2 2.6" />
      <path d="M8.5 12H15.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></>;
  return (
    <svg className={validado ? "seal" : "seal seal-neutral"} width={tamanho} height={tamanho} viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      {forma}
    </svg>
  );
}

export function Simbolo() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M4.5 12.5 10 18 19.5 6.5" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="4.5" cy="12.5" r="2.6" fill="currentColor" /><circle cx="10" cy="18" r="2.6" fill="currentColor" />
      <circle cx="19.5" cy="6.5" r="3.6" fill="currentColor" />
    </svg>
  );
}
