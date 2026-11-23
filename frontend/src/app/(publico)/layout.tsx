import "@fontsource/lora/latin-600.css"; // Lora só nas páginas públicas (guia de marca 5.1)
import Link from "next/link";
import { Simbolo } from "@/componentes/Icone";

export default function LayoutPublico({ children }: { children: React.ReactNode }) {
  return (
    <div className="publica">
      <main id="conteudo" className="caixa larga">
        <Link className="marca" href="/"><Simbolo />rasto</Link>
        {children}
        <p className="t-sm muted"><Link className="link" href="/privacidade">Privacidade e termos</Link></p>
      </main>
    </div>
  );
}
