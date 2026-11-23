import type { Metadata } from "next";
import Link from "next/link";
import { Cabecalho, Cartao, Vazio } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData, plural } from "@/lib/formatos";
import type { Mandato, PedidoAcesso } from "@/lib/tipos";

export const metadata: Metadata = { title: "Início" };

const CHIP: Record<string, string> = { pendente: "chip-neutral", aceite: "chip-ok", recusado: "chip-neutral", expirado: "chip-neutral", retirado: "chip-neutral", revogado: "chip-warn" };

export default async function InicioInvestidor() {
  const e = await exigirPapel("investidor");
  const [m, p] = await Promise.all([
    api<{ mandato: Mandato; compativeis: number; publicadas: number }>("/api/v1/investidor/mandato"),
    api<{ pedidos: (PedidoAcesso & { startup: { id: string; nome: string } })[] }>("/api/v1/investidor/pedidos-acesso"),
  ]);
  return (
    <>
      <Cabecalho titulo={`Olá, ${e.utilizador.nome.split(" ")[0] || "investidor"}`} />
      <main id="conteudo" className="conteudo estreito">
        {!m.mandato.minimo_completo ? (
          <Vazio titulo="Comece pelo mandato." accao={<Link className="btn btn-primary" href="/i/mandato">Definir mandato</Link>}>
            Diga que sectores e fases procura. Em menos de um minuto vê as startups que encaixam e porquê.
          </Vazio>
        ) : (
          <Cartao titulo="Sugestões" accao={<Link className="link" href="/i/mandato">Rever mandato</Link>}>
            <div className="kpi"><span className="valor">{m.compativeis}</span>
              <span className="t-sm muted">{m.compativeis === 1 ? "startup compatível" : "startups compatíveis"} de {plural(m.publicadas, "publicada", "publicadas")}</span></div>
            <div><Link className="btn btn-primary" href="/i/sugestoes">Ver sugestões</Link></div>
          </Cartao>
        )}
        <Cartao titulo="Os meus pedidos de acesso">
          {p.pedidos.length === 0 ? <p className="muted">Ainda não pediu acesso a nenhuma startup.</p> : (
            <ul className="lista limpa">{p.pedidos.map((x) => (
              <li key={x.id} className="entre">
                <Link className="link" href={`/i/startups/${x.startup.id}`}>{x.startup.nome}</Link>
                <span className={`chip ${CHIP[x.estado] ?? "chip-neutral"}`}>{x.estado_rotulo}{x.estado === "pendente" ? ` · até ${fmtData(x.expira_em)}` : ""}</span>
              </li>
            ))}</ul>
          )}
        </Cartao>
      </main>
    </>
  );
}
