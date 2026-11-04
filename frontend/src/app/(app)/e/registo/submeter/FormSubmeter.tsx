"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { AreaTexto, Campo, ErroTopo } from "@/componentes/Campo";
import { ErroPedido, post } from "@/lib/api-cliente";
import { fmtHora } from "@/lib/formatos";
import { useRascunho } from "@/lib/rascunho";
import type { Organizacao } from "@/lib/tipos";

export function FormSubmeter({ o }: { o: Organizacao }) {
  const router = useRouter();
  const { dados: d, mudar: m, guardadoAs, limpar } = useRascunho("registo-entidade-3", {
    nome_publico: o.nome_publico ?? "", responsavel_nome: o.responsavel_nome ?? "", responsavel_cargo: o.responsavel_cargo ?? "",
    responsavel_email: o.responsavel_email ?? "", descricao_programa: o.descricao_programa ?? "",
  });
  const [campos, setCampos] = useState<Record<string, string[]>>({});
  const [erro, setErro] = useState<string | null>(null);
  const [aEnviar, setAEnviar] = useState(false);
  const mudar = (k: keyof typeof d) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => m({ [k]: e.target.value });

  async function enviar(ev: React.FormEvent) {
    ev.preventDefault();
    setErro(null); setCampos({}); setAEnviar(true);
    try {
      await post("/api/v1/entidade/submeter", d);
      limpar();
      router.push("/e");
      router.refresh();
    } catch (e) { setErro((e as ErroPedido).message); setCampos((e as ErroPedido).campos); } finally { setAEnviar(false); }
  }

  return (
    <form className="card pad-lg pilha" onSubmit={enviar} noValidate>
      <ErroTopo mensagem={erro} />
      <Campo rotulo="Nome que os investidores vão ver" opcional value={d.nome_publico} onChange={mudar("nome_publico")} ajuda="Se ficar vazio, usamos o nome legal." erros={campos.nome_publico} />
      <Campo rotulo="Nome do responsável" autoComplete="name" value={d.responsavel_nome} onChange={mudar("responsavel_nome")} erros={campos.responsavel_nome} />
      <Campo rotulo="Cargo" opcional value={d.responsavel_cargo} onChange={mudar("responsavel_cargo")} erros={campos.responsavel_cargo} />
      <Campo rotulo="E-mail institucional do responsável" type="email" value={d.responsavel_email} onChange={mudar("responsavel_email")} erros={campos.responsavel_email} />
      <AreaTexto rotulo="Programas ou turmas já realizados" rows={4} maxLength={600} value={d.descricao_programa} onChange={mudar("descricao_programa")}
        ajuda="Ex.: Programa de Aceleração 2025, 12 startups, Março a Junho." erros={campos.descricao_programa} />
      {guardadoAs && <p className="help">Rascunho guardado neste aparelho às {fmtHora(guardadoAs)}.</p>}
      <div className="linha">
        <Link className="btn btn-ghost" href="/e/registo/comprovativos">Voltar</Link>
        <button className="btn btn-primary btn-lg btn-movel-cheio" disabled={aEnviar} aria-busy={aEnviar}>{aEnviar ? "A enviar…" : "Enviar para verificação"}</button>
      </div>
    </form>
  );
}
