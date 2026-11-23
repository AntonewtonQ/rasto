import type { Metadata } from "next";
import Link from "next/link";
import { ChipPontuacao, ResumoStartup } from "@/componentes/Compatibilidade";
import { Selo } from "@/componentes/Icone";
import { Cabecalho, Vazio } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { plural } from "@/lib/formatos";
import type { Compatibilidade, PerfilStartup } from "@/lib/tipos";

export const metadata: Metadata = { title: "Sugestões" };

type Cartao = {
  posicao: number; tem_acesso: boolean; compatibilidade: Compatibilidade;
  startup: Pick<PerfilStartup, "id" | "nome" | "sector" | "fase" | "provincia" | "cidade" | "ronda" | "verificados">;
};
type Resposta = { mandato_incompleto: boolean; publicadas: number; compativeis?: number; sugestoes: Cartao[] };

export default async function Sugestoes({ searchParams }: { searchParams: Promise<{ parciais?: string }> }) {
  await exigirPapel("investidor");
  const parciais = (await searchParams).parciais === "1";
  const d = await api<Resposta>(`/api/v1/investidor/sugestoes${parciais ? "?parciais=1" : ""}`);
  return (
    <>
      <Cabecalho titulo="Sugestões" />
      <main id="conteudo" className="conteudo estreito">
        {d.mandato_incompleto ? (
          <Vazio titulo="Defina primeiro o seu mandato." accao={<Link className="btn btn-primary" href="/i/mandato">Definir mandato</Link>}>
            Com pelo menos um sector e uma fase, ordenamos as startups publicadas e explicamos porque cada uma aparece.
          </Vazio>
        ) : (<>
          <div className="entre">
            <p className="muted">{plural(d.compativeis ?? 0, "compatível", "compatíveis")} de {plural(d.publicadas, "startup publicada", "startups publicadas")}.</p>
            <nav className="separadores" aria-label="Filtro">
              <Link href="/i/sugestoes" aria-current={!parciais ? "page" : undefined}>Compatíveis</Link>
              <Link href="/i/sugestoes?parciais=1" aria-current={parciais ? "page" : undefined}>Incluir parciais</Link>
            </nav>
          </div>
          {d.sugestoes.length === 0 ? (
            <Vazio titulo="Nenhuma startup encaixa agora."
              accao={<Link className="btn btn-secondary" href={parciais ? "/i/mandato" : "/i/sugestoes?parciais=1"}>{parciais ? "Rever mandato" : "Ver as parciais"}</Link>}>
              Não inventamos encaixes: só aparecem startups com perfil publicado que cumprem o seu mandato.
            </Vazio>
          ) : (
            <ol className="pilha limpa">
              {d.sugestoes.map((c) => (
                <li key={c.startup.id} className="card pad-lg pilha-sm">
                  <div className="entre">
                    <h2 className="t-h3"><Link className="link" href={`/i/startups/${c.startup.id}?origem=sugestao&posicao=${c.posicao}`}>{c.startup.nome}</Link></h2>
                    <ChipPontuacao c={c.compatibilidade} />
                  </div>
                  <ResumoStartup p={c.startup} />
                  {c.startup.verificados.length > 0 && (
                    <p className="linha-sm t-sm"><Selo estado="validado" tamanho={16} />
                      {c.startup.verificados.map((s) => s.validador?.nome).filter(Boolean).join(", ")}</p>
                  )}
                  <ul className="limpa t-sm muted">
                    {c.compatibilidade.criterios.filter((x) => x.peso > 0).slice(0, 3).map((x) => <li key={x.chave}>{x.frase}</li>)}
                  </ul>
                  {c.tem_acesso && <p><span className="chip chip-ok">Tem acesso</span></p>}
                </li>
              ))}
            </ol>
          )}
          <p className="t-sm muted">A pontuação mede o encaixe com o seu mandato, não a qualidade da startup.</p>
        </>)}
      </main>
    </>
  );
}
