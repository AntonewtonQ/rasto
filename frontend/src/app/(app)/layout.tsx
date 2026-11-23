import { redirect } from "next/navigation";
import { type Destino, Navegacao } from "@/componentes/Navegacao";
import { eu } from "@/lib/api-servidor";

// Destinos por papel (base de UX 4.3–4.6): no máximo 5. Os selos da startup estão no Perfil (S4b).
function destinos(papel: string, contadores: Record<string, number>): Destino[] {
  switch (papel) {
    case "entidade":
      return [
        { rotulo: "Início", href: "/e", icone: "casa" },
        { rotulo: "Turmas", href: "/e/turmas", icone: "turmas" },
        { rotulo: "Validações", href: "/e/validacoes", icone: "selo", contador: contadores.validacoes_pendentes },
        { rotulo: "Entidade", href: "/e/entidade", icone: "documento" },
        { rotulo: "Conta", href: "/conta", icone: "pessoa" },
      ];
    case "startup":
      return [
        { rotulo: "Início", href: "/s", icone: "casa" },
        { rotulo: "Investidores", href: "/s/investidores", icone: "investidores", contador: contadores.pedidos_pendentes },
        { rotulo: "Actualizações", href: "/s/actualizacoes", icone: "sino" },
        { rotulo: "Perfil", href: "/s/perfil", icone: "documento" },
        { rotulo: "Conta", href: "/conta", icone: "pessoa" },
      ];
    case "investidor":
      return [
        { rotulo: "Início", href: "/i", icone: "casa" },
        { rotulo: "Sugestões", href: "/i/sugestoes", icone: "procurar" },
        { rotulo: "Pipeline", href: "/i/pipeline", icone: "investidores" },
        { rotulo: "Mandato", href: "/i/mandato", icone: "documento" },
        { rotulo: "Conta", href: "/conta", icone: "pessoa" },
      ];
    default:
      return [
        { rotulo: "Verificações", href: "/admin/verificacoes", icone: "selo" },
        { rotulo: "Conta", href: "/conta", icone: "pessoa" },
      ];
  }
}

export default async function LayoutApp({ children }: { children: React.ReactNode }) {
  const e = await eu();
  if (!e.autenticado) redirect("/entrar");
  return (
    <div className="app">
      <Navegacao destinos={destinos(e.utilizador.papel, e.contadores)} />
      <div className="app-main">{children}</div>
    </div>
  );
}
