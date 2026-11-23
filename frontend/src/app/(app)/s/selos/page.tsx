import type { Metadata } from "next";
import { Cabecalho, CartaoSinal, Cartao } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import type { Sinal, Turma } from "@/lib/tipos";
import { CancelarPedido } from "./CancelarPedido";
import { PedirSelo } from "./PedirSelo";

export const metadata: Metadata = { title: "Selos" };

export type EntidadeComTurmas = { id: string; nome: string; tipo_rotulo: string; turmas: (Turma & { ja_pedido: boolean })[] };

export default async function Selos() {
  await exigirPapel("startup");
  const d = await api<{ sinais: (Sinal & { nota?: string })[]; entidades: EntidadeComTurmas[] }>("/api/v1/startup/selos");
  return (
    <>
      <Cabecalho titulo="Selos" />
      <main id="conteudo" className="conteudo estreito">
        <Cartao titulo="Pedir o selo à sua aceleradora">
          <p className="muted">A aceleradora confirma que a startup participou na turma. Os investidores vêem o selo com o nome da aceleradora e a data.</p>
          <PedirSelo entidades={d.entidades} />
        </Cartao>
        <section className="pilha" aria-labelledby="t-selos">
          <h2 id="t-selos" className="t-h3">Os seus selos e pedidos</h2>
          {d.sinais.length ? d.sinais.map((s) => (
            <div key={s.id} className="pilha-sm"><CartaoSinal s={s} />{s.estado === "pendente" && <CancelarPedido id={s.id} />}</div>
          )) : <p className="muted">Ainda não pediu nenhum selo.</p>}
          <p className="t-sm muted">Os pedidos pendentes só aparecem para si. Os investidores só vêem os selos confirmados.</p>
        </section>
      </main>
    </>
  );
}
