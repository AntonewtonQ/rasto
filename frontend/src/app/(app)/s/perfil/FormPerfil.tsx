"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { AreaTexto, Campo, ErroTopo } from "@/componentes/Campo";
import { Cartao } from "@/componentes/Ui";
import { ErroPedido, pedido, post } from "@/lib/api-cliente";
import { fmtData } from "@/lib/formatos";
import type { Catalogo, Item, PerfilStartup, Ronda } from "@/lib/tipos";

function useEnvio() {
  const router = useRouter();
  const [erro, setErro] = useState<string | null>(null);
  const [campos, setCampos] = useState<Record<string, string[]>>({});
  const [ok, setOk] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);
  async function enviar(f: () => Promise<unknown>, mensagem: string) {
    setErro(null); setCampos({}); setOk(null); setAEnviar(true);
    try { await f(); setOk(mensagem); router.refresh(); return true; }
    catch (e) { setErro((e as ErroPedido).message); setCampos((e as ErroPedido).campos); return false; }
    finally { setAEnviar(false); }
  }
  return { erro, campos, ok, aEnviar, enviar };
}

function Lista({ rotulo, itens, valor, aoMudar, erros }: { rotulo: string; itens: Item[]; valor: string; aoMudar: (v: string) => void; erros?: string[] }) {
  const id = `sel-${rotulo.toLowerCase().replace(/\W+/g, "-")}`;
  return (
    <div className="field">
      <label className="label" htmlFor={id}>{rotulo}</label>
      <select id={id} className="input" value={valor} onChange={(e) => aoMudar(e.target.value)}>
        <option value="">Escolha…</option>
        {itens.map((i) => <option key={i.id} value={i.id}>{i.nome}{i.descricao ? ` (${i.descricao})` : ""}</option>)}
      </select>
      {erros?.map((e) => <p key={e} className="err">Erro: {e}</p>)}
    </div>
  );
}

