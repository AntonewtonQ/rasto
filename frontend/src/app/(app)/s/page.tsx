import type { Metadata } from "next";
import { Icone, Selo } from "@/componentes/Icone";
import { CartaoSinal, Cabecalho, Cartao } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { decil } from "@/lib/formatos";
import type { Sinal } from "@/lib/tipos";

export const metadata: Metadata = { title: "Início" };

type InicioStartup = {
  startup: { id: string; nome: string; estado: string }; completude: number; sinais: Sinal[];
  passos: { texto: string; feito: boolean; selo?: boolean }[];
};

export default async function InicioStartup() {
  await exigirPapel("startup");
  const d = await api<InicioStartup>("/api/v1/startup/inicio");
  return (
    <>
      <Cabecalho titulo={d.startup.nome} />
      <main id="conteudo" className="conteudo estreito">
        <Cartao titulo="Perfil" accao={<span className="chip chip-neutral">{d.startup.estado === "publicado" ? "Publicado" : "Rascunho"}</span>}>
          <p className="t-label">{d.completude}% completo</p>
          <div className="bar bar-pri" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={d.completude} aria-label="Completude do perfil"><i className={decil(d.completude)} /></div>
          <p className="t-sm muted">O perfil fica em rascunho até decidir publicá-lo. Nenhum investidor o vê enquanto estiver em rascunho.</p>
        </Cartao>
        <section className="pilha" aria-labelledby="sinais-t">
          <h2 className="t-h3" id="sinais-t">Sinais</h2>
          {d.sinais.length ? d.sinais.map((s) => <CartaoSinal key={s.id} s={s} />) : <p className="muted">Ainda sem sinais.</p>}
          <p className="t-sm muted">Os sinais pendentes só aparecem para si. Os investidores só vêem os validados (com quem confirmou e quando) e, em secção separada, os declarados.</p>
        </section>
        <Cartao titulo="Próximos passos">
          <ul className="pilha limpa">{d.passos.map((p) => (
            <li key={p.texto} className={`passo${p.feito ? " feito" : ""}`}>
              {p.selo ? <Selo estado="validado" tamanho={20} /> : p.feito ? <span className="marca-passo"><Icone nome="visto" /></span> : <span className="marca-passo" aria-hidden="true" />}
              <p className={p.feito ? "muted" : ""}>{p.texto}{p.feito && <span className="sr-only"> (feito)</span>}</p>
            </li>
          ))}</ul>
        </Cartao>
      </main>
    </>
  );
}
