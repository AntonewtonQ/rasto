import type { Metadata } from "next";
import { Suspense } from "react";
import { FormEntrar } from "./FormEntrar";

export const metadata: Metadata = { title: "Entrar" };

export default function Entrar() {
  return (
    <>
      <div className="trilho" aria-hidden="true" />
      <div className="pilha-sm">
        <h1 className="t-display">Confiança que se verifica.</h1>
        <p className="t-body muted">Entre na sua conta. As startups entram por convite da sua aceleradora ou universidade.</p>
      </div>
      <Suspense fallback={<div className="card pad-lg sk" aria-busy="true" />}>
        <FormEntrar />
      </Suspense>
    </>
  );
}
