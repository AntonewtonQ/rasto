import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";
import { entrar } from "./ajudas";

// WCAG 2.2 AA (RNF03): nenhuma violação grave ou crítica nos ecrãs do Sprint 1, a 390 e a 1280 px.
async function semViolacoes(page: import("@playwright/test").Page, ecra: string) {
  const r = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  const graves = r.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
  expect(graves.map((v) => `${ecra}: ${v.id} — ${v.help} (${v.nodes.length})`)).toEqual([]);
}

test("ecrãs públicos", async ({ page }) => {
  for (const url of ["/", "/entrar", "/recuperar", "/registo/entidade", "/privacidade"]) {
    await page.goto(url);
    await semViolacoes(page, url);
  }
});

test("ecrãs da entidade", async ({ page }) => {
  await entrar(page, "gestora@kalandula.demo");
  await page.waitForURL(/\/e$/);
  for (const url of ["/e", "/e/turmas", "/e/turmas/nova", "/e/validacoes", "/e/validacoes?ver=historico", "/e/entidade", "/conta"]) {
    await page.goto(url);
    await semViolacoes(page, url);
  }
  await page.goto("/e/turmas");
  await page.getByRole("link", { name: /Programa de Aceleração/ }).first().click();
  await semViolacoes(page, "detalhe da turma");
});

test("ecrãs da startup", async ({ page }) => {
  await entrar(page, "ana@mbote.demo");
  await page.waitForURL(/\/s$/);
  await semViolacoes(page, "/s");
});
