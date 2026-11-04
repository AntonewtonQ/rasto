import "server-only";
import { cookies } from "next/headers";
import { notFound, redirect } from "next/navigation";
import type { Eu } from "./tipos";

// Pedidos do servidor do Next.js ao Django, em nome do utilizador: reencaminham o cookie de sessão.
// O Next.js não guarda sessão nem segredos próprios; quem decide o acesso é sempre a API (base técnica 1.5).
const DJANGO = process.env.DJANGO_INTERNO ?? "http://127.0.0.1:8000";

export class ErroApi extends Error {
  constructor(public estado: number, public codigo: string, mensagem: string) {
    super(mensagem);
  }
}

export async function api<T>(caminho: string): Promise<T> {
  const jar = await cookies();
  const r = await fetch(`${DJANGO}${caminho}`, {
    // O pedido interno é HTTP; o utilizador chegou por HTTPS (Caddy). Sem isto, o Django redireccionaria para HTTPS.
    headers: { cookie: jar.toString(), accept: "application/json", "x-forwarded-proto": "https" },
    cache: "no-store",
  });
  if (r.status === 401) redirect("/entrar");
  if (r.status === 404) notFound();
  const corpo = await r.json().catch(() => ({}));
  if (r.status === 403 && corpo?.erro?.codigo === "mfa_obrigatoria") redirect("/conta/2fa");
  if (!r.ok) throw new ErroApi(r.status, corpo?.erro?.codigo ?? "erro", corpo?.erro?.mensagem ?? "Erro do servidor.");
  return corpo as T;
}

/** Utilizador da sessão, ou null. Não redirecciona. */
export async function eu(): Promise<Eu> {
  const jar = await cookies();
  const r = await fetch(`${DJANGO}/api/v1/eu`, { headers: { cookie: jar.toString(), "x-forwarded-proto": "https" }, cache: "no-store" });
  return (await r.json()) as Eu;
}

/** Exige sessão de um dos papéis indicados; caso contrário, vai para a entrada ou para a área do papel. */
export async function exigirPapel(...papeis: string[]): Promise<Eu & { autenticado: true }> {
  const e = await eu();
  if (!e.autenticado) redirect("/entrar");
  if (!papeis.includes(e.utilizador.papel)) redirect(destinoDoPapel(e.utilizador.papel));
  return e as Eu & { autenticado: true };
}

export function destinoDoPapel(papel: string): string {
  return { entidade: "/e", startup: "/s", investidor: "/i", admin: "/admin/verificacoes" }[papel] ?? "/conta";
}
