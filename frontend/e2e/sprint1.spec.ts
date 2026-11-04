import { expect, test } from "@playwright/test";
import { PALAVRA, criarAdministracao, entrar, sufixo, totp, ultimoEmail, vigiarConsola } from "./ajudas";

// Fluxo do Sprint 1 (especificação de interface, secção 8): registo da entidade → verificação pela administração
// (com 2FA) → turma → convite → a startup aceita → validação em lote → a startup vê o selo.
test("fluxo completo da aceleradora", async ({ page, context }) => {
  const s = sufixo();
  const semErros = vigiarConsola(page);
  const entidade = `Incubadora ${s}, Lda`;
  const gestora = `rosa-${s}@incubadora.test`;

  await test.step("registo da entidade em 3 passos", async () => {
    await page.goto("/registo/entidade");
    await page.getByLabel("Aceleradora ou incubadora").check();
    await page.getByLabel("Nome legal").fill(entidade);
    await page.getByLabel("NIF").fill(`5${String(parseInt(s, 16)).padStart(9, "0")}`);
    await page.getByLabel("O seu nome").fill("Rosa Teste");
    await page.getByLabel("E-mail institucional").fill(gestora);
    await page.getByLabel("Palavra-passe").fill(PALAVRA);
    await page.getByLabel("Li o aviso de privacidade").check();
    await page.getByRole("button", { name: "Continuar para os comprovativos" }).click();
    await page.waitForURL("**/e/registo/comprovativos");
    await page.setInputFiles("#ficheiro", { name: "certidao.pdf", mimeType: "application/pdf", buffer: Buffer.from("%PDF-1.4 teste") });
    await page.getByRole("button", { name: "Anexar" }).click();
    await expect(page.getByText("certidao.pdf")).toBeVisible();
    await page.getByRole("link", { name: "Continuar" }).click();
    await page.getByLabel("Programas ou turmas já realizados").fill("Programa 2025, 8 startups");
    await page.getByRole("button", { name: "Enviar para verificação" }).click();
    await page.waitForURL(/\/e$/);
    await expect(page.getByText("Estamos a verificar")).toBeVisible();
  });

  await test.step("turma em rascunho antes da verificação", async () => {
    await page.goto("/e/turmas/nova");
    await page.getByLabel("Programa", { exact: true }).fill("Programa de Aceleração");
    await page.getByLabel("Edição").fill("2026 · Turma 1");
    await page.getByRole("textbox", { name: "Início" }).fill("02/03/2026");
    await page.getByRole("textbox", { name: "Fim" }).fill("26/06/2026");
    await expect(page.getByText("participou no Programa de Aceleração 2026 · Turma 1 (Mar.–Jun. 2026)")).toBeVisible();
    await page.getByRole("button", { name: "Criar turma" }).click();
    await expect(page.getByText("Turma em rascunho")).toBeVisible();
    await context.clearCookies();
  });

  const admin = `admin-${s}@rasto.test`;
  let segredo = "";
  await test.step("a administração activa a 2FA e verifica a entidade", async () => {
    criarAdministracao(admin);
    await entrar(page, admin);
    await page.waitForURL("**/conta/2fa");
    segredo = await page.getByLabel("Segredo (para escrever à mão)").inputValue();
    await page.getByLabel("Código da aplicação").fill(totp(segredo));
    await page.getByLabel("Palavra-passe").fill(PALAVRA);
    await page.getByRole("button", { name: "Activar" }).click();
    await expect(page.getByText("Autenticação em dois passos activa.")).toBeVisible();
    await page.goto(`/admin/verificacoes?q=${encodeURIComponent(entidade)}`);
    await page.getByRole("link", { name: entidade }).click();
    for (const c of ["Existência legal", "Presença pública", "Responsável identificado", "Programa realizado"])
      await page.getByRole("group", { name: new RegExp(c) }).getByLabel("Cumpre", { exact: true }).check();
    await page.getByRole("button", { name: "Verificar entidade" }).click();
    await expect(page.getByText("Decisão registada.")).toBeVisible();
    await context.clearCookies();
  });

  await test.step("entrada com 2FA pede o código", async () => {
    await entrar(page, admin);
    await page.getByLabel("Código").fill(totp(segredo));
    await page.getByRole("button", { name: "Confirmar código" }).click();
    await page.waitForURL("**/admin/verificacoes");
    await context.clearCookies();
  });

  const fundador = `fundador-${s}@startup.test`;
  await test.step("a entidade convida por e-mail com verificação linha a linha", async () => {
    await entrar(page, gestora);
    await page.waitForURL(/\/e$/);
    await page.getByRole("link", { name: "Ver turma" }).click();
    await page.getByRole("link", { name: "Convidar startups" }).first().click();
    await page.getByLabel("E-mails das startups").fill(`${fundador}\nmau-email`);
    await page.getByRole("button", { name: "Verificar e-mails" }).click();
    await expect(page.getByText("Erro: formato de e-mail inválido. Não é enviado.")).toBeVisible();
    await page.getByRole("button", { name: "Enviar 1 convite" }).click();
    await page.waitForURL(/\/e\/turmas\/[0-9a-f-]+$/);
    await context.clearCookies();
  });

  await test.step("a startup aceita e cria conta", async () => {
    const ligacao = ultimoEmail(fundador).match(/https?:\/\/\S+\/convite\/\S+?\//)![0];
    await page.goto(new URL(ligacao).pathname);
    await expect(page.getByText(`Incubadora ${s}`).first()).toBeVisible();
    await page.getByLabel("O seu nome").fill("Fundador Teste");
    await page.getByLabel("Nome da startup").fill(`Lueji ${s}`);
    await page.getByLabel("Palavra-passe").fill(PALAVRA);
    await page.getByLabel("Li o aviso de privacidade").check();
    await page.getByRole("button", { name: "Aceitar e criar conta" }).click();
    await page.waitForURL(/\/s$/);
    await expect(page.getByText(/^Pendente · /)).toBeVisible();
    await context.clearCookies();
  });

  await test.step("a entidade valida em lote e a startup vê o selo", async () => {
    await entrar(page, gestora);
    await page.waitForURL(/\/e$/);
    await page.goto("/e/validacoes");
    await page.getByLabel(`Lueji ${s}`).check();
    await page.getByRole("button", { name: "Validar 1 participação" }).click();
    await expect(page.getByLabel(`Lueji ${s}`)).toHaveCount(0);
    await context.clearCookies();
    await entrar(page, fundador);
    await page.waitForURL(/\/s$/);
    await expect(page.getByText("Validado · nível alto")).toBeVisible();
  });

  semErros();
});
