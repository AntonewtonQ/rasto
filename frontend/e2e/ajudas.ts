import { execFileSync } from "node:child_process";
import { createHmac, randomBytes } from "node:crypto";
import { readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { type Page, expect } from "@playwright/test";

export const PALAVRA = "demonstracao-rasto-2026";
const BACKEND = path.resolve(__dirname, "../../backend");
const PYTHON = process.env.BACKEND_PYTHON ?? path.join(BACKEND, ".venv/bin/python");

export const sufixo = () => randomBytes(3).toString("hex");

/** Corre código Python no backend (dados de teste e leitura da fila de e-mails). */
export function django(codigo: string): string {
  return execFileSync(PYTHON, ["manage.py", "shell", "-c", codigo], { cwd: BACKEND, encoding: "utf8" }).trim();
}

/** Corpo do último e-mail da fila da aplicação para um destinatário. */
export function ultimoEmail(destinatario: string): string {
  return django(`from rasto.nucleo.models import EmailSaida as E; print(E.objects.filter(destinatario='${destinatario}').latest('criado_em').corpo)`);
}

/** E-mails do allauth (recuperação de palavra-passe), escritos em ficheiros quando EMAIL_FICHEIROS está definido. */
export function ultimoEmailEmFicheiro(destinatario: string): string | null {
  const pasta = process.env.EMAIL_FICHEIROS;
  if (!pasta) return null;
  const ficheiros = readdirSync(pasta).map((f) => path.join(pasta, f)).sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs);
  for (const f of ficheiros) {
    const t = readFileSync(f, "utf8");
    if (t.includes(`To: ${destinatario}`)) return t;
  }
  return null;
}

export function criarAdministracao(email: string) {
  django(`from rasto.contas.models import Utilizador as U; U.objects.create_user('${email}', '${PALAVRA}', nome='Administração de teste', papel_id='admin', is_staff=True)`);
}

/** Código TOTP (RFC 6238) a partir do segredo mostrado no ecrã de activação. */
export function totp(segredo: string): string {
  const alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
  let bits = "";
  for (const c of segredo.replace(/=+$/, "").toUpperCase()) bits += alfabeto.indexOf(c).toString(2).padStart(5, "0");
  const chave = Buffer.from(bits.match(/.{8}/g)!.map((b) => parseInt(b, 2)));
  const contador = Buffer.alloc(8);
  contador.writeBigUInt64BE(BigInt(Math.floor(Date.now() / 30_000)));
  const h = createHmac("sha1", chave).update(contador).digest();
  const o = h[h.length - 1] & 15;
  return String((h.readUInt32BE(o) & 0x7fffffff) % 1_000_000).padStart(6, "0");
}

export async function entrar(page: Page, email: string, palavra = PALAVRA) {
  await page.goto("/entrar");
  await page.getByLabel("E-mail").fill(email);
  await page.getByLabel("Palavra-passe").fill(palavra);
  await page.getByRole("button", { name: "Entrar" }).click();
}

/** Falha o teste se a consola mostrar erros que não sejam as respostas esperadas do allauth (401/404). */
export function vigiarConsola(page: Page) {
  const erros: string[] = [];
  page.on("pageerror", (e) => erros.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error" && !/status of (401|404)/.test(m.text())) erros.push(m.text());
  });
  return () => expect(erros, "erros na consola (incluindo violações da CSP)").toEqual([]);
}
