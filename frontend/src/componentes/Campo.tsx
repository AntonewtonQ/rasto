"use client";

import type { InputHTMLAttributes, ReactNode, TextareaHTMLAttributes } from "react";
import { useId } from "react";
import { Icone } from "./Icone";

type Base = { rotulo: string; ajuda?: ReactNode; erros?: string[]; opcional?: boolean };

/** Campo com rótulo visível, ajuda e erro ligados por aria-describedby (especificação 2.4). */
export function Campo({ rotulo, ajuda, erros, opcional, ...props }: Base & InputHTMLAttributes<HTMLInputElement>) {
  const id = useId();
  const desc = [ajuda && `${id}-ajuda`, erros?.length && `${id}-erro`].filter(Boolean).join(" ") || undefined;
  return (
    <div className="field">
      <label className="label" htmlFor={id}>{rotulo}{opcional && <span className="req"> (opcional)</span>}</label>
      <input id={id} className={`input${erros?.length ? " is-error" : ""}${props.readOnly ? " is-readonly" : ""}`}
        aria-describedby={desc} aria-invalid={erros?.length ? true : undefined} {...props} />
      {ajuda && <p className="help" id={`${id}-ajuda`}>{ajuda}</p>}
      {erros?.map((e) => <p key={e} className="err" id={`${id}-erro`}><Icone nome="erro" pequeno /><span>{e.startsWith("Erro") ? e : `Erro: ${e}`}</span></p>)}
    </div>
  );
}

export function AreaTexto({ rotulo, ajuda, erros, opcional, maxLength, value, ...props }:
  Base & TextareaHTMLAttributes<HTMLTextAreaElement>) {
  const id = useId();
  const n = typeof value === "string" ? value.length : 0;
  const desc = [ajuda && `${id}-ajuda`, erros?.length && `${id}-erro`].filter(Boolean).join(" ") || undefined;
  return (
    <div className="field">
      <label className="label" htmlFor={id}>{rotulo}{opcional && <span className="req"> (opcional)</span>}</label>
      <textarea id={id} className={`input${erros?.length ? " is-error" : ""}`} maxLength={maxLength} value={value}
        aria-describedby={desc} aria-invalid={erros?.length ? true : undefined} {...props} />
      {maxLength && <p className="counter" aria-live={n >= 0.9 * maxLength ? "polite" : "off"}>{n}/{maxLength}</p>}
      {ajuda && <p className="help" id={`${id}-ajuda`}>{ajuda}</p>}
      {erros?.map((e) => <p key={e} className="err" id={`${id}-erro`}><Icone nome="erro" pequeno /><span>Erro: {e}</span></p>)}
    </div>
  );
}

export function Caixa({ rotulo, erros, ...props }: { rotulo: ReactNode; erros?: string[] } & InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div className="field">
      <label className="caixa-check"><input type="checkbox" {...props} /><span className="t-body">{rotulo}</span></label>
      {erros?.map((e) => <p key={e} className="err"><Icone nome="erro" pequeno /><span>Erro: {e}</span></p>)}
    </div>
  );
}

export function Opcoes({ legenda, nome, opcoes, valor, aoMudar, erros }:
  { legenda: string; nome: string; opcoes: { valor: string; rotulo: string }[]; valor: string; aoMudar: (v: string) => void; erros?: string[] }) {
  return (
    <fieldset>
      <legend>{legenda}</legend>
      <div className="opcoes">
        {opcoes.map((o) => (
          <label key={o.valor} className="opcao">
            <input type="radio" name={nome} value={o.valor} checked={valor === o.valor} onChange={() => aoMudar(o.valor)} />
            <span>{o.rotulo}</span>
          </label>
        ))}
      </div>
      {erros?.map((e) => <p key={e} className="err"><Icone nome="erro" pequeno /><span>Erro: {e}</span></p>)}
    </fieldset>
  );
}

export function ErroTopo({ mensagem }: { mensagem?: string | null }) {
  if (!mensagem) return null;
  return (
    <div className="aviso aviso-err" role="alert" tabIndex={-1} ref={(el) => el?.focus()}>
      <Icone nome="erro" />
      <div><p>{mensagem.startsWith("Erro") || mensagem.startsWith("Há campos") ? mensagem : `Erro: ${mensagem}`}</p></div>
    </div>
  );
}
