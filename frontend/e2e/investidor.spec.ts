import { expect, test } from "@playwright/test";
import { PALAVRA, entrar, sufixo, ultimoEmail, vigiarConsola } from "./ajudas";

// Sprint 2 (parte 1): a startup publica o perfil; o investidor define o mandato, vê a sugestão explicada e pede
// acesso; a startup aceita e só então o investidor vê o contacto e os documentos.
test("investidor encontra a startup, pede acesso e a startup aceita", async ({ page, context }) => {
  const s = sufixo();
  const semErros = vigiarConsola(page);
  const fundadora = `fundadora-${s}@startup.test`;
  const investidor = `investidor-${s}@fundo.test`;
  const startup = `Mukua ${s}`;

  await test.step("a startup completa e publica o perfil", async () => {
    await page.goto("/registo/startup");
    await page.getByLabel("Nome da startup").fill(startup);
    await page.getByLabel("O seu nome").fill("Fundadora Teste");
    await page.getByLabel("E-mail").fill(fundadora);
    await page.getByLabel("Palavra-passe").fill(PALAVRA);
    await page.getByLabel("Li o aviso de privacidade").check();
    await page.getByRole("button", { name: "Criar conta" }).click();
    await page.waitForURL(/\/s$/);
    await page.getByRole("link", { name: "Perfil", exact: true }).click();
    await expect(page.getByRole("button", { name: "Publicar" })).toBeDisabled();
    await page.getByLabel("Sector").selectOption({ label: "Agritech" });
    await page.getByLabel("Fase").selectOption({ label: "Seed (Receita recorrente e equipa a crescer)" });
    await page.getByLabel("Província").selectOption({ label: "Luanda" });
    await page.getByLabel("Cidade").fill("Luanda");
    await page.getByLabel("Resumo").fill("Transforma fruta local em sumos para escolas.");
    await page.getByLabel("Contacto do fundador").fill(fundadora);
    await page.getByRole("button", { name: "Guardar", exact: true }).click();
    await expect(page.getByText("Perfil guardado.")).toBeVisible();
    await page.getByLabel("Valor que procura").fill("150000");
    await page.getByLabel("Início da ronda").fill("01/10/2026");
    await page.getByRole("button", { name: "Guardar ronda" }).click();
    await expect(page.getByText("Ronda guardada.")).toBeVisible();
    await page.getByLabel("Título").fill("Apresentação");
    await page.getByLabel("Ligação").fill("https://example.org/apresentacao.pdf");
    await page.getByRole("button", { name: "Juntar documento" }).click();
    await expect(page.getByText("Documento juntado.")).toBeVisible();
    await page.getByRole("button", { name: "Publicar" }).click();
    await expect(page.getByRole("heading", { name: "Publicado" })).toBeVisible();
    await context.clearCookies();
  });

  await test.step("o investidor regista-se e define o mandato", async () => {
    await page.goto("/entrar");
    await page.getByRole("link", { name: "Sou investidor" }).click();
    await page.getByLabel("O seu nome").fill("Investidor Teste");
    await page.getByLabel("E-mail").fill(investidor);
    await page.getByLabel("Palavra-passe").fill(PALAVRA);
    await page.getByLabel("Li o aviso de privacidade").check();
    await page.getByRole("button", { name: "Criar conta" }).click();
    await page.waitForURL(/\/i\/mandato$/);
    await page.getByRole("button", { name: "Agritech" }).click();
    await page.getByRole("button", { name: "Seed", exact: true }).click();
    await page.getByLabel("Mínimo").fill("20000");
    await page.getByLabel("Máximo").fill("60000");
    await page.getByRole("button", { name: "Guardar mandato" }).click();
    await expect(page.getByText(/Mandato guardado\. \d+ startups? compatíve/)).toBeVisible();
  });

  await test.step("vê a sugestão explicada e pede acesso", async () => {
    await page.getByRole("link", { name: "Sugestões", exact: true }).click();
    await page.getByRole("link", { name: startup }).click();
    await expect(page.getByRole("heading", { name: "Porque esta startup" })).toBeVisible();
    await expect(page.getByText("Agritech está no seu mandato.")).toBeVisible();
    await expect(page.getByText(fundadora)).toHaveCount(0);
    await page.getByLabel("Nota para a startup").fill("Invisto em agritech em fase seed.");
    await page.getByRole("button", { name: "Pedir acesso" }).click();
    await expect(page.getByRole("button", { name: "Retirar pedido" })).toBeVisible();
    expect(ultimoEmail(fundadora)).toContain("Invisto em agritech em fase seed.");
    await context.clearCookies();
  });

  await test.step("a startup aceita o pedido", async () => {
    await entrar(page, fundadora);
    await page.waitForURL(/\/s$/);
    await page.getByRole("link", { name: /1 investidor pediu acesso/ }).click();
    await expect(page.getByText("«Invisto em agritech em fase seed.»")).toBeVisible();
    await page.getByRole("button", { name: "Aceitar" }).click();
    await expect(page.getByRole("button", { name: "Retirar acesso" })).toBeVisible();
    await context.clearCookies();
  });

  await test.step("o investidor vê a camada 2", async () => {
    await entrar(page, investidor);
    await page.waitForURL(/\/i$/);
    await page.getByRole("link", { name: startup }).click();
    await expect(page.getByRole("heading", { name: "Acesso concedido" })).toBeVisible();
    await expect(page.getByText(fundadora)).toBeVisible();
    const doc = page.getByRole("link", { name: "Apresentação" });
    await expect(doc).toHaveAttribute("href", /\/api\/v1\/startups\/.+\/documentos\/.+\/abrir$/);
  });

  semErros();
});
