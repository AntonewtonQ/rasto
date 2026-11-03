# Registo de decisões e sincronizações do relatório

Formato: data · decisão · justificação (dado: inquérito, literatura, entrevista; ou **suposição**) · secção do relatório.

## Decisões anteriores ao desenvolvimento
- 2026-11-03 · Nome definitivo: Rasto · decisão do autor · capa, Introdução.
- 2026-11-03 · Comparações em texto chamam-se «Quadro»; dados numéricos, «Tabela» · ABNT/IBGE · todo o relatório.
- 2026-11-03 · Âmbito: ligação e acompanhamento; documentos por ligação externa; cofre de documentos é trabalho futuro · *data room* em último lugar no inquérito (45,8%, P14) apesar de 79,2% o acharem útil isoladamente (P13a) · Cap. II 2.3.6, Quadro 4; Trabalhos futuros.
- 2026-11-03 · Compatibilidade por regras explicáveis, pesos configuráveis (40/25/25/10, risco 0) · poucos dados no ecossistema; explicação faz parte da confiança; Lei 22/11 art. 29.º (decisões automatizadas); pesos a validar nas entrevistas · Cap. I 1.4.3; Cap. III.
- 2026-11-03 · Desenvolvimento começa pela autenticação com papéis e pelo módulo da aceleradora · base dos outros módulos e arranque da plataforma com turmas de startups · Cap. II 2.2, Tabela 2.
- 2026-11-03 · A plataforma não movimenta dinheiro · escopo do MVP; 3 respostas do inquérito sobre pagamentos ficam fora do âmbito (P17) · Introdução; Quadro 1; Quadro 4.
- 2026-11-03 · Entrega do TCC marcada para 15/11/2026; plano de *sprints* comprimido (3 *sprints* de 2 a 4 dias + avaliação a 12–13/11) · decisão do autor · Cap. II 2.2.2, Tabela 2 (períodos a preencher quando cada *sprint* fechar); base técnica v1.2, secção 10.
- 2026-11-03 · Autenticação com papéis e módulo da aceleradora juntos no Sprint 1 (a Tabela 2 aprovada separava-os) · pedido do autor na base técnica; o módulo da aceleradora é a porta de entrada das startups · Cap. II Tabela 2.
- 2026-11-03 · *Stack*: Django 5.2 LTS + HTMX + PostgreSQL 16, monólito modular, Docker Compose · comparação ponderada de 3 opções (base técnica 1.2): produtividade de uma pessoa, segurança por omissão, custo · Cap. III (arquitectura), Cap. VI.
- 2026-11-03 · Ficam fora do MVP entregue, salvo se sobrar tempo: Kanban com arrastar, actualizações periódicas, lembretes por e-mail, sincronização sem rede, API JSON, exportação e eliminação pelo titular · **suposição** de capacidade face ao prazo de 15/11 · Conclusões («Trabalhos futuros»); Cap. III (estado da implementação).
- 2026-11-03 · CSS próprio com os componentes dos *wireframes* em vez do Tailwind (desvio à ADR-11 da base técnica) · prazo de 15/11: evita um passo de compilação; o CSS dos componentes já estava escrito e ligado aos tokens · Cap. III (interface), Cap. VI.
- 2026-11-03 · CSP sem `unsafe-inline` nem estilos em linha; larguras das barras em classes de 10% · OWASP A03; base técnica 7.4 · Cap. V.
- 2026-11-03 · Fonte Inter não alojada no Sprint 1 (a interface usa a pilha de recurso `system-ui`); Google Fonts retirado por causa da CSP e da Lei n.º 22/11 · guia de marca 5.1 · Cap. III (identidade visual) — **pendente**: alojar o subconjunto latino da Inter.
- 2026-11-03 · Sem *webhook* do fornecedor de e-mail no Sprint 1: o «erro de envio» do convite vem das falhas do envio SMTP (3 tentativas) · **suposição** de que basta para o MVP · Cap. III; Cap. VI.
- 2026-11-03 · Lembretes por e-mail (convite ao 7.º dia, validação aos 7 dias) não implementados; os prazos expiram · corte face ao prazo · Trabalhos futuros.
- 2026-11-03 · Entrega adiada para 30/11/2026; voltam ao âmbito a API JSON, os lembretes por e-mail, as actualizações periódicas e o Kanban · decisão do autor · Cap. II Tabela 2; Cap. III; base técnica v1.3, secção 10. (Substitui a entrada de 15/11.)
- 2026-11-03 · *Stack* final: **Next.js no *frontend*, Django REST no *backend*, PostgreSQL**; mesma origem com Caddy, sessões por *cookie* e CSRF, allauth *headless* para entrada e 2FA · decisão do autor; justificação e consequências na base técnica 1.5 e ADR-02 revista · Cap. III (arquitectura, tecnologias), Cap. V, Cap. VI. (Substitui a entrada «Django + HTMX».)
- 2026-11-03 · Interface HTML do Django retirada; o Django passa a servir só a API, a autenticação *headless*, a saúde e o admin interno · consequência da *stack* final · Cap. III (arquitectura).
- 2026-11-03 · Next.js 16 sem `cacheComponents` (modelo de cache anterior) · todas as páginas são autenticadas e dinâmicas; o novo modelo obrigaria a `<Suspense>` em cada leitura da sessão sem ganho · Cap. III (tecnologias).
- 2026-11-03 · Activar a 2FA e ver os códigos de recuperação exige confirmar a palavra-passe (reautenticação do allauth) · protecção contra uso de uma sessão deixada aberta · Cap. V.
- 2026-11-03 · CSP estrita também no Next.js: *nonce* por pedido gerada em `frontend/src/proxy.ts`, sem `unsafe-inline`; todas as páginas renderizadas a pedido para receberem a *nonce* · OWASP A03 · Cap. V.
- 2026-11-03 · Esquema OpenAPI incompleto (vistas sem serializadores de resposta); avisos do drf-spectacular silenciados · **pendente** do Sprint 2: anotar e gerar tipos TypeScript · Cap. III.
- 2026-11-03 · Repositório reorganizado em `backend/`, `frontend/`, `docs/` (produto, marca, técnica, relatório) e `infra/`, com `compose.yml` na raiz · pedido do autor; legibilidade do repositório · Cap. III (implementação), Cap. VI.
- 2026-11-03 · Lembretes por e-mail ao 7.º dia para convites e pedidos de validação, idempotentes (`LembreteEnviado`); convite por e-mail recebe ligação nova (o token antigo só existe como *hash*), convite por ligação avisa a entidade · base de UX 5.0; HU06 · Cap. III, Cap. V.
- 2026-11-03 · Equipa da entidade (E-09): só o responsável convida e retira membros; a entidade nunca fica sem responsável; o membro retirado fica com a conta desactivada e o nome mantém-se na auditoria · **suposição** (a base de UX não define quem gere a equipa) · Cap. III, Cap. V.

## Sincronizações
- 2026-11-03 · Relatório gerado com pré-textuais, Introdução e Capítulos I e II · commit: {{ainda sem código}}
