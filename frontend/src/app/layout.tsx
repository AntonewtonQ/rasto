import type { Metadata, Viewport } from "next";
import { connection } from "next/server";
import { AvisoRede } from "@/componentes/AvisoRede";
// Fontes alojadas no próprio servidor (guia de marca 5.1; CSP font-src 'self'). Só o subconjunto usado é descarregado.
import "@fontsource-variable/inter";
import "@/estilos/rasto.css";
import "@/estilos/app.css";

export const metadata: Metadata = {
  title: { default: "Rasto", template: "%s · Rasto" },
  description: "Startups aceleradas e investidores em Angola a decidir com a mesma informação.",
};

export const viewport: Viewport = { width: "device-width", initialScale: 1, viewportFit: "cover" };

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  // Todas as páginas são renderizadas a pedido, para cada uma receber a nonce da CSP (ver src/proxy.ts).
  await connection();
  return (
    <html lang="pt-PT">
      <body>
        <a className="saltar link" href="#conteudo">Saltar para o conteúdo</a>
        <AvisoRede />
        {children}
      </body>
    </html>
  );
}
