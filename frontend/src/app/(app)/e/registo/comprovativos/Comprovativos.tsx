"use client";

import Link from "next/link";
import { useState } from "react";
import { ErroTopo } from "@/componentes/Campo";
import { Icone } from "@/componentes/Icone";
import { ErroPedido, pedido } from "@/lib/api-cliente";
import type { Comprovativo } from "@/lib/tipos";

const TIPOS = ["Certidão ou registo comercial", "Comprovativo do NIF", "Evidência de programa realizado", "Outro"];
const tamanho = (b: number) => (b < 1024 * 1024 ? `${Math.round(b / 1024)} KB` : `${(b / 1024 / 1024).toFixed(1).replace(".", ",")} MB`);

export function Comprovativos({ iniciais }: { iniciais: Comprovativo[] }) {
  const [lista, setLista] = useState(iniciais);
  const [descricao, setDescricao] = useState(TIPOS[0]);
  const [ficheiro, setFicheiro] = useState<File | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);

  async function anexar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null);
    if (!ficheiro) return setErro("Escolha um ficheiro.");
    if (ficheiro.size > 2 * 1024 * 1024) return setErro("Erro: o ficheiro tem mais de 2 MB. Reduza-o ou envie outro.");
    const f = new FormData();
    f.append("descricao", descricao);
    f.append("ficheiro", ficheiro);
    setAEnviar(true);
    try {
      const c = await pedido<Comprovativo>("POST", "/api/v1/entidade/comprovativos", f);
      setLista([...lista, c]);
      setFicheiro(null);
      (ev.target as HTMLFormElement).reset();
    } catch (e) { setErro((e as ErroPedido).message); } finally { setAEnviar(false); }
  }

  async function remover(id: string) {
    try { await pedido("DELETE", `/api/v1/entidade/comprovativos/${id}`); setLista(lista.filter((c) => c.id !== id)); }
    catch (e) { setErro((e as ErroPedido).message); }
  }

  return (
    <>
      {lista.length > 0 && (
        <ul className="card lista limpa">
          {lista.map((c) => (
            <li key={c.id} className="entre">
              <div><p className="t-label">{c.descricao}</p><p className="t-sm muted">{c.nome_original} · {tamanho(c.tamanho_bytes)}</p></div>
              <div className="linha">
                <a className="btn btn-ghost" href={`/api/v1/comprovativos/${c.id}/ficheiro`}>Descarregar</a>
                <button className="btn btn-ghost" onClick={() => remover(c.id)}>Remover</button>
              </div>
            </li>
          ))}
        </ul>
      )}
      <form className="card pad-lg pilha" onSubmit={anexar} noValidate>
        <ErroTopo mensagem={erro} />
        <div className="field">
          <label className="label" htmlFor="descricao">Que documento é</label>
          <select id="descricao" className="input" value={descricao} onChange={(e) => setDescricao(e.target.value)}>
            {TIPOS.map((t) => <option key={t}>{t}</option>)}
          </select>
        </div>
        <div className="field">
          <label className="label" htmlFor="ficheiro">Ficheiro</label>
          <input id="ficheiro" className="input" type="file" accept=".pdf,.jpg,.jpeg,.png" aria-describedby="ficheiro-ajuda"
            onChange={(e) => setFicheiro(e.target.files?.[0] ?? null)} />
          <p className="help" id="ficheiro-ajuda">PDF, JPEG ou PNG, até 2 MB.</p>
        </div>
        <div className="linha"><button className="btn btn-secondary" disabled={aEnviar} aria-busy={aEnviar}><Icone nome="mais" /> {aEnviar ? "A anexar…" : "Anexar"}</button></div>
      </form>
      <div className="linha">
        {lista.length
          ? <Link className="btn btn-primary btn-lg btn-movel-cheio" href="/e/registo/submeter">Continuar</Link>
          : <><span className="btn btn-primary btn-lg" aria-disabled="true">Continuar</span><span className="help">Fica activo quando houver pelo menos um comprovativo.</span></>}
      </div>
    </>
  );
}
