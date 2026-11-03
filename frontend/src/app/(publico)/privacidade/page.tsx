import type { Metadata } from "next";

export const metadata: Metadata = { title: "Privacidade e termos" };

export default function Privacidade() {
  return (
    <>
      <h1 className="t-h1">Privacidade e termos</h1>
      <p className="t-sm muted">Versão de 3 de Novembro de 2026. Texto provisório do protótipo académico (TCC, ISPTEC), a rever antes de uso com dados reais.</p>
      <section className="pilha-sm">
        <h2 className="t-h3">Que dados guardamos</h2>
        <p>O seu nome, e-mail e palavra-passe (guardada cifrada, nunca em claro). Para entidades validadoras: nome legal, NIF, site, responsável e os comprovativos enviados para a verificação. Para startups: o nome da startup, as turmas a que pertence e o que decidir pôr no perfil.</p>
      </section>
      <section className="pilha-sm">
        <h2 className="t-h3">Para que servem</h2>
        <p>Para criar e proteger a sua conta, verificar entidades e mostrar aos investidores autenticados os sinais confirmados por elas, sempre com quem confirmou e quando. Não vendemos dados nem os usamos para publicidade.</p>
      </section>
      <section className="pilha-sm">
        <h2 className="t-h3">Quem vê o quê</h2>
        <p>Os comprovativos da entidade só são vistos pela administração da plataforma. A startup decide sempre o que partilha e com quem: nenhum investidor vê contactos ou documentos sem autorização da startup.</p>
      </section>
      <section className="pilha-sm">
        <h2 className="t-h3">Os seus direitos (Lei n.º 22/11)</h2>
        <p>Pode pedir acesso aos seus dados, a rectificação ou a eliminação, e opor-se a comunicações por e-mail. Registamos as acções importantes (verificações, validações, convites) num registo de auditoria que não pode ser alterado.</p>
      </section>
      <section className="pilha-sm">
        <h2 className="t-h3">Segurança</h2>
        <p>Ligações cifradas, palavras-passe com pelo menos 12 caracteres, bloqueio temporário depois de várias tentativas falhadas e autenticação em dois passos opcional (obrigatória para a administração).</p>
      </section>
    </>
  );
}
