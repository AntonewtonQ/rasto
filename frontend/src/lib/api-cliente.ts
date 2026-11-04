"use client";

// Pedidos do navegador à API (mesma origem). Envia o token CSRF do cookie csrftoken no cabeçalho X-CSRFToken,
// como o Django exige em todos os métodos que alteram dados.

export type ErroCampos = Record<string, string[]>;

export class ErroPedido extends Error {
  constructor(public estado: number, public codigo: string, mensagem: string, public campos: ErroCampos = {}) {
    super(mensagem);
  }
}

function lerCookie(nome: string): string {
  const m = document.cookie.match(new RegExp(`(?:^|; )${nome}=([^;]*)`));
  return m ? decodeURIComponent(m[1]) : "";
}

async function garantirCsrf(): Promise<string> {
  let t = lerCookie("csrftoken");
  if (!t) {
    await fetch("/api/v1/csrf", { credentials: "same-origin" });
    t = lerCookie("csrftoken");
  }
  return t;
}

export async function pedido<T = unknown>(metodo: string, caminho: string, corpo?: unknown): Promise<T> {
  const cabecalhos: Record<string, string> = { accept: "application/json" };
  let body: BodyInit | undefined;
  if (metodo !== "GET") cabecalhos["X-CSRFToken"] = await garantirCsrf();
  if (corpo instanceof FormData) body = corpo;
  else if (corpo !== undefined) {
    cabecalhos["content-type"] = "application/json";
    body = JSON.stringify(corpo);
  }
  let r: Response;
  try {
    r = await fetch(caminho, { method: metodo, headers: cabecalhos, body, credentials: "same-origin" });
  } catch {
    throw new ErroPedido(0, "sem_rede", "Sem ligação. O que escreveu continua no formulário; tente de novo quando houver rede.");
  }
  if (r.status === 204) return undefined as T;
  if (r.status === 401 && caminho.startsWith("/api/v1/")) {
    // Sessão expirada a meio: o rascunho fica no aparelho; depois de entrar, volta-se a esta página.
    const aqui = window.location.pathname + window.location.search;
    // Recarga completa de propósito: limpa o estado do cliente associado à sessão que terminou.
    // eslint-disable-next-line @next/next/no-location-assign-relative-destination
    window.location.assign(`/entrar?seguinte=${encodeURIComponent(aqui)}&sessao=expirada`);
    throw new ErroPedido(401, "sem_sessao", "A sessão terminou. Entre de novo; o que escreveu está guardado neste aparelho.");
  }
  const dados = await r.json().catch(() => ({}));
  if (!r.ok) {
    // Formato da API (/api/v1) ou do allauth headless (/_allauth): {"errors": [{"message", "param"}]}
    if (dados?.erro) throw new ErroPedido(r.status, dados.erro.codigo, dados.erro.mensagem, dados.erro.campos ?? {});
    if (Array.isArray(dados?.errors)) {
      const campos: ErroCampos = {};
      for (const e of dados.errors) if (e.param) (campos[e.param] ??= []).push(e.message);
      throw new ErroPedido(r.status, dados.errors[0]?.code ?? "erro", dados.errors.map((e: { message: string }) => e.message).join(" "), campos);
    }
    throw new ErroPedido(r.status, "erro", "Ocorreu um erro. Tente de novo.");
  }
  return dados as T;
}

export const post = <T = unknown>(caminho: string, corpo?: unknown) => pedido<T>("POST", caminho, corpo);

/** Resposta sem conversão em erro (o allauth responde 401 com os passos pendentes, ex.: 2FA). */
export async function pedidoBruto(metodo: string, caminho: string, corpo?: unknown) {
  const cabecalhos: Record<string, string> = { accept: "application/json", "content-type": "application/json" };
  if (metodo !== "GET") cabecalhos["X-CSRFToken"] = await garantirCsrf();
  try {
    const r = await fetch(caminho, { method: metodo, headers: cabecalhos, credentials: "same-origin",
      body: corpo === undefined ? undefined : JSON.stringify(corpo) });
    return { estado: r.status, dados: await r.json().catch(() => ({})) };
  } catch {
    return { estado: 0, dados: { errors: [{ message: "Sem ligação. Tente de novo quando houver rede." }] } };
  }
}

export function mensagemAllauth(dados: { errors?: { message: string }[]; erro?: { mensagem: string } }): string {
  return dados?.erro?.mensagem ?? dados?.errors?.map((e) => e.message).join(" ") ?? "Ocorreu um erro. Tente de novo.";
}
