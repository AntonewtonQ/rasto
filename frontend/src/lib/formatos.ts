// Formatos locais (especificação de interface, secção 5). Iguais aos de rasto/nucleo/formatos.py.

export const SEP = " ";
const MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
const MOEDAS: Record<string, string> = { AOA: "Kz", USD: "USD" };

export function fmtInt(n: number): string {
  const s = String(Math.abs(Math.round(n))).replace(/\B(?=(\d{3})+(?!\d))/g, SEP);
  return n < 0 ? `-${s}` : s;
}

export const fmtDinheiro = (valor: number, moeda: string) => `${MOEDAS[moeda] ?? moeda} ${fmtInt(valor)}`;

export function fmtPct(x: number, casas = 1): string {
  return Number.isInteger(x) ? `${x}%` : `${x.toFixed(casas).replace(".", ",")}%`;
}

// Datas no fuso de Luanda, independentemente do fuso do servidor ou do aparelho.
function partes(d: string | Date) {
  const f = new Intl.DateTimeFormat("pt-PT", { timeZone: "Africa/Luanda", day: "2-digit", month: "2-digit", year: "numeric" });
  const p = Object.fromEntries(f.formatToParts(typeof d === "string" ? dataDe(d) : d).map((x) => [x.type, x.value]));
  return { dia: p.day, mes: p.month, ano: p.year };
}

function dataDe(s: string): Date {
  // "2026-06-26" (data sem hora) é interpretado ao meio-dia para não mudar de dia com o fuso.
  return /^\d{4}-\d{2}-\d{2}$/.test(s) ? new Date(`${s}T12:00:00Z`) : new Date(s);
}

export function fmtData(d?: string | null): string {
  if (!d) return "";
  const { dia, mes, ano } = partes(d);
  return `${dia}/${mes}/${ano}`;
}

export function fmtDataExtenso(d?: string | null): string {
  if (!d) return "";
  const { dia, mes, ano } = partes(d);
  return `${Number(dia)} de ${MESES[Number(mes) - 1]} de ${ano}`;
}

export function fmtHora(d?: string | null): string {
  if (!d) return "";
  return new Intl.DateTimeFormat("pt-PT", { timeZone: "Africa/Luanda", hour: "2-digit", minute: "2-digit" }).format(new Date(d));
}

export const plural = (n: number, s: string, p = `${s}s`) => `${n} ${n === 1 ? s : p}`;

/** Classe de largura em passos de 10% (sem estilos em linha). */
export const decil = (pct: number) => `w-${Math.max(0, Math.min(100, Math.round(pct / 10) * 10))}`;
