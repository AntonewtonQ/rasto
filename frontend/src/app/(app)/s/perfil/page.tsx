import type { Metadata } from "next";
import { ResumoStartup } from "@/componentes/Compatibilidade";
import { Cabecalho, CartaoSinal, Cartao } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { decil } from "@/lib/formatos";
import type { Catalogo, PerfilStartup } from "@/lib/tipos";
import { Documentos, FormPerfil, FormRonda, Publicacao } from "./FormPerfil";

export const metadata: Metadata = { title: "Perfil" };

export type DadosPerfil = { perfil: PerfilStartup; completude: number; em_falta: string[] };

export default async function PaginaPerfil() {
  await exigirPapel("startup");
  const [d, catalogo] = await Promise.all([api<DadosPerfil>("/api/v1/startup/perfil"), api<Catalogo>("/api/v1/catalogo")]);
  const p = d.perfil;
  return (
    <>
      <Cabecalho titulo="Perfil" />
      <main id="conteudo" className="conteudo estreito">
        <Cartao titulo={p.estado === "publicado" ? "Publicado" : "Rascunho"} accao={<Publicacao publicado={p.estado === "publicado"} pronto={!d.em_falta.length} />}>
          <p className="t-label">{d.completude}% completo</p>
          <div className="bar bar-pri" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={d.completude} aria-label="Completude do perfil"><i className={decil(d.completude)} /></div>
          {d.em_falta.length ? <p className="t-sm">Para publicar, falta: {d.em_falta.join(", ")}.</p>
            : p.estado === "publicado" ? <p className="t-sm muted">Os investidores com mandato compatível vêem o resumo abaixo. Os documentos e o contacto só depois de aceitar um pedido.</p>
              : <p className="t-sm muted">Pronto a publicar. Nenhum investidor o vê enquanto estiver em rascunho.</p>}
        </Cartao>
        <FormPerfil perfil={p} catalogo={catalogo} />
        <FormRonda ronda={p.ronda} />
        <Documentos documentos={p.documentos ?? []} />
        <Cartao titulo="Como o investidor vê (antes de aceitar)">
          <div className="pilha-sm">
            <p className="t-h3">{p.nome}</p>
            <ResumoStartup p={p} />
            <p>{p.resumo || <span className="muted">Sem resumo.</span>}</p>
          </div>
          {p.verificados.map((s) => <CartaoSinal key={s.id} s={s} />)}
          <p className="t-sm muted">Não aparecem: contacto do fundador, documentos e sinais por validar.</p>
        </Cartao>
      </main>
    </>
  );
}
