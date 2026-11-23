// Capturas de ecrã para o Capítulo III, só com os dados fictícios de `semear_demo` (instruções do relatório, secção 6).
// Uso: com o Django e o Next.js a correr sobre uma base semeada só com `semear_demo`:
//   node docs/relatorio/figuras/ecras/capturar.cjs
const path = require("node:path");
const { chromium } = require(path.resolve(__dirname, "../../../../frontend/node_modules/@playwright/test"));

const BASE = process.env.BASE ?? "http://localhost:3000";
const PALAVRA = "demonstracao-rasto-2026";
const SAIDA = __dirname;

const ECRAS = [
  { ficheiro: "e02-validacoes.png", conta: "gestora@kalandula.demo", url: "/e/validacoes" },
  { ficheiro: "s06-pedido.png", conta: "ana@mbote.demo", url: "/s/investidores?ver=pedidos", abrir: "summary",
    elemento: "main article.card" },
  { ficheiro: "s08-pipeline.png", conta: "ana@mbote.demo", url: "/s/investidores", largura: 1440, altura: 860 },
  { ficheiro: "i03-sugestoes.png", conta: "rui@imbondeiro.demo", url: "/i/sugestoes" },
  { ficheiro: "i04-porque.png", conta: "rui@imbondeiro.demo", url: "/i/sugestoes", clicar: "Mbote Pagamentos",
    elemento: "section.card:has(section[aria-label='Porque esta startup'])" },
];

(async () => {
  const browser = await chromium.launch(process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {});
  for (const e of ECRAS) {
    const ctx = await browser.newContext({ viewport: { width: e.largura ?? 390, height: e.altura ?? 844 }, deviceScaleFactor: 2,
      locale: "pt-PT", colorScheme: "light", reducedMotion: "reduce", bypassCSP: true });
    const page = await ctx.newPage();
    await page.goto(`${BASE}/entrar`);
    await page.getByLabel("E-mail").fill(e.conta);
    await page.getByLabel("Palavra-passe").fill(PALAVRA);
    await page.getByRole("button", { name: "Entrar" }).click();
    await page.waitForURL((u) => !u.pathname.startsWith("/entrar"), { waitUntil: "commit" });
    await page.goto(`${BASE}${e.url}`);
    if (e.clicar) await page.getByRole("link", { name: e.clicar }).first().click();
    if (e.abrir) await page.locator(e.abrir).first().click();
    await page.waitForLoadState("networkidle");
    if (e.elemento) {
      // Só o cartão relevante: a página inteira do telemóvel não cabe numa página A4.
      await page.locator(e.elemento).first().screenshot({ path: path.join(SAIDA, e.ficheiro), style: ".nav{display:none!important}" });
      console.log("ok", e.ficheiro);
      await ctx.close();
      continue;
    }
    // Na captura da página inteira, a barra de navegação fixa do telemóvel ficaria a meio da imagem.
    await page.screenshot({ path: path.join(SAIDA, e.ficheiro), fullPage: !!e.inteira, style: e.inteira ? ".nav{display:none!important}" : "" });
    console.log("ok", e.ficheiro);
    await ctx.close();
  }
  await browser.close();
})();
