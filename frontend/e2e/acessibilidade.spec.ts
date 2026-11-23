import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";
import { PALAVRA, django, entrar } from "./ajudas";

// WCAG 2.2 AA (RNF03): nenhuma violação grave ou crítica nos ecrãs do Sprint 1, a 390 e a 1280 px.
async function semViolacoes(page: import("@playwright/test").Page, ecra: string) {
  const r = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  const graves = r.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
  expect(graves.map((v) => `${ecra}: ${v.id} — ${v.help} (${v.nodes.length})`)).toEqual([]);
}

test("ecrãs públicos", async ({ page }) => {
  for (const url of ["/", "/entrar", "/recuperar", "/registo/entidade", "/registo/startup", "/registo/investidor", "/privacidade"]) {
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
  // Garante cartões no pipeline (Kanban a 1280, grupos no telemóvel), mesmo numa base anterior ao Sprint 2.
  django(`from rasto.pipeline import services as p
from rasto.contas.models import Utilizador as U
from rasto.startups.models import startup_do_utilizador as s
u = U.objects.get(email='ana@mbote.demo')
if not p.relacoes_do_utilizador(u).exists():
    p.adicionar_externo(utilizador=u, startup=s(u), nome='Paulo Afonso', organizacao='Clube de Investidores')`);
  await entrar(page, "ana@mbote.demo");
  await page.waitForURL(/\/s$/);
  for (const url of ["/s", "/s/perfil", "/s/investidores", "/s/investidores?ver=pedidos", "/s/actualizacoes", "/s/selos"]) {
    await page.goto(url);
    await semViolacoes(page, url);
  }
  await page.goto("/s/investidores");
  await page.getByRole("button", { name: /^Mover / }).first().click();
  await semViolacoes(page, "pipeline com a folha Mover aberta");
  await page.getByRole("link", { name: "Paulo Afonso" }).first().click();
  await semViolacoes(page, "detalhe da relação");
});

test("ecrãs do investidor", async ({ page }) => {
  // Conta de investidor fictícia (a mesma do semear_demo), criada se a base de dados for anterior ao Sprint 2.
  django(`from rasto.investidores import services as s
from rasto.catalogo.models import ItemCatalogo as I
from rasto.contas.models import Utilizador as U
if not U.objects.filter(email='rui@imbondeiro.demo').exists():
    u, _ = s.registar_investidor(email='rui@imbondeiro.demo', palavra_passe='${PALAVRA}', nome='Rui Gaspar', tipo='anjo')
    s.guardar_mandato(utilizador=u, sectores=list(I.objects.filter(tipo='sector', codigo__in=['agritech', 'fintech']).values_list('id', flat=True)),
                      fases=list(I.objects.filter(tipo='fase', codigo__in=['pre_seed', 'seed']).values_list('id', flat=True)), geografias=[])`);
  await entrar(page, "rui@imbondeiro.demo");
  await page.waitForURL(/\/i$/);
  for (const url of ["/i", "/i/mandato", "/i/sugestoes", "/i/sugestoes?parciais=1", "/i/pipeline"]) {
    await page.goto(url);
    await semViolacoes(page, url);
  }
  const primeira = page.getByRole("listitem").getByRole("link").first();
  if (await primeira.count()) {
    await primeira.click();
    await semViolacoes(page, "perfil da startup (investidor)");
  }
});
