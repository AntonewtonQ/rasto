import type { Metadata } from "next";
import { Cabecalho, Cartao } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData } from "@/lib/formatos";
import type { Actualizacao, Metrica } from "@/lib/tipos";
import { ListaMetricas } from "@/componentes/Metricas";
import { FormActualizacao } from "./FormActualizacao";

export const metadata: Metadata = { title: "Actualizações" };

export type DadosActualizacoes = {
  publicadas: Actualizacao[]; rascunho: Actualizacao | null; modelo: Metrica[]; destinatarios: number;
  periodo_sugerido: string; perfil_publicado: boolean;
};

export default async function Actualizacoes() {
  await exigirPapel("startup");
  const d = await api<DadosActualizacoes>("/api/v1/startup/actualizacoes");
  return (
    <>
      <Cabecalho titulo="Actualizações" />
      <main id="conteudo" className="conteudo estreito">
        <FormActualizacao d={d} />
        <section className="pilha" aria-labelledby="pub-t">
          <h2 className="t-h3" id="pub-t">Publicadas</h2>
          {d.publicadas.length === 0 ? <p className="muted">Ainda sem actualizações publicadas.</p> : d.publicadas.map((a) => (
            <Cartao key={a.id} titulo={a.corrige ? `Correcção à actualização de ${a.corrige.mes}` : a.mes}>
              <p className="t-sm subtle">Publicada a {fmtData(a.publicada_em)}</p>
              <ListaMetricas m={a.metricas} />
              {a.destaques && <p>{a.destaques}</p>}
              {a.pedidos_ajuda && <p className="t-sm"><strong>Onde precisamos de ajuda:</strong> {a.pedidos_ajuda}</p>}
              {!!a.falhas_envio?.length && <p className="aviso aviso-warn" role="status">Não receberam o e-mail: {a.falhas_envio.join(", ")}. Vêem a actualização no Rasto.</p>}
            </Cartao>
          ))}
        </section>
      </main>
    </>
  );
}
