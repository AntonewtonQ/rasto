import { redirect } from "next/navigation";
import { destinoDoPapel, eu } from "@/lib/api-servidor";

export default async function Inicio() {
  const e = await eu();
  if (!e.autenticado) redirect("/entrar");
  redirect(destinoDoPapel(e.utilizador.papel));
}
