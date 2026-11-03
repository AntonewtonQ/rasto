"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Icone, type NomeIcone, Simbolo } from "./Icone";

export type Destino = { rotulo: string; href: string; icone: NomeIcone; contador?: number };

/** Navegação por papel (C-00): barra inferior < 768, calha 768–1279, barra lateral ≥ 1280. Máximo de 5 destinos. */
export function Navegacao({ destinos }: { destinos: Destino[] }) {
  const caminho = usePathname();
  const raizes = new Set(["/e", "/s", "/i"]);
  return (
    <nav className="nav" aria-label="Navegação principal">
      <Link className="marca-nav marca" href="/inicio" aria-label="Rasto, início"><Simbolo /><span className="so-largo">rasto</span></Link>
      {destinos.map((d) => {
        const actual = caminho === d.href || (!raizes.has(d.href) && caminho.startsWith(`${d.href}/`));
        return (
          <Link key={d.href} href={d.href} aria-current={actual ? "page" : undefined}>
            <Icone nome={d.icone} /><span>{d.rotulo}</span>
            {!!d.contador && <span className="contador" aria-label={`${d.contador} pendentes`}>{d.contador}</span>}
          </Link>
        );
      })}
    </nav>
  );
}