export function FormPerfil({ perfil, catalogo }: { perfil: PerfilStartup; catalogo: Catalogo }) {
  const [d, setD] = useState({
    nome: perfil.nome, sector: perfil.sector?.id ?? "", fase: perfil.fase?.id ?? "", provincia: perfil.provincia?.id ?? "",
    cidade: perfil.cidade, resumo: perfil.resumo, contacto_fundador: perfil.contacto_fundador ?? "",
  });
  const { erro, campos, ok, aEnviar, enviar } = useEnvio();
  const mudar = (p: Partial<typeof d>) => setD({ ...d, ...p });
  return (
    <Cartao titulo="Dados da startup">
      <form className="pilha" noValidate onSubmit={(ev) => {
        ev.preventDefault();
        enviar(() => pedido("PATCH", "/api/v1/startup/perfil", { ...d, sector: d.sector || null, fase: d.fase || null, provincia: d.provincia || null }), "Perfil guardado.");
      }}>
        <ErroTopo mensagem={erro} />
        <Campo rotulo="Nome" value={d.nome} onChange={(e) => mudar({ nome: e.target.value })} erros={campos.nome} />
        <div className="duas">
          <Lista rotulo="Sector" itens={catalogo.sector} valor={d.sector} aoMudar={(v) => mudar({ sector: v })} erros={campos.sector} />
          <Lista rotulo="Fase" itens={catalogo.fase} valor={d.fase} aoMudar={(v) => mudar({ fase: v })} erros={campos.fase} />
        </div>
        <div className="duas">
          <Lista rotulo="Província" itens={catalogo.geografia.filter((g) => g.codigo !== "AO")} valor={d.provincia} aoMudar={(v) => mudar({ provincia: v })} erros={campos.provincia} />
          <Campo rotulo="Cidade" value={d.cidade} onChange={(e) => mudar({ cidade: e.target.value })} erros={campos.cidade} />
        </div>
        <AreaTexto rotulo="Resumo" rows={3} maxLength={280} value={d.resumo} onChange={(e) => mudar({ resumo: e.target.value })}
          ajuda="O que faz e para quem, numa ou duas frases." erros={campos.resumo} />
        <Campo rotulo="Contacto do fundador" opcional value={d.contacto_fundador} onChange={(e) => mudar({ contacto_fundador: e.target.value })}
          ajuda="E-mail ou telefone. Só o vê quem tiver o pedido de acesso aceite." erros={campos.contacto_fundador} />
        {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
        <div><button className="btn btn-primary" disabled={aEnviar} aria-busy={aEnviar}>{aEnviar ? "A guardar…" : "Guardar"}</button></div>
      </form>
    </Cartao>
  );
}

export function FormRonda({ ronda }: { ronda: Ronda | null }) {
  const [valor, setValor] = useState(ronda?.valor_alvo?.toString() ?? "");
  const [moeda, setMoeda] = useState(ronda?.moeda ?? "USD");
  const [data, setData] = useState(ronda ? fmtData(ronda.data_inicio) : "");
  const { erro, campos, ok, aEnviar, enviar } = useEnvio();
  return (
    <Cartao titulo="Ronda aberta">
      <form className="pilha" noValidate onSubmit={(ev) => {
        ev.preventDefault();
        enviar(() => pedido("PUT", "/api/v1/startup/ronda", { valor_alvo: Number(valor.replace(/\s/g, "")) || null, moeda, data_inicio: data }), "Ronda guardada.");
      }}>
        <ErroTopo mensagem={erro} />
        <div className="duas">
          <Campo rotulo="Valor que procura" inputMode="numeric" value={valor} onChange={(e) => setValor(e.target.value)} erros={campos.valor_alvo} />
          <div className="field">
            <label className="label" htmlFor="moeda-ronda">Moeda</label>
            <select id="moeda-ronda" className="input" value={moeda} onChange={(e) => setMoeda(e.target.value)}>
              <option value="USD">USD</option><option value="AOA">Kz</option>
            </select>
          </div>
        </div>
        <Campo rotulo="Início da ronda" placeholder="dd/mm/aaaa" inputMode="numeric" value={data} onChange={(e) => setData(e.target.value)} erros={campos.data_inicio} />
        {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
        <div><button className="btn btn-secondary" disabled={aEnviar}>Guardar ronda</button></div>
      </form>
    </Cartao>
  );
}

export function Documentos({ documentos }: { documentos: { id: string; titulo: string; url?: string }[] }) {
  const [titulo, setTitulo] = useState("");
  const [url, setUrl] = useState("");
  const { erro, ok, aEnviar, enviar } = useEnvio();
  return (
    <Cartao titulo="Documentos">
      <p className="t-sm muted">Ligações (Drive, Dropbox…) para a apresentação ou as contas. Só as abre quem tiver acesso aceite, e cada abertura fica registada.</p>
      <ErroTopo mensagem={erro} />
      {documentos.length > 0 && (
        <ul className="lista limpa">{documentos.map((d) => (
          <li key={d.id} className="entre">
            <a className="link" href={d.url} target="_blank" rel="noreferrer noopener">{d.titulo}</a>
            <button type="button" className="btn btn-ghost" onClick={() => enviar(() => pedido("DELETE", `/api/v1/startup/documentos/${d.id}`), "Documento removido.")}>Remover</button>
          </li>
        ))}</ul>
      )}
      <form className="pilha" noValidate onSubmit={async (ev) => {
        ev.preventDefault();
        if (await enviar(() => post("/api/v1/startup/documentos", { titulo, url }), "Documento juntado.")) { setTitulo(""); setUrl(""); }
      }}>
        <div className="duas">
          <Campo rotulo="Título" value={titulo} onChange={(e) => setTitulo(e.target.value)} />
          <Campo rotulo="Ligação" type="url" placeholder="https://" value={url} onChange={(e) => setUrl(e.target.value)} />
        </div>
        {ok && <p className="aviso aviso-ok" role="status">{ok}</p>}
        <div><button className="btn btn-secondary" disabled={aEnviar || !titulo.trim() || !url.trim()}>Juntar documento</button></div>
      </form>
    </Cartao>
  );
}

export function Publicacao({ publicado, pronto }: { publicado: boolean; pronto: boolean }) {
  const { erro, aEnviar, enviar } = useEnvio();
  return (
    <div className="pilha-sm">
      <ErroTopo mensagem={erro} />
      {publicado
        ? <button type="button" className="btn btn-secondary" disabled={aEnviar} onClick={() => enviar(() => post("/api/v1/startup/perfil/despublicar"), "")}>Despublicar</button>
        : <button type="button" className="btn btn-primary" disabled={aEnviar || !pronto} onClick={() => enviar(() => post("/api/v1/startup/perfil/publicar"), "")}>Publicar</button>}
    </div>
  );
}
