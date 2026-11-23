import { expect, test } from "@playwright/test";
import { PALAVRA, entrar, sufixo, ultimoEmail, vigiarConsola } from "./ajudas";

// Fluxo definido pelo autor: a startup cria conta, convida a equipa e pede à aceleradora o selo de participação.
test("a startup cria conta, convida a equipa e pede o selo", async ({ page, context }) => {
  const s = sufixo();
  const semErros = vigiarConsola(page);
  const fundadora = `fundadora-${s}@startup.test`;
  const colega = `colega-${s}@startup.test`;
  const startup = `Lueji ${s}`;

  await test.step("registo da startup", async () => {
    await page.goto("/");
    await page.getByRole("link", { name: "Criar conta da startup" }).first().click();
    await page.getByLabel("Nome da startup").fill(startup);
    await page.getByLabel("O seu nome").fill("Fundadora Teste");
    await page.getByLabel("E-mail").fill(fundadora);
    await page.getByLabel("Palavra-passe").fill(PALAVRA);
    await page.getByLabel("Li o aviso de privacidade").check();
    await page.getByRole("button", { name: "Criar conta" }).click();
    await page.waitForURL(/\/s$/);
    await expect(page.getByRole("link", { name: "Pedir o selo à sua aceleradora" })).toBeVisible();
  });

  await test.step("convida um membro da equipa, que aceita", async () => {
    await page.getByRole("link", { name: "Conta", exact: true }).click();
    await page.getByRole("link", { name: "Gerir a equipa" }).click();
    await page.getByLabel("Convidar membro da equipa por e-mail").fill(colega);
    await page.getByRole("button", { name: "Enviar convite" }).click();
    await expect(page.getByText("Convite enviado.")).toBeVisible();
    await context.clearCookies();
    const ligacao = ultimoEmail(colega).match(/https?:\/\/\S+\/equipa\/\S+?\//)![0];
    await page.goto(new URL(ligacao).pathname);
    await expect(page.getByRole("heading", { name: `Equipa da ${startup}` })).toBeVisible();
    await page.getByLabel("O seu nome").fill("Colega Teste");
    await page.getByLabel("Palavra-passe").fill(PALAVRA);
    await page.getByLabel("Li o aviso de privacidade.").check();
    await page.getByRole("button", { name: "Aceitar e criar conta" }).click();
    await page.waitForURL(/\/s$/);
    await page.goto("/s/equipa");
    await expect(page.getByText("Só os fundadores podem convidar")).toBeVisible();
    await context.clearCookies();
  });

  await test.step("a fundadora pede o selo à aceleradora", async () => {
    await entrar(page, fundadora);
    await page.waitForURL(/\/s$/);
    await page.getByRole("link", { name: "Perfil", exact: true }).click();
    await page.getByRole("link", { name: "Gerir selos" }).click();
    await page.getByLabel("Aceleradora ou universidade").selectOption({ label: "Aceleradora Kalandula" });
    await page.getByLabel("Turma em que participou").selectOption({ label: "Programa de Aceleração 2026 · Turma 3 · Mar.–Jun. 2026" });
    await page.getByLabel("Nota para a aceleradora").fill("Demo day em Junho");
    await page.getByRole("button", { name: "Pedir selo" }).click();
    await expect(page.getByText(/Pedido enviado à Aceleradora Kalandula/)).toBeVisible();
    await expect(page.getByText(/^Pendente · Aceleradora Kalandula/)).toBeVisible();
    await context.clearCookies();
  });

  await test.step("a aceleradora vê o pedido com a nota e confirma", async () => {
    await entrar(page, "gestora@kalandula.demo");
    await page.waitForURL(/\/e$/);
    await page.goto("/e/validacoes");
    const item = page.getByRole("listitem").filter({ hasText: startup });
    await expect(item.getByText("Pedido pela startup")).toBeVisible();
    await expect(item.getByText("Demo day em Junho")).toBeVisible();
    await item.getByRole("link", { name: "Ver e decidir" }).click();
    await expect(page.getByText(`«${startup} participou no Programa de Aceleração 2026 · Turma 3 (Mar.–Jun. 2026).»`)).toBeVisible();
    await page.getByRole("button", { name: "Confirmar participação" }).click();
    await page.waitForURL(/\/e\/validacoes$/);
    await context.clearCookies();
  });

  await test.step("a startup vê o selo confirmado", async () => {
    await entrar(page, fundadora);
    await page.waitForURL(/\/s$/);
    await expect(page.getByText("Validado · nível alto")).toBeVisible();
    await expect(page.getByText("Validado por Aceleradora Kalandula", { exact: false })).toBeVisible();
  });

  semErros();
});
