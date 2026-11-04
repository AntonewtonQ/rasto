import { expect, test } from "@playwright/test";
import { PALAVRA, django, entrar, sufixo, ultimoEmail, ultimoEmailEmFicheiro, vigiarConsola } from "./ajudas";

test("equipa da entidade: convite, aceitação e membro sem gestão", async ({ page, context }) => {
  const semErros = vigiarConsola(page);
  const colega = `colega-${sufixo()}@kalandula.test`;
  await entrar(page, "gestora@kalandula.demo");
  await page.waitForURL(/\/e$/);
  await page.getByRole("link", { name: "Entidade" }).click();
  await page.getByLabel("Convidar colega por e-mail").fill(colega);
  await page.getByRole("button", { name: "Enviar convite" }).click();
  await expect(page.getByText("Convite enviado.")).toBeVisible();
  await context.clearCookies();
  const ligacao = ultimoEmail(colega).match(/https?:\/\/\S+\/equipa\/\S+?\//)![0];
  await page.goto(new URL(ligacao).pathname);
  await page.getByLabel("O seu nome").fill("Colega Teste");
  await page.getByLabel("Palavra-passe").fill(PALAVRA);
  await page.getByLabel("Li o aviso de privacidade.").check();
  await page.getByRole("button", { name: "Aceitar e criar conta" }).click();
  await page.waitForURL(/\/e$/);
  await page.goto("/e/entidade");
  await expect(page.getByText("Só o responsável da entidade pode convidar")).toBeVisible();
  semErros();
});

test("recuperação da palavra-passe de ponta a ponta", async ({ page }) => {
  test.skip(!process.env.EMAIL_FICHEIROS, "Precisa do Django com EMAIL_FICHEIROS para ler o e-mail do allauth.");
  const email = `recupera-${sufixo()}@startup.test`;
  django(`from rasto.contas.models import Utilizador as U; U.objects.create_user('${email}', '${PALAVRA}', papel_id='investidor')`);
  await page.goto("/recuperar");
  await page.getByLabel("E-mail").fill(email);
  await page.getByRole("button", { name: "Enviar ligação" }).click();
  await expect(page.getByText("Verifique o seu e-mail.")).toBeVisible();
  await expect.poll(() => ultimoEmailEmFicheiro(email)).not.toBeNull();
  const mensagem = ultimoEmailEmFicheiro(email)!;
  expect(mensagem).toContain("Definir nova palavra-passe");
  const ligacao = mensagem.match(/https?:\/\/\S+\/recuperar\/\S+/)![0];
  await page.goto(new URL(ligacao).pathname);
  const nova = `${PALAVRA}-nova`;
  await page.getByLabel("Nova palavra-passe").fill(nova);
  await page.getByRole("button", { name: "Guardar palavra-passe" }).click();
  await expect(page.getByText("Palavra-passe alterada.")).toBeVisible();
  await entrar(page, email, nova);
  await page.waitForURL(/\/i$/);
  // A ligação só serve uma vez.
  await page.goto(new URL(ligacao).pathname);
  await page.getByLabel("Nova palavra-passe").fill(`${nova}-2`);
  await page.getByRole("button", { name: "Guardar palavra-passe" }).click();
  await expect(page.getByRole("heading", { name: "Esta ligação expirou" })).toBeVisible();
});
