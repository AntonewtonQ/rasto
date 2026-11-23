import type { Metadata } from "next";
import { Decomposicao, ResumoStartup } from "@/componentes/Compatibilidade";
import { Cabecalho, CartaoSinal, Cartao, Voltar } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData } from "@/lib/formatos";
import type { Compatibilidade, PedidoAcesso, PerfilStartup } from "@/lib/tipos";
import { PedirAcesso, RetirarPedido } from "./PedirAcesso";

export const metadata: Metadata = { title: "Startup" };

type Resposta = { perfil: PerfilStartup; compatibilidade: Compatibilidade | null; pedido: PedidoAcesso | null; novo_pedido_a_partir_de: string | null };

export default async function PerfilStartupInvestidor({ params, searchParams }:
  { params: Promise<{ id: string }>; searchParams: Promise<{ origem?: string; posicao?: string }> }) {
  await exigirPapel("investidor");
  const { id } = await params;
  const q = await searchParams;
  const d = await api<Resposta>(`/api/v1/startups/${id}`);
  const p = d.perfil;
  const pendente = d.pedido?.estado === "pendente";
  return (
    <>
      <Cabecalho titulo={p.nome} voltar={<Voltar href="/i/sugestoes" rotulo="Voltar às sugestões" />} />
      <main id="conteudo" className="conteudo estreito">
        <section className="pilha-sm">
          <ResumoStartup p={p} />
          <p className="t-body-lg">{p.resumo}</p>
          <p className="t-sm subtle">Perfil actualizado a {fmtData(p.actualizado_em)}</p>
        </section>

        <section className="pilha" aria-labelledby="verif-t">
          <h2 className="t-h3" id="verif-t">Verificado</h2>
          {p.verificados.length ? p.verificados.map((s) => <CartaoSinal key={s.id} s={s} />)
            : <p className="muted">Ainda sem sinais validados por entidades verificadas.</p>}
        </section>
        {p.declarados.length > 0 && (
          <section className="pilha" aria-labelledby="decl-t">
            <h2 className="t-h3" id="decl-t">Declarado pela startup</h2>
            <p className="t-sm muted">Ninguém confirmou estes dados.</p>
            {p.declarados.map((s) => <CartaoSinal key={s.id} s={s} />)}
          </section>
        )}

        {d.compatibilidade && <Cartao><Decomposicao c={d.compatibilidade} /></Cartao>}

        {p.camada === 2 ? (
          <Cartao titulo="Acesso concedido">
            <p><span className="t-label">Contacto do fundador:</span> {p.contacto_fundador || "Não indicado"}</p>
            {p.documentos?.length ? (
              <ul className="lista limpa">{p.documentos.map((doc) => (
                <li key={doc.id}><a className="link" href={`/api/v1/startups/${p.id}/documentos/${doc.id}/abrir`} target="_blank" rel="noreferrer noopener">{doc.titulo}</a></li>
              ))}</ul>
            ) : <p className="muted">A startup ainda não juntou documentos.</p>}
            <p className="t-sm muted">Cada abertura de documento fica registada. A startup pode retirar o acesso quando quiser.</p>
          </Cartao>
        ) : (
          <Cartao titulo="Conhecer melhor">
            {pendente && d.pedido ? (<>
              <p>Pedido enviado a {fmtData(d.pedido.criado_em)}. A startup tem até {fmtData(d.pedido.expira_em)} para responder.</p>
              <p className="copiavel">«{d.pedido.nota}»</p>
              <RetirarPedido id={d.pedido.id} />
            </>) : d.novo_pedido_a_partir_de ? (<>
              <p>{d.pedido?.estado === "expirado" ? "O pedido expirou sem resposta." : "A startup não aceitou o pedido desta vez."}
                {d.pedido?.motivo && <> Motivo: {d.pedido.motivo}.</>}</p>
              <p className="muted">Pode voltar a pedir a partir de {fmtData(d.novo_pedido_a_partir_de)}.</p>
            </>) : (
              <PedirAcesso id={p.id} origem={q.origem === "sugestao" ? "sugestao" : "perfil"} posicao={q.posicao} />
            )}
          </Cartao>
        )}
      </main>
    </>
  );
}
