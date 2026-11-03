import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { Icone } from "@/componentes/Icone";
import { Cabecalho, Cartao, EstadoVerificacao } from "@/componentes/Ui";
import { api, exigirPapel } from "@/lib/api-servidor";
import { decil, fmtData, fmtDataExtenso, plural } from "@/lib/formatos";
import type { Contagens, Organizacao, Turma } from "@/lib/tipos";

export const metadata: Metadata = { title: "Início" };

type Espera = { tipo: string; quantidade?: number; startups?: string[]; email?: string; turma_id?: string; prazo: string | null };
type PainelEntidade = { organizacao: Organizacao; turma_activa: (Turma & { contagens: Contagens }) | null; turmas: Turma[]; a_espera: Espera[] };

function EstadoEntidade({ o }: { o: Organizacao }) {
  switch (o.estado_verificacao) {
    case "verificada":
      return <p className="muted">Entidade verificada pela plataforma a {fmtData(o.verificada_em)}. Pode convidar startups e validar participações.</p>;
    case "submetida": case "em_analise":
      return (<>
        <p><strong>Estamos a verificar a {o.nome}.</strong> Prazo indicativo: {fmtDataExtenso(o.prazo_resposta)}.</p>
        <p className="muted">A administração confirma existência legal, presença pública, o responsável e um programa já realizado. Enquanto isso, pode preparar a primeira turma em rascunho. Os convites ficam disponíveis depois da verificação.</p>
      </>);
    case "pedido_info":
      return (<>
        <p><strong>A plataforma pediu mais informação até {fmtDataExtenso(o.prazo_resposta)}:</strong></p>
        <p className="muted pre">{o.motivo}</p>
        <p><Link className="btn btn-primary" href="/e/registo/comprovativos">Responder</Link></p>
      </>);
    case "recusada":
      return (<><p>A verificação foi recusada. Motivo: {o.motivo}</p><p><Link className="btn btn-secondary" href="/e/registo/comprovativos">Corrigir e submeter de novo</Link></p></>);
    case "suspensa":
      return (<><p>A entidade está suspensa. Motivo: {o.motivo}</p><p className="muted">Os sinais que validou mostram um aviso aos investidores e as novas validações estão bloqueadas.</p></>);
    case "expirada":
      return (<><p>O pedido de informação expirou sem resposta. Pode retomar o processo.</p><p><Link className="btn btn-secondary" href="/e/registo/comprovativos">Retomar</Link></p></>);
    default:
      return null;
  }
}

export default async function PainelEntidade() {
  await exigirPapel("entidade");
  const p = await api<PainelEntidade>("/api/v1/entidade/painel");
  const o = p.organizacao;
  if (o.estado_verificacao === "rascunho") redirect((o.passo_registo ?? 2) <= 2 ? "/e/registo/comprovativos" : "/e/registo/submeter");
  const t = p.turma_activa;
  const c = t?.contagens;
  return (
    <>
      <Cabecalho titulo="Início" accoes={<Link className="btn btn-primary" href="/e/turmas/nova"><Icone nome="mais" /><span>Nova turma</span></Link>} />
      <main id="conteudo" className="conteudo">
        <Cartao titulo={o.nome} accao={<EstadoVerificacao estado={o.estado_verificacao} rotulo={o.estado_rotulo} />}>
          <EstadoEntidade o={o} />
        </Cartao>

        {t && c && (
          <section className="pilha" aria-labelledby="turma-activa">
            <div className="entre"><h2 className="t-h3" id="turma-activa">{t.nome} <span className="t-sm muted">· {t.periodo}</span></h2>
              <Link className="link" href={`/e/turmas/${t.id}`}>Ver turma</Link></div>
            <div className="grelha-3">
              <div className="card kpi"><span className="t-caption muted">Convites aceites</span>
                <span className="valor num">{c.aceites}<span className="t-body muted"> de {c.total}</span></span>
                <div className="bar" role="img" aria-label={`${c.aceites} aceites, ${c.pendentes} pendentes, ${c.expirados} expirados`}>
                  <i className={`bar-aceites ${decil(c.total ? (100 * c.aceites) / c.total : 0)}`} />
                  <i className={`bar-pendentes ${decil(c.total ? (100 * c.pendentes) / c.total : 0)}`} />
                </div>
                <span className="t-sm muted">{plural(c.aceites, "aceite")} · {plural(c.pendentes, "pendente")} · {plural(c.expirados, "expirado")}</span>
              </div>
              <div className="card kpi"><span className="t-caption muted">Participações validadas</span><span className="valor num">{c.validados}</span></div>
              <div className="card kpi"><span className="t-caption muted">Perfis publicados</span><span className="valor num">{c.perfis_publicados}</span></div>
            </div>
          </section>
        )}

        <div className="duas">
          <Cartao titulo="À espera de si">
            {p.a_espera.length ? (
              <ul className="lista limpa">
                {p.a_espera.map((x, i) => (
                  <li key={i} className="entre">
                    {x.tipo === "validacoes"
                      ? <><span>{plural(x.quantidade ?? 0, "participação para confirmar", "participações para confirmar")}: {x.startups?.join(", ")}{(x.quantidade ?? 0) > 3 ? "…" : ""}</span>
                        <Link className="btn btn-secondary" href="/e/validacoes">Confirmar</Link></>
                      : <><span>Convite para {x.email} {x.tipo === "convite_expirado" ? "expirou" : "não foi entregue"}</span>
                        <Link className="btn btn-secondary" href={`/e/turmas/${x.turma_id}`}>Resolver</Link></>}
                  </li>
                ))}
              </ul>
            ) : <p className="muted">Nada à espera de si. Quando uma startup aceitar um convite, a participação aparece aqui para confirmar.</p>}
          </Cartao>
          <Cartao titulo="Turmas" accao={<Link className="link" href="/e/turmas">Ver todas</Link>}>
            {p.turmas.length ? (
              <ul className="lista limpa">{p.turmas.map((x) => <li key={x.id}><Link className="link" href={`/e/turmas/${x.id}`}>{x.nome}</Link><span className="t-sm muted">{x.periodo} · {x.estado_rotulo}</span></li>)}</ul>
            ) : (<><p className="muted">Ainda sem turmas.</p><p><Link className="btn btn-primary" href="/e/turmas/nova">Criar a primeira turma</Link></p></>)}
          </Cartao>
        </div>
      </main>
    </>
  );
}
