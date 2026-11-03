import type { Metadata } from "next";
import { Aviso, Cabecalho, Voltar } from "@/componentes/Ui";
import { exigirPapel } from "@/lib/api-servidor";
import { FormTurma } from "./FormTurma";

export const metadata: Metadata = { title: "Nova turma" };

export default async function NovaTurma() {
  const e = await exigirPapel("entidade");
  const org = e.organizacao;
  return (
    <>
      <Cabecalho titulo="Nova turma" voltar={<Voltar href="/e/turmas" rotulo="Voltar às turmas" />} />
      <main id="conteudo" className="conteudo estreito">
        {org && org.estado_verificacao !== "verificada" && (
          <Aviso><p>Pode criar a turma em rascunho; os convites ficam disponíveis depois da verificação da {org.nome}.</p></Aviso>
        )}
        <FormTurma entidade={org?.nome ?? "entidade"} />
      </main>
    </>
  );
}
