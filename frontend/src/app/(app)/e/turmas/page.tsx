import type { Metadata } from "next";
import Link from "next/link";
import { Icone } from "@/componentes/Icone";
import { Cabecalho, Vazio } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { Contagens, Turma } from "@/lib/tipos";

export const metadata: Metadata = { title: "Turmas" };

export default async function Turmas() {
  await exigirPapel("entidade");
  const { turmas } = await api<{ turmas: (Turma & { contagens: Contagens })[] }>("/api/v1/turmas");
  return (
    <>
      <Cabecalho titulo="Turmas" accoes={<Link className="btn btn-primary" href="/e/turmas/nova"><Icone nome="mais" /><span>Nova turma</span></Link>} />
      <main id="conteudo" className="conteudo">
        {turmas.length === 0 ? (
          <Vazio titulo="Ainda sem turmas" accao={<Link className="btn btn-primary" href="/e/turmas/nova">Nova turma</Link>}>Crie a turma do programa para convidar as startups.</Vazio>
        ) : (<>
          <div className="card tbl-wrap so-largo">
            <table className="tbl">
              <thead><tr><th scope="col">Turma</th><th scope="col">Período</th><th scope="col">Estado</th><th scope="col" className="num">Convites aceites</th><th scope="col" className="num">Validadas</th></tr></thead>
              <tbody>{turmas.map((t) => (
                <tr key={t.id}><td><Link className="link" href={`/e/turmas/${t.id}`}>{t.nome}</Link></td><td>{t.periodo}</td><td>{t.estado_rotulo}</td>
                  <td className="num">{t.contagens.aceites} de {t.contagens.total}</td><td className="num">{t.contagens.validados}</td></tr>
              ))}</tbody>
            </table>
          </div>
          <ul className="card lista limpa so-estreito">{turmas.map((t) => (
            <li key={t.id}><Link className="link" href={`/e/turmas/${t.id}`}>{t.nome}</Link>
              <span className="t-sm muted">{t.periodo} · {t.estado_rotulo} · {t.contagens.aceites} de {t.contagens.total} convites aceites</span></li>
          ))}</ul>
        </>)}
      </main>
    </>
  );
}
