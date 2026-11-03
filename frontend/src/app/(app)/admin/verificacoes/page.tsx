import type { Metadata } from "next";
import Link from "next/link";
import { Cabecalho, Vazio } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData } from "@/lib/formatos";
import type { Organizacao } from "@/lib/tipos";

export const metadata: Metadata = { title: "Verificação de entidades" };
const FILTROS: [string, string][] = [["por_decidir", "Por decidir"], ["pedido_info", "À espera da entidade"], ["verificada", "Verificadas"], ["outras", "Recusadas, suspensas e expiradas"]];

export default async function Verificacoes({ searchParams }: { searchParams: Promise<{ estado?: string; q?: string }> }) {
  const { estado = "por_decidir", q = "" } = await searchParams;
  await exigirPapel("admin");
  const d = await api<{ contagens: Record<string, number>; organizacoes: Organizacao[] }>(
    `/api/v1/admin/verificacoes?estado=${encodeURIComponent(estado)}&q=${encodeURIComponent(q)}`);
  return (
    <>
      <Cabecalho titulo="Verificação de entidades" />
      <main id="conteudo" className="conteudo">
        <div className="entre">
          <nav className="separadores" aria-label="Estado">
            {FILTROS.map(([k, r]) => <Link key={k} href={`?estado=${k}`} aria-current={estado === k ? "page" : undefined}>{r} ({d.contagens[k] ?? 0})</Link>)}
          </nav>
          <form className="linha" role="search">
            <input type="hidden" name="estado" value={estado} />
            <label className="sr-only" htmlFor="q">Pesquisar por nome ou NIF</label>
            <input className="input" id="q" name="q" defaultValue={q} placeholder="Nome ou NIF" type="search" />
            <button className="btn btn-secondary">Pesquisar</button>
          </form>
        </div>
        {d.organizacoes.length ? (
          <div className="card tbl-wrap">
            <table className="tbl">
              <thead><tr><th scope="col">Entidade</th><th scope="col">Tipo</th><th scope="col">Estado</th><th scope="col">Submetida</th><th scope="col">Prazo</th></tr></thead>
              <tbody>{d.organizacoes.map((o) => (
                <tr key={o.id}><td><Link className="link" href={`/admin/verificacoes/${o.id}`}>{o.nome_legal}</Link><br /><span className="t-sm muted">NIF {o.nif}</span></td>
                  <td>{o.tipo_rotulo}</td><td>{o.estado_rotulo}</td><td>{fmtData(o.submetida_em)}</td><td>{fmtData(o.prazo_resposta)}</td></tr>
              ))}</tbody>
            </table>
          </div>
        ) : <Vazio titulo="Nenhuma entidade neste estado." />}
      </main>
    </>
  );
}
