// Ilustração «pontos e trilho» (guia de marca 7.2): pontos numa grelha (tinta) e uma linha contínua que passa entre
// eles (laterite), a mesma gramática do símbolo — registos ligados. Decorativa; menos de 5 KB.
// Inspirada nos desenhos de linha contínua sobre pontos, sem reproduzir nenhum desenho tradicional.

const COLUNAS = 9;
const LINHAS = 5;
const PASSO = 40;

export function Trilho({ className = "" }: { className?: string }) {
  const pontos = [];
  for (let l = 0; l < LINHAS; l++)
    for (let c = 0; c < COLUNAS; c++)
      pontos.push(<circle key={`${l}-${c}`} cx={20 + c * PASSO} cy={20 + l * PASSO} r={c === 7 && l === 1 ? 6 : 3} />);
  return (
    <svg className={`trilho-svg ${className}`} viewBox="0 0 360 200" aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMid slice">
      <g className="trilho-pontos">{pontos}</g>
      <path className="trilho-linha" fill="none" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"
        d="M20 140 C 40 160, 60 160, 80 140 S 120 100, 140 120 S 180 180, 200 140 S 220 60, 260 80 S 300 100, 300 60" />
    </svg>
  );
}
