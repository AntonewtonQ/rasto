import type { Metadata, Viewport } from "next";
import "@/estilos/rasto.css";
import "@/estilos/app.css";

export const metadata: Metadata = {
  title: { default: "Rasto", template: "%s · Rasto" },
  description: "Startups aceleradas e investidores em Angola a decidir com a mesma informação.",
};

export const viewport: Viewport = { width: "device-width", initialScale: 1, viewportFit: "cover" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-PT">
      <body>
        <a className="saltar link" href="#conteudo">Saltar para o conteúdo</a>
        {children}
      </body>
    </html>
  );
}
