import Link from "next/link";
import type { ReactNode } from "react";
import { fmtData } from "@/lib/formatos";
import type { Convite, Sinal } from "@/lib/tipos";
import { Icone, Selo } from "./Icone";

export function Aviso({ tipo = "info", titulo, children, alerta = false }:
  { tipo?: "info" | "warn" | "err" | "ok"; titulo?: string; children?: ReactNode; alerta?: boolean }) {
  const icone = tipo === "err" ? "erro" : tipo === "warn" ? "aviso" : tipo === "ok" ? "visto" : "info";
  return (
    <div className={`aviso aviso-${tipo}`} role={alerta ? "alert" : "status"} tabIndex={alerta ? -1 : undefined}>
      <Icone nome={icone} />
      <div>{titulo && <p><strong>{titulo}</strong></p>}{children}</div>
    </div>
  );
}

export function Cartao({ children, titulo, accao, className = "" }:
  { children: ReactNode; titulo?: string; accao?: ReactNode; className?: string }) {
  return (
    <section className={`card pad-lg pilha ${className}`}>
      {(titulo || accao) && <div className="entre">{titulo && <h2 className="t-h3">{titulo}</h2>}{accao}</div>}
      {children}
    </section>
  );
}

export function Vazio({ titulo, children, accao }: { titulo: string; children?: ReactNode; accao?: ReactNode }) {
  return (
    <div className="card pad-lg pilha-sm">
      <h2 className="t-h3">{titulo}</h2>
      {children && <p className="muted">{children}</p>}
      {accao && <div>{accao}</div>}
    </div>
  );
}

export function ChipConvite({ c }: { c: Convite }) {
  switch (c.estado) {
    case "pendente": return <span className="chip chip-neutral"><Icone nome="relogio" pequeno />Pendente · até {fmtData(c.expira_em)}</span>;
    case "aceite": return <span className="chip chip-ok"><Icone nome="visto" pequeno />Aceite{c.aceite_em ? ` a ${fmtData(c.aceite_em)}` : ""}</span>;
    case "expirado": return <span className="chip chip-neutral">Expirado a {fmtData(c.expira_em)}</span>;
    case "erro_envio": return <span className="chip chip-err"><Icone nome="erro" pequeno />Erro de envio</span>;
    case "recusado": return <span className="chip chip-neutral">Recusado pela startup</span>;
    default: return <span className="chip chip-neutral">{c.estado_rotulo}</span>;
  }
}

export function EstadoVerificacao({ estado, rotulo }: { estado: string; rotulo: string }) {
  if (estado === "verificada") return <span className="chip chip-primary"><Selo estado="validado" tamanho={16} />Entidade verificada</span>;
  if (estado === "suspensa") return <span className="chip chip-warn"><Icone nome="aviso" pequeno />Suspensa</span>;
  if (estado === "recusada") return <span className="chip chip-err"><Icone nome="erro" pequeno />Recusada</span>;
  if (estado === "pedido_info") return <span className="chip chip-warn"><Icone nome="aviso" pequeno />Falta informação</span>;
  return <span className="chip chip-neutral"><Icone nome="relogio" pequeno />{rotulo}</span>;
}

/** Cartão de sinal (guia de marca 6.4): validado com carimbo tinta; o resto tracejado e neutro. */
export function CartaoSinal({ s }: { s: Sinal }) {
  const e = s.estado;
  const validado = e === "validado" || e === "validado_com_aviso";
  const rotulo = {
    validado: "Validado · nível alto", validado_com_aviso: "Validado · a entidade está suspensa",
    pendente: `Pendente · ${s.validador?.nome ?? ""} até ${fmtData(s.expira_em)}`, recusado: "Não validado",
    retirado: `Validação retirada a ${fmtData(s.actualizado_em)}`, expirado: "Pedido de validação expirado",
  }[e] ?? "Declarado";
  return (
    <article className={`sig ${validado ? "sig-val" : "sig-dec"}`}>
      <Selo estado={e} />
      <div className="pilha-sm">
        <p className={`eyebrow ${validado ? "tinta" : "muted"}`}>{rotulo}</p>
        <p className="t-label">{s.descricao}</p>
        {validado && s.validador && <>
          <p className="t-sm muted">Validado por <strong>{s.validador.nome}</strong> · {fmtData(s.validado_em)}</p>
          <p className="t-sm subtle">Entidade verificada pela plataforma{s.validador.verificada_em ? ` a ${fmtData(s.validador.verificada_em)}` : ""}</p>
        </>}
        {e === "recusado" && s.motivo && <p className="t-sm muted">Motivo indicado por {s.validador?.nome}: {s.motivo}</p>}
      </div>
    </article>
  );
}

export function Voltar({ href, rotulo }: { href: string; rotulo: string }) {
  return <Link className="btn btn-ghost btn-icon" href={href} aria-label={rotulo}><Icone nome="voltar" /></Link>;
}

export function Cabecalho({ titulo, voltar, accoes }: { titulo: string; voltar?: ReactNode; accoes?: ReactNode }) {
  return (
    <header className="app-head">
      <div className="linha">{voltar}<h1>{titulo}</h1></div>
      <div className="linha">{accoes}</div>
    </header>
  );
}
