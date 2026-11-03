import type { Metadata } from "next";
import Link from "next/link";
import { Selo } from "@/componentes/Icone";
import { Aviso, Cabecalho, Cartao, ChipConvite, Voltar } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { fmtData } from "@/lib/formatos";
import type { Contagens, Convite, Turma } from "@/lib/tipos";
import { AccoesConvite } from "./AccoesConvite";

export const metadata: Metadata = { title: "Turma" };

type DetalheTurma = {
  turma: Turma; contagens: Contagens; pode_convidar: boolean; frase_exemplo: string; convites: Convite[];
  startups: { id: string; nome: string; entrou_em: string; participacao: { id: string; estado: string; validado_em: string | null } | null }[];
};

export default async function TurmaDetalhe({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  await exigirPapel("entidade");
  const d = await api<DetalheTurma>(`/api/v1/turmas/${id}`);
  const t = d.turma;
  return (
    <>
      <Cabecalho titulo={t.nome} voltar={<Voltar href="/e/turmas" rotulo="Voltar às turmas" />}
        accoes={d.pode_convidar && <Link className="btn btn-primary" href={`/e/turmas/${t.id}/convidar`}>Convidar startups</Link>} />
      <main id="conteudo" className="conteudo">
        <p className="muted">{t.periodo} · {t.estado_rotulo} · {d.contagens.aceites} de {d.contagens.total} convites aceites · {d.contagens.validados} participações validadas</p>
        {!d.pode_convidar && t.estado === "rascunho" && <Aviso><p>Turma em rascunho. Os convites ficam disponíveis depois da verificação da entidade.</p></Aviso>}

        <Cartao titulo="Startups da turma">
          {d.startups.length ? (
            <ul className="lista limpa">{d.startups.map((s) => (
              <li key={s.id} className="entre"><span className="t-label">{s.nome}</span>
                {s.participacao?.estado === "validado" && <span className="chip chip-primary"><Selo estado="validado" tamanho={16} />Participação validada · {fmtData(s.participacao.validado_em)}</span>}
                {s.participacao?.estado === "pendente" && <Link className="btn btn-secondary" href={`/e/validacoes/${s.participacao.id}`}>Confirmar participação</Link>}
                {s.participacao && !["validado", "pendente"].includes(s.participacao.estado) && <span className="chip chip-neutral">{s.participacao.estado}</span>}
              </li>
            ))}</ul>
          ) : <p className="muted">Ainda nenhuma startup aceitou. Quando aceitarem, aparecem aqui e a participação fica à espera da sua confirmação.</p>}
        </Cartao>

        <Cartao titulo="Convites">
          {d.convites.length ? (
            <ul className="lista limpa">{d.convites.map((c) => (
              <li key={c.id}>
                <div className="entre"><span className="t-label">{c.email}</span><ChipConvite c={c} /></div>
                <span className="t-sm muted">Enviado por {c.canal === "ligacao" ? "ligação" : "e-mail"}{c.enviado_por ? ` por ${c.enviado_por}` : ""} a {fmtData(c.criado_em)}{c.reenvios ? ` · reenviado ${c.reenvios}×` : ""}</span>
                {d.pode_convidar && ["pendente", "expirado", "erro_envio"].includes(c.estado) && <AccoesConvite c={c} />}
              </li>
            ))}</ul>
          ) : (<>
            <p className="muted">Convide as startups desta turma por e-mail ou por uma ligação para enviar no WhatsApp.</p>
            {d.pode_convidar && <p><Link className="btn btn-primary" href={`/e/turmas/${t.id}/convidar`}>Convidar startups</Link></p>}
          </>)}
        </Cartao>
      </main>
    </>
  );
}
