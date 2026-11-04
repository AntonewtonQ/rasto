import { defineConfig, devices } from "@playwright/test";

// Testes ponta a ponta no navegador real. Precisam do Django (porta 8000) e do Next.js (porta 3000) a correr;
// ver frontend/e2e/README.md. PW_CHROMIUM permite usar um Chromium já instalado no aparelho.
export default defineConfig({
  testDir: "./e2e",
  workers: 1,
  timeout: 60_000,
  expect: { timeout: 10_000 },
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:3000",
    locale: "pt-PT",
    trace: "retain-on-failure",
    ignoreHTTPSErrors: !!process.env.IGNORAR_TLS, // pilha local com o certificado interno do Caddy
    launchOptions: process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {},
  },
  projects: [
    { name: "telemovel", use: { ...devices["Desktop Chrome"], viewport: { width: 390, height: 844 } } },
    { name: "computador", use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 860 } }, testMatch: /acessibilidade/ },
  ],
});
