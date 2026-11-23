import type { Metadata } from "next";
import Link from "next/link";
import { Selo, Simbolo } from "@/componentes/Icone";
import { eu } from "@/lib/api-servidor";
import "@fontsource/lora/latin-600.css"; // Lora só nas páginas públicas (guia de marca 5.1)
import "@/estilos/entrada.css";
import { Trilho } from "./Trilho";

export const metadata: Metadata = {
  title: { absolute: "Rasto · Confiança que se verifica" },
  description: "Startups aceleradas e investidores em Angola. Cada sinal mostra quem o confirmou e quando.",
};

const PASSOS = [
  { titulo: "A startup cria conta e pede o selo", texto: "À aceleradora em que participou." },
  { titulo: "A aceleradora confirma", texto: "Com o seu nome e a data." },
  { titulo: "O investidor vê o que foi verificado", texto: "Separado do que é declarado." },
];

const PUBLICOS = [
  { titulo: "Startups", texto: "Credibilidade confirmada e os investidores organizados por etapa." },
  { titulo: "Investidores", texto: "Startups do seu mandato, com sinais que pode verificar." },
  { titulo: "Aceleradoras", texto: "As startups da turma visíveis depois do programa." },
];

export default async function Entrada() {
  const e = await eu();
  return (
    <div className="entrada">
      <header className="entrada-topo">
        <div className="entrada-largura entre">
          <Link className="marca" href="/" aria-label="Rasto, página inicial"><Simbolo />rasto</Link>
          {e.autenticado
            ? <Link className="btn btn-primary" href="/inicio">A minha área</Link>
            : <Link className="btn btn-ghost" href="/entrar">Entrar</Link>}
        </div>
      </header>

      <main id="conteudo">
        <section className="entrada-heroi" aria-labelledby="titulo">
          <Trilho className="heroi-fundo" />
          <div className="entrada-largura heroi-grelha">
            <div className="pilha-lg">
              <h1 id="titulo" className="t-display heroi-titulo">Confiança que se verifica.</h1>
              <p className="t-body-lg muted heroi-texto">Startups aceleradas e investidores em Angola. Cada sinal mostra quem o confirmou e quando.</p>
              {!e.autenticado && (
                <div className="heroi-accoes">
                  <Link className="btn btn-primary btn-lg" href="/registo/startup">Criar conta da startup</Link>
                  <Link className="btn btn-secondary btn-lg" href="/registo/entidade">Sou uma aceleradora</Link>
                  <Link className="btn btn-ghost btn-lg" href="/registo/investidor">Sou investidor</Link>
                </div>
              )}
            </div>

            <figure className="heroi-exemplo card pad-lg pilha" aria-label="Exemplo de perfil com dados fictícios">
              <div className="sig sig-val">
                <Selo estado="validado" />
                <div className="pilha-sm">
                  <p className="eyebrow tinta">Validado</p>
                  <p className="t-label">Participou no Programa de Aceleração 2026</p>
                  <p className="t-sm muted">Aceleradora Kalandula · 02/07/2026</p>
                </div>
              </div>
              <div className="sig sig-dec">
                <Selo estado="declarado" />
                <div className="pilha-sm">
                  <p className="eyebrow muted">Declarado</p>
                  <p className="t-label">Primeiro cliente pagante</p>
                  <p className="t-sm muted">Ainda sem validação</p>
                </div>
              </div>
              <figcaption className="t-caption subtle">Exemplo com dados fictícios.</figcaption>
            </figure>
          </div>
        </section>

        <section className="entrada-seccao" aria-labelledby="t-como">
          <div className="entrada-largura pilha-lg">
            <h2 id="t-como" className="t-h2">Como funciona</h2>
            <ol className="passos-cadeia limpa">
              {PASSOS.map((p, i) => (
                <li key={p.titulo} className="passo-cadeia">
                  <span className="passo-numero" aria-hidden="true">{i + 1}</span>
                  <div>
                    <h3 className="t-label passo-titulo">{p.titulo}</h3>
                    <p className="t-sm muted">{p.texto}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="entrada-seccao seccao-rebaixada" aria-labelledby="t-quem">
          <div className="entrada-largura pilha-lg">
            <h2 id="t-quem" className="t-h2">Para quem</h2>
            <ul className="publicos limpa">
              {PUBLICOS.map((p) => (
                <li key={p.titulo} className="publico">
                  <h3 className="t-h3">{p.titulo}</h3>
                  <p className="muted">{p.texto}</p>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="entrada-fecho" aria-labelledby="t-fecho">
          <div className="entrada-largura fecho-conteudo">
            <h2 id="t-fecho" className="t-display fecho-titulo">Mostre quem confirma a sua startup.</h2>
            {!e.autenticado && <Link className="btn btn-lg btn-claro" href="/registo/startup">Criar conta</Link>}
          </div>
        </section>
      </main>

      <footer className="entrada-rodape">
        <div className="entrada-largura entre">
          <p className="t-sm muted">Nada é partilhado sem o consentimento da startup.</p>
          <p className="t-sm muted">Rasto · TCC, ISPTEC · 2026 · <Link className="link" href="/privacidade">Privacidade</Link></p>
        </div>
      </footer>
    </div>
  );
}
