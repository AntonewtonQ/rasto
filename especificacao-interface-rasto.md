# Especificação de interface · Rasto (nome provisório)

**Versão:** 1.0 · 3 de Novembro de 2026
**Autor:** Antonewton Emanuel Lungoge Quima
**Âmbito:** TCC de Engenharia Informática, ISPTEC
**Entradas usadas:** `base-ux-plataforma.md` v1.0 (comportamento), `guia-de-marca-rasto.md` v1.0 (forma), `rasto.css` e `rasto.tokens.json` v1.0 (tokens).
**Entregáveis:** este documento e `wireframes-rasto.html` (HTML estático com Tailwind, ligado só aos tokens; cada quadro tem o mesmo código que a lista de ecrãs, ex.: E-07).

---

## 0. Convenções

| Marca | Significado |
|---|---|
| **[D]** | Dado do inquérito (Fev. 2026, n = 24) ou fonte citada no contexto. |
| **[S]** | Suposição deste documento. |
| **[H-nn] / [H-Bnn]** | Hipóteses da base de UX e do guia de marca. |
| **[H-Inn]** | Hipótese de interface, nova (secção 6). |
| **[Dec-n]** | Decisão em aberto da base de UX. **[Dec-In]**: decisão de interface, nova (secção 6.2). |
| **P0 / P1 / P2** | Prioridades da base de UX, secção 13. |

Regra de precedência (igual à do guia de marca): **a base de UX decide o comportamento, o guia de marca decide a forma, este documento decide a composição.** Onde as entradas se contradizem, assinalo e sigo a base de UX (0.2).

### 0.1 Hipótese de dispositivo [H-I01] e onde a apliquei

> **[H-I01] [S]:** as startups usam mais o telemóvel; investidores, aceleradoras e administração usam mais o computador.
> Sustentação parcial: contexto "telemóvel primeiro, redes lentas"; persona Nádia (Android de gama média, dados pré-pagos); base de UX 4.1 (administração pode ser optimizada para computador). Para investidores e aceleradoras não há dado: n = 3 e n = 2.

Todos os ecrãs funcionam a 360 px (requisito). A hipótese só decide **qual tamanho se desenha primeiro** e onde se aceita uma vista mais densa no computador.

| Papel | Desenhado primeiro a | Onde a hipótese pesa | Se a hipótese cair |
|---|---|---|---|
| Startup | 360 | Pipeline em lista por etapa no telemóvel (Kanban só ≥ 1280); actualização e decisão de pedido como ecrãs de coluna única. | Nada muda: o computador já tem Kanban. |
| Investidor | 1280 (análise) · 360 (pedido, notificações) | Sugestões com painel "Porque esta startup" ao lado (≥ 1280); relações em tabela. | No telemóvel o painel "Porque" já abre como ecrã próprio; a tabela vira lista de cartões. |
| Entidade | 1280 (painel, fila) · 360 (turma, convites) | Fila de validação em tabela com selecção em lote; painel com 3 indicadores lado a lado. | Fila vira lista de cartões com selecção; já especificado (E-07, telemóvel). |
| Administração | 1280 | Processo de verificação em três colunas. Não se desenha versão de telemóvel dedicada (só tem de ser utilizável). | Baixo risco: 1 a 2 pessoas [S]. |

Como validar: perguntar o aparelho em cada sessão de teste (base de UX 9.3 já pede o telemóvel do participante) e, depois do lançamento, registar a largura de ecrã por papel (dado agregado, sem identificar pessoas).

### 0.2 Inconsistências encontradas nas entradas

| # | Onde | O quê | O que fiz |
|---|---|---|---|
| 1 | Guia de marca 1.5 vs base de UX 8.0 e guia 5.4 | Exemplo "15 000 000 Kz" (moeda depois) contra a regra "Kz 45 000 000" (moeda antes). | Segui a regra: **moeda antes do valor**. A corrigir no guia de marca. |
| 2 | Guia de marca 8.2 vs base de UX 5.6 | O cartão de perfil do guia mostra a % da ronda comprometida na camada 1; a base de UX põe indicadores na camada 2. | Segui a base de UX: a camada 1 mostra **só o valor da ronda**. Decisão [Dec-I1]. |
| 3 | Guia de marca 8 e 9 | Os SVG de `sinais/` e `logo/` não estão no projecto. | Os wireframes usam aproximações desenhadas a partir da descrição (6.2–6.3). Substituir pelos ficheiros oficiais. |
| 4 | Tokens | Não há tokens de pontos de quebra, grelha, camadas (z-index) nem alturas de componentes. | Proponho-os em 2.2, a acrescentar ao `rasto.tokens.json`. |
| 5 | Contexto vs base de UX | O contexto fala em selo "acelerada por X"; a base de UX usa a frase "Participou no {Programa} {Edição}". | Segui a base de UX (diz exactamente o que foi confirmado). |

---

## 1. Inventário de ecrãs

Ordem de desenvolvimento definida no contexto: autenticação e módulo da aceleradora, depois startup, investidor e administração. A verificação de entidades (D-01, D-02) sobe para o Sprint 1 porque sem ela a aceleradora não pode convidar nem validar (base de UX 5.2).

Rotas propostas [S] para a engenharia; o prefixo indica o papel.

### 1.1 Comum (Sprint 1)

| ID | Ecrã | Rota | Prioridade | Dispositivo alvo | Wireframe |
|---|---|---|---|---|---|
| C-00 | Concha da aplicação (navegação por papel, aviso de rede, notificações temporárias) | — | P0 | todos | todos os quadros |
| C-01 | Entrar | `/entrar` | P0 | 360 | sim |
| C-02 | Recuperar palavra-passe (pedir ligação · definir nova) | `/recuperar`, `/recuperar/:token` | P0 | 360 | — (padrão de formulário de C-01) |
| C-03 | Aceitar convite | `/convite/:token` | P0 | 360 | sim, com 5 estados |
| C-04 | Privacidade e termos | `/privacidade` | P0 | 360 | — (página de texto) |
| C-05 | Centro de notificações | `/notificacoes` | P1 | 360 | — |
| C-06 | Erro global e página não encontrada | — | P0 | todos | estado em Componentes |

### 1.2 Entidade validadora (Sprint 1)

| ID | Ecrã | Rota | Prioridade | Dispositivo alvo | Wireframe |
|---|---|---|---|---|---|
| E-01 | Registo da entidade (3 passos: entidade · comprovativos · responsável) | `/registo/entidade` | P0 | 360 | passo 2 |
| E-02 | Início (estado da verificação + resumo da turma + "À espera de si") | `/e` | P0 | 1280 | sim, com 6 estados |
| E-03 | Turmas (lista) | `/e/turmas` | P0 | 1280 | tabela em E-02 |
| E-04 | Nova turma | `/e/turmas/nova` | P0 | 360 | sim |
| E-05 | Turma (startups, convites, estado) | `/e/turmas/:id` | P0 | 1280 | lista de convites em E-06 |
| E-06 | Convidar startups (e-mail · ligação) | `/e/turmas/:id/convidar` | P0 | 360 | sim |
| E-07 | Validações (pendentes · histórico) | `/e/validacoes` | P0 | 1280 | sim |
| E-08 | Confirmar ou recusar validação (folha/diálogo) | sobre E-07 | P0 | 360 e 1280 | E-08 e E-08b |
| E-09 | Entidade (perfil verificado, membros da equipa) | `/e/entidade` | P1 | 1280 | — |
| E-10 | Conta (notificações, privacidade e dados) | `/e/conta` | P1 | 360 | — |

### 1.3 Administração (Sprint 1 para verificação; resto P1/P2)

| ID | Ecrã | Rota | Prioridade | Wireframe |
|---|---|---|---|---|
| D-01 | Verificação de entidades (lista) | `/admin/verificacoes` | P0 | coluna central de D-02 |
| D-02 | Processo de verificação | `/admin/verificacoes/:id` | P0 | sim |
| D-03 | Compatibilidade: pesos, pré-visualização, versões | `/admin/compatibilidade` | P1 | — |
| D-04 | Campos do mandato (sectores, fases, geografias, risco) | `/admin/campos` | P1 | — |
| D-05 | Parâmetros (prazos, taxa de câmbio de referência) | `/admin/parametros` | P1 | — |
| D-06 | Utilizadores (inclui aprovação de investidores, se [Dec-1] = b) | `/admin/utilizadores` | P2 (P1 se Dec-1 = b) | — |
| D-07 | Pedidos de titulares de dados (Lei 22/11) | `/admin/titulares` | P2 | — |
| D-08 | Auditoria | `/admin/auditoria` | P2 | — |
| D-09 | Saúde da plataforma | `/admin/saude` | P2 | — |

Todos os ecrãs da administração: 1280, barra lateral, utilizáveis a 360 sem versão dedicada.

### 1.4 Startup (Sprints 2 e 3)

| ID | Ecrã | Rota | Prioridade | Dispositivo | Wireframe |
|---|---|---|---|---|---|
| S-01 | Início no arranque: lista de passos, completude, métricas sugeridas | `/s` | P1 | 360 | sim |
| S-02 | Editar perfil (passos: dados · ronda · resumo · métricas · documentos) | `/s/perfil/editar` | P1 | 360 | — (padrão E-01) |
| S-03 | Sinais (declarar marco, pedir validação, estados) | `/s/perfil/sinais` | P1 | 360 | cartões em Componentes |
| S-04 | Ver como investidor (camadas 1 e 2) | `/s/perfil/ver` | P1 | 360 | sim |
| S-05 | Pedidos de acesso (pendentes, histórico) | `/s/investidores/pedidos` | P1 | 360 | estados ao lado de S-06 |
| S-06 | Decidir pedido de acesso | `/s/investidores/pedidos/:id` | P1 | 360 | sim |
| S-07 | Investidores com acesso · revogar | `/s/perfil/acessos` | P1 | 360 | — |
| S-08 | Pipeline (lista por etapa · Kanban) | `/s/investidores` | P2 | 360 e 1280 | sim, as duas |
| S-09 | Relação (histórico, notas, soft commit) | `/s/investidores/:id` | P2 | 360 | — |
| S-10 | Adicionar investidor de fora | `/s/investidores/novo` | P2 | 360 | — |
| S-11 | Actualizações (lista) | `/s/actualizacoes` | P2 | 360 | — |
| S-12 | Nova actualização | `/s/actualizacoes/nova` | P2 | 360 | sim |
| S-13 | Indicadores da ronda (Início depois do arranque) | `/s` | P2 | 360 e 1280 | 1280 |
| S-14 | Conta (equipa, notificações, privacidade e dados) | `/s/conta` | P1 | 360 | — |

### 1.5 Investidor (Sprints 2 e 3)

| ID | Ecrã | Rota | Prioridade | Dispositivo | Wireframe |
|---|---|---|---|---|---|
| I-01 | Registo do investidor | `/registo/investidor` | P1 | 360 | — (padrão E-01) |
| I-02 | Mandato | `/i/mandato` | P1 | 360 e 1280 | 360 |
| I-03 | Sugestões + "Porque esta startup" | `/i/sugestoes` | P1 | 1280 | sim |
| I-04 | Perfil da startup, camada 1 (e camada 2 com acesso) | `/i/startups/:id` | P1 | 360 | igual a S-04 + compatibilidade |
| I-05 | Pedir acesso com nota | `/i/startups/:id/pedir` | P1 | 360 | sim, com 3 estados |
| I-06 | Início (pedidos pendentes, actualizações, lembretes) | `/i` | P1 | 360 | — |
| I-07 | Pipeline e acompanhamento (Kanban · lista) | `/i/pipeline` | P2 | 1280 | lista |
| I-08 | Relação (camada 2, documentos, histórico) | `/i/pipeline/:id` | P2 | 1280 | — |
| I-09 | Actualizações recebidas | `/i/actualizacoes` | P2 | 360 | — |
| I-10 | Conta e perfil do investidor | `/i/conta` | P1 | 360 | — |

---

## 2. Design system

### 2.1 Fundações

**Pontos de quebra** (pedido: 360, 768, 1280). Desenha-se a 360; 360 é a largura mínima suportada, não um ponto de quebra de CSS.

| Faixa | Colunas | Margem lateral | Espaço entre colunas | Navegação | Largura máxima do conteúdo |
|---|---|---|---|---|---|
| 360–767 | 4 | 16 (`space-4`) | 16 (`space-4`) | Barra inferior, 5 destinos, 56 de altura | — |
| 768–1279 (`md`) | 8 | 24 (`space-6`) | 16 (`space-4`) | Calha lateral de 80 com ícone e rótulo | — |
| ≥ 1280 (`lg`) | 12 | 32 (`space-8`) | 24 (`space-6`) | Barra lateral de 232 | 1200 (formulários: 640) |

Regras:
- Margens laterais com `max(16px, env(safe-area-inset-left))` para telemóveis com recorte.
- A barra inferior no telemóvel é fixa; o conteúdo tem `padding-bottom` igual à sua altura para nunca tapar o foco (WCAG 2.4.11).
- Formulários longos nunca passam de 640 de largura, mesmo a 1280 (linhas legíveis, perto de 65 caracteres).
- A 768 o Kanban continua em lista por etapa; só a 1280 há colunas (7 colunas × 140 mínimo cabem a partir de ~1100 de conteúdo).

**Espaçamento:** só a escala `space-*` dos tokens (4, 8, 12, 16, 20, 24, 32, 40, 48, 64). Uso: 4–8 dentro de componentes; 12–16 entre elementos de um cartão; 24 entre blocos; 32–48 entre secções. Grupos de irmãos com `gap`, nunca margens individuais.

**Raio:** `radius-sm` 4 (chips de código, esqueletos), `radius-md` 8 (botões, campos, cartões de sinal), `radius-lg` 12 (cartões), `radius-pill` (chips). Folha inferior: 16 nos cantos de cima [S, token novo].

**Elevação:** só `shadow-1`, e só em elementos que flutuam (folha, menu, notificação temporária). Cartões em superfície usam contorno `border`, não sombra (menos pintura em aparelhos lentos).

**Tipografia:** escala do guia (5.3) sem alterações. Mapeamento: título de ecrã `h1` (computador) / `h2` no cabeçalho de telemóvel; secção `h3`; corpo `body`; metadados `body-sm`; estado do sinal `caption` em maiúsculas; indicadores `metric-lg` e `metric` sempre com `.num`. Lora só em C-01 (título) e páginas públicas. Campos nunca abaixo de 16 px.

**Movimento:** 120–200 ms, só para cor e opacidade em hover/pressão e para a folha a entrar. Nada depende de animação: sem animação o estado final aparece de imediato (`prefers-reduced-motion` desliga tudo). Esqueletos estáticos, sem brilho.

### 2.2 Tokens novos propostos (para o guia de marca)

| Token | Valor | Porquê |
|---|---|---|
| `breakpoint.md` / `breakpoint.lg` | 768 / 1280 px | Pedido do Kima; hoje só existem no CSS deste documento. |
| `grid.columns.sm/md/lg` | 4 / 8 / 12 | Grelha 2.1. |
| `grid.margin.sm/md/lg` | `{space.4}` / `{space.6}` / `{space.8}` | Grelha 2.1. |
| `size.control` / `size.control-lg` | 44 / 48 px | Botões e campos; 44 já existe como `touch-target`. |
| `size.nav-bottom` / `size.nav-side` / `size.nav-rail` | 56 / 232 / 80 px | Concha da aplicação. |
| `radius.sheet` | 16 px | Folha inferior. |
| `z.nav` / `z.sheet` / `z.toast` | 10 / 30 / 40 | Ordem de sobreposição previsível. |
| `delay.skeleton` | 300 ms | Esqueleto só aparece se a espera passar deste valor (evita piscar). |

### 2.3 Configuração Tailwind (para a engenharia)

Tailwind só lê variáveis CSS; nunca hexadecimais. Em produção usar a CLI do Tailwind (CSS compilado e purgado), **não** o script de CDN dos wireframes.

```js
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{html,js,ts,jsx,tsx}'],
  theme: {
    screens: { md: '768px', lg: '1280px' },
    extend: {
      colors: {
        bg: 'var(--color-bg)', surface: 'var(--color-surface)', sunken: 'var(--color-surface-sunken)',
        line: 'var(--color-border)', 'line-strong': 'var(--color-border-strong)',
        ink: 'var(--color-text)', muted: 'var(--color-text-muted)', subtle: 'var(--color-text-subtle)',
        primary: { DEFAULT: 'var(--color-primary)', hover: 'var(--color-primary-hover)', subtle: 'var(--color-primary-subtle)', on: 'var(--color-on-primary)' },
        laterite: { DEFAULT: 'var(--color-secondary)', subtle: 'var(--color-secondary-subtle)', on: 'var(--color-on-secondary)' },
        success: { DEFAULT: 'var(--color-success)', subtle: 'var(--color-success-subtle)' },
        warning: { DEFAULT: 'var(--color-warning)', subtle: 'var(--color-warning-subtle)' },
        error:   { DEFAULT: 'var(--color-error)',   subtle: 'var(--color-error-subtle)' },
        info:    { DEFAULT: 'var(--color-info)',    subtle: 'var(--color-info-subtle)' },
      },
      borderColor: { DEFAULT: 'var(--color-border)' },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
        serif: ['Lora', 'Georgia', 'Times New Roman', 'serif'],
      },
      borderRadius: { sm: '4px', md: '8px', lg: '12px', pill: '999px' },
    },
  },
};
```

Como os valores mudam dentro das variáveis, o modo escuro funciona sem prefixos `dark:`. Os componentes ficam como classes próprias (`.btn`, `.input`, `.sig`, `.stage`…) com o CSS que está em `wireframes-rasto.html`; os utilitários Tailwind servem para composição (flex, grid, gap, padding).

### 2.4 Tabela de componentes

Todas as cores referem tokens de `rasto.css`. "Estados" inclui sempre: normal, hover/pressionado, foco, desactivado, a carregar e erro, quando se aplicam.

| Componente | Variantes | Estados | Tokens | Acessibilidade e regras |
|---|---|---|---|---|
| **Botão** | primário, secundário, fantasma, perigo, só ícone; normal (44) e grande (48); largura total no telemóvel | normal, hover/pressionado (`primary-hover` / `primary-subtle`), foco (anel 2 px `focus`, afastado 2), desactivado (`surface-sunken` + `text-subtle`), a carregar (texto muda: "A enviar…", `aria-busy`), sem rodas animadas | `primary`, `on-primary`, `primary-hover`, `primary-subtle`, `border-strong`, `error`, `radius-md`, `text-label` 600 | Um primário por ecrã. Verbos no infinitivo ("Aceitar pedido"). Botão desactivado explica porquê ao lado (ex.: "Publicar fica activo quando houver rede"). Só ícone: `aria-label`, alvo 44 × 44. |
| **Ligação** | em texto, isolada | normal, hover, foco, visitada = normal | `primary` | Sempre sublinhada (não depende só da cor, WCAG 1.4.1). |
| **Campo de texto** | texto, e-mail, palavra-passe (com "Mostrar"), NIF, telefone (+244), pesquisa | normal, foco, preenchido, só leitura (fundo `surface-sunken`, contorno tracejado), erro, desactivado | `surface`, `border-strong`, `text`, `text-subtle` (placeholder), `error`, `focus`, `radius-md`, `text-body` | Rótulo visível sempre (placeholder não é rótulo). Erro com ícone + "Erro:" + como corrigir, ligado por `aria-describedby`. `autocomplete` correcto (1.3.5). Palavra-passe aceita colar (3.3.8). |
| **Área de texto com contador** | nota de pedido (300), resumo (280), destaques (600), motivo (300) | normal, perto do limite (contador `warning` a 90%), no limite (bloqueia), erro | `text-subtle` (contador), `warning` | Contador com `aria-live="polite"` só a partir de 90%. |
| **Campo de moeda** | Kz ou USD (selector segmentado + prefixo) | normal, foco, erro (não é número), com equivalência | `surface-sunken` (prefixo), `text-muted` (equivalência) | Só inteiros [S]: ignora espaços e pontos ao colar. Equivalência "≈ USD 54 000 · taxa de 01/11/2026" por baixo. `inputmode="numeric"`. |
| **Campo de data** | data, mês e ano (para marcos) | normal, erro (data impossível, fim antes do início) | iguais ao campo | Texto `dd/mm/aaaa` com máscara leve; sem calendário obrigatório (calendários nativos falham em Android antigo [S]). |
| **Selector segmentado** | 2–3 opções (moeda, Pendentes/Histórico, Kanban/Lista) | seleccionado (`primary-subtle` + `primary` + peso 600), normal, foco | `border-strong`, `primary-subtle`, `primary` | `role="tablist"` ou `radiogroup` conforme o caso. Seleccionado não depende só da cor (peso 600). |
| **Chip de selecção** | sectores, fases, geografias (multi) | seleccionado, normal, foco, desactivado | iguais ao segmentado, `radius-pill` | `aria-pressed`. Altura 40 + margem: alvo efectivo ≥ 44. |
| **Caixa e opção** | caixa (multi), opção (única) | marcada, desmarcada, foco, erro de grupo | `primary`, `border-strong` | Toda a linha é clicável; alvo 44. |
| **Navegação inferior** | 5 destinos por papel | actual (barra superior 3 px + cor + peso), normal, com contador | `surface`, `primary`, `text-muted`, `border` | Ícone + rótulo sempre. `aria-current="page"`. Contador numérico, não ponto vermelho. |
| **Barra lateral / calha** | 232 (lg) / 80 (md) | actual (`primary-subtle`), normal, contador | `surface`, `primary-subtle`, `primary` | Mesma ordem dos destinos do telemóvel. |
| **Cabeçalho de ecrã** | telemóvel (56, voltar/fechar + título + acção), computador (64, título + acções) | — | `surface`, `border` | Título é o `h1` da página. Voltar com `aria-label`. |
| **Selo de verificação** | nível alto (MVP); intermédio e básico [F]; 16, 20, 24 | validado, declarado, pendente (só startup), expirado, retirado, validado com aviso | `primary`, `--seal-knock`, `--seal-warn`, `text-muted` | Forma > texto > cor (guia 6.1). SVG decorativo (`aria-hidden`) com texto visível ao lado; sozinho: `role="img"` + `aria-label` "Validado por {entidade} em {data}". 16 px nunca sem texto. Carimbo dentado exclusivo de validação. |
| **Cartão de sinal** | validado, declarado, pendente (só startup), expirado, retirado | — | Validado: contorno `primary` + barra interna 3 px; declarado: contorno tracejado `border-strong`, fundo transparente | Rótulo em `caption` maiúsculas. Sempre: o que foi confirmado, quem, data da validação, data do facto. Secção "Verificado" antes de "Declarado pela startup". |
| **Cartão de startup (sugestão)** | normal, seleccionado (contorno `primary` 2 px), compatibilidade parcial (critério que falha em texto) | a carregar (esqueleto), erro | `surface`, `border`, `primary` | Pontuação **sempre** com a decomposição dos 4 critérios na mesma linha. Até 2 sinais validados com selo 16 + "+N validados". `article` com `h2`. |
| **Decomposição da compatibilidade** | compacta (uma linha de texto), completa (barra por critério + frase) | encaixe total, parcial, nenhum, peso 0 (risco, a cinzento) | `primary` (barra), `surface-sunken` (calha) | Valores "40 de 40" em texto; barras são redundantes. Frase obrigatória: "mede o encaixe com o seu mandato, não a qualidade da startup". |
| **Chip de etapa** | 7 etapas + Perdido | normal; Perdido riscado + ícone ✕ | `surface-sunken`, `text`, `text-muted` (pontos), `secondary` (pontos a partir de Soft commit) | Nome da etapa sempre escrito; 6 pontos indicam a posição. A cor da etapa não muda (só a laterite marca progresso de capital indicativo, guia 4.1). |
| **Chip de estado** | neutro (pendente, expirado), aviso (parada, prazo a expirar), sucesso (aceite), erro (erro de envio), info (fora da plataforma), primário (contagens) | — | `*-subtle` + cor do estado | Ícone + texto em todos os que não são neutros. Pendente diz **de quem e até quando** (regra 3 da base de UX). Sucesso nunca junto de um selo (guia 6.5.4). |
| **Cartão do pipeline** | telemóvel (com botão "Mover"), Kanban (compacto) | normal, parado (contorno `warning` + chip), a sincronizar (texto `warning` + ícone), seleccionado por teclado (anel `focus`), perdido | `surface`, `border`, `warning`, `focus` | Arrastar é opcional: "Mover para…" em menu e teclado (WCAG 2.5.7). Mostra: nome, tipo, origem (plataforma / fora), última actividade, valor se houver. |
| **Coluna Kanban / grupo por etapa** | coluna (≥ 1280), grupo recolhível (< 1280) | vazio ("Sem relações."), com contagem | `surface-sunken`, `caption` 600 | Cabeçalho com contagem. Perdidos fora das colunas (ligação "Perdidos (n)"). |
| **Gráfico de indicador** | número grande (KPI), barra de progresso da ronda, barras de conversão por etapa | normal, dados insuficientes (< 3 relações), valor da ronda em falta, a carregar | `metric-lg`, `secondary` (progresso da ronda), `primary` (barras), `surface-sunken` (calha) | Cada gráfico tem tabela equivalente ("Ver como tabela"). Barras com valor em texto. Progresso: `role="img"` + `aria-label` com a percentagem. Sem eixos inventados: uma escala, 0 a total. |
| **Tabela** | densa (lg), lista de cartões (< 1280) | linha seleccionada (`primary-subtle`), linha em foco, vazia, a carregar | `border-strong` (cabeçalho), `border` (linhas), `text-muted` | `th` com `scope`. Números alinhados à direita com `.num`. Em ecrã estreito vira lista, não rola para o lado (excepto tabelas de auditoria). |
| **Lista de pedidos** | pedidos de acesso (startup), validações (entidade), convites (entidade) | pendente com prazo, aceite, recusado, expirado, retirado, erro | chips de estado | Cada item: quem, o quê, prazo, acção principal. Ordenada por prazo mais próximo. |
| **Estado vazio** | primeira vez, sem resultados, filtrado | — | `text`, `text-muted`, botão | Sempre: porquê está vazio + uma acção seguinte (regra 4). Sem ilustrações dentro de cartões de dados; ilustração "pontos e trilho" só em vazios de ecrã inteiro, SVG < 5 KB. |
| **Notificação temporária** | sucesso, informação; com "Desfazer" | aparece 6 s, pausa com foco/hover | fundo `text`, texto `bg` (inverso) | `role="status"`. Nunca para erros que exigem acção (esses ficam como aviso em linha). |
| **Aviso em linha (banner)** | sem rede, erro, aviso, informação | — | `*-subtle` + cor | Erro: `role="alert"`, "Erro:" + o que fazer + referência. Sem rede: fixo no topo do conteúdo enquanto durar. |
| **Centro de notificações** | lista, item lido/não lido | vazio, não lidas | `primary` (marca de não lida) + peso | Não é mensagens (base de UX 4.1). Cada item leva ao objecto. |
| **Folha inferior / diálogo** | folha (< 768), diálogo (≥ 768) | aberta, a enviar | `surface`, `shadow-1`, `radius.sheet`, fundo escurecido | `role="dialog"` + `aria-modal`, foco preso, Esc fecha, foco volta ao botão de origem. Confirmações sempre dentro da página (nada de `confirm()`). |
| **Indicador de completude** | barra + texto "60% completo" + "faltam N obrigatórios" | rascunho, pronto a publicar, publicado | `primary` (barra), `surface-sunken` | `role="progressbar"` com `aria-valuenow`. |
| **Lista de passos (checklist)** | onboarding da startup, métricas por fase | feito (ícone neutro), validado (selo 20), por fazer (círculo vazio), obrigatório | `text-muted`, `primary` | Feito não usa verde (verde nunca perto de sinais). Cada linha é uma ligação para o passo. |
| **Passos de formulário** | 2 a 5 passos | actual, guardado, erro | `primary` (barra) | "Passo 2 de 3 · Comprovativos" em texto; rascunho guardado com hora. |
| **Esqueleto** | linha, bloco, cartão | — | `surface-sunken` | Estático. Só depois de 300 ms. Contentor com `aria-busy="true"`. |

### 2.5 Padrões transversais

- **Formulários:** um campo por linha no telemóvel; validação ao sair do campo e ao submeter; o primeiro erro recebe o foco; nada se perde por falha de rede (rascunho no aparelho com hora visível).
- **Confirmações:** antes de partilhar, validar ou revogar, a folha lista o que muda e para quem (regra 6 da base de UX).
- **Prazos:** em listas `até 17/11/2026`; a 3 dias ou menos, chip passa a `warning` com "faltam 3 dias".
- **Contagens honestas:** "2 compatíveis de 12 startups verificadas" (base de UX 5.1); nunca números simulados.

---

## 3. Ecrãs-chave em detalhe

Formato: objectivo · dado que justifica · estrutura · conteúdo de exemplo · estados · notas. Os conteúdos são fictícios (pessoas, startups, entidades, valores e taxa de câmbio de 1 USD = 920 Kz).

### 3.1 Aceleradora

#### E-02 · Início da entidade (painel)
- **Objectivo:** em 10 segundos, a gestora sabe o estado da entidade e o que precisa dela.
- **Porquê:** base de UX 3.1 (verificação é pico negativo); persona Teresa reporta "startups apoiadas" a financiadores [S].
- **Estrutura (1280):** barra lateral (Início · Turmas · Validações [n] · Entidade · Conta) → cabeçalho "Início" + "Nova turma" → cartão de estado da verificação → 3 indicadores da turma activa (convites aceites, perfis publicados, sinais validados) → "À espera de si" (3/5) + "Turmas" (2/5).
- **Estrutura (360):** mesma ordem numa coluna; indicadores em grelha 2 × 2 com o terceiro em largura total; "Turmas" passa para o destino Turmas.
- **Conteúdo:** "Entidade verificada pela plataforma a 10/01/2026"; "8 de 12 aceites · 8 aceites · 3 pendentes · 1 expirado"; "2 participações para confirmar — Kitanda Fresca e Dikanza Saúde"; "1 convite expirou — Reenviar".
- **Estados:** verificação submetida / em análise (prazo indicativo de 3 dias úteis, "pode preparar a turma em rascunho") / pedido de informação (diz o que falta e até quando) / recusada (motivo) / suspensa (aviso nos sinais) / verificada; sem turmas (vazio com "Nova turma"); a carregar (3 blocos de esqueleto); erro.
- **Notas:** barra de convites com 3 segmentos + legenda em texto (cor nunca sozinha). "À espera de si" ordena pelo prazo mais próximo.

#### E-04 · Nova turma
- **Objectivo:** criar a turma em menos de 2 minutos (tarefa A3, base de UX 9.4).
- **Estrutura:** Programa · Edição · Início · Fim · pré-visualização da frase de validação · "Criar turma".
- **Conteúdo:** "Programa de Aceleração" · "2026 · Turma 3" · 02/03/2026 · 26/06/2026 → pré-visualização "Participou no Programa de Aceleração 2026 · Turma 3 (Mar.–Jun. 2026)."
- **Estados:** entidade por verificar (banner: "Pode criar a turma em rascunho; os convites ficam disponíveis depois da verificação"); erro de datas ("o fim (26/02/2026) é antes do início (02/03/2026)"); a guardar; erro de rede (dados guardados).
- **Notas:** a pré-visualização responde ao medo reputacional da aceleradora (base de UX 3.1): vê a frase que vai assinar desde o primeiro momento.

#### E-06 · Convidar startups
- **Objectivo:** convidar várias startups de uma vez e resolver convites que falham (tarefas A4 e A6).
- **Estrutura:** separadores "Por e-mail" | "Por ligação" → área de texto (um e-mail por linha) → validação linha a linha → "Enviar N convites" → lista de convites com estado e acção.
- **Validação por linha:** válido (novo) · formato inválido (não é enviado, os restantes seguem) · já tem conta de startup (convite para juntar à turma) · já convidado para esta turma (ignorado, com aviso).
- **Por ligação:** mensagem pronta para WhatsApp/SMS (texto da base de UX 8.1) + "Copiar mensagem"; ligação pessoal de uso único.
- **Estados dos convites:** pendente (até dd/mm), aceite, recusado, expirado (Reenviar), cancelado, erro de envio (Corrigir e-mail).
- **Notas:** o botão diz o número real de envios ("Enviar 2 convites"), não "Enviar". A cópia anuncia-se com `aria-live`.

#### E-07 / E-08 · Fila de validação e confirmação
- **Objectivo:** validar com segurança e rapidez; nunca assinar o que não se sabe (base de UX 2.3).
- **Estrutura (1280):** separadores Pendentes (n) | Histórico → barra de selecção em lote → tabela (startup, o que vai confirmar, pedido em, expira) + painel de detalhe do item em foco com a frase exacta que o investidor vai ler → Validar / Recusar com motivo.
- **Estrutura (360):** lista de cartões; tocar abre E-08 (folha) com a frase e os dois botões.
- **Regras:** só **participações** entram em lote (base de UX 3.1); marcos validam-se um a um (caixa desactivada com explicação). Recusar exige motivo, que vai só para a startup. Histórico mostra validados, recusados e retirados com data, e permite "Retirar validação" (com folha de confirmação).
- **Estados:** vazio ("Nenhum pedido à espera. Quando uma startup aceitar um convite, a participação aparece aqui."); prazo a expirar (chip `warning`); entidade suspensa (validações bloqueadas com explicação); a enviar; erro.

### 3.2 Administração

#### D-02 · Processo de verificação
- **Objectivo:** verificar uma entidade em poucos minutos, com critérios fixos e prova guardada (persona 1.4).
- **Estrutura (1280, três colunas):** navegação · lista de processos (pesquisa + estado + prazo) · processo: dados da entidade → 4 critérios, cada um com "Cumpre / Falta / Não cumpre", evidência e nota → decisão → registo.
- **Critérios (base de UX 5.2):** existência legal (NIF, certidão) · presença pública · responsável com e-mail institucional · evidência de um programa realizado.
- **Regras:** "Verificar entidade" só activo com os 4 em "Cumpre". "Pedir informação" envia à entidade as notas dos critérios em "Falta" e muda o estado (prazo de 14 dias). "Recusar" exige motivo. Cada decisão entra no registo com autor, data e hora.
- **Estados:** submetida, em análise, pedido de informação (com dias em espera), verificada, recusada, suspensa (acção "Suspender" no processo de uma entidade verificada, com motivo).

### 3.3 Startup

#### S-01 · Início no arranque (onboarding com completude e métricas por fase)
- **Objectivo:** levar a fundadora ao perfil mínimo publicado sem saber de antemão o que um investidor quer ver.
- **Porquê:** 92% < 3 anos no ecossistema; 58% sem indicadores; "não sei que métricas mostrar" [D]; princípio P7.
- **Estrutura:** cartão de completude (% + barra + "faltam N obrigatórios") → lista de passos → cartão "Métricas sugeridas · {fase}" → "Continuar o perfil".
- **Cálculo da completude [S, H-I03]:** 6 campos obrigatórios (nome, sector, fase, cidade, resumo, ronda) valem 60% (10% cada); participação validada 10%; pelo menos 1 marco 10%; pelo menos 3 métricas da fase 10%; ligações para documentos 10%. **Publicar** fica disponível com os 6 obrigatórios, mesmo abaixo de 100%.
- **Métricas sugeridas por fase [S, H-10]:**

| Fase | Métricas sugeridas (escolher pelo menos 3) |
|---|---|
| Ideia | Entrevistas a clientes feitas · Utilizadores em lista de espera · Data prevista do MVP · Meses de tesouraria |
| Pré-seed | Clientes activos · Receita mensal (Kz) · Meses de tesouraria · Utilizadores em piloto · Custo mensal da operação (Kz) |
| Seed | Receita mensal (Kz) · Crescimento mensal da receita (%) · Clientes pagantes · Retenção de clientes (%) · Meses de tesouraria |
| Série A ou mais | Fora do foco do MVP; mostrar a lista de Seed |

- **Estados:** perfil mínimo incompleto; pronto a publicar (botão "Publicar perfil" passa a primário); publicado (o ecrã passa a ser S-13, com a lista de passos recolhida no fim enquanto não chegar a 100%).
- **Notas:** passo feito usa ícone neutro; a participação validada usa o selo (guia 6.5.4: nunca verde junto de sinais).

#### S-04 · Perfil com sinais (ver como investidor)
- **Objectivo:** a fundadora vê exactamente o que o investidor vê, nas duas camadas (tarefa S4).
- **Estrutura:** faixa "É isto que qualquer investidor autenticado vê" + selector Camada 1 | 2 → identidade (iniciais, nome, sector · fase · cidade) → resumo → ronda (valor e equivalência) → **Verificado** → **Declarado pela startup** → "Perfil actualizado há N dias".
- **Camada 2 acrescenta:** contacto do fundador, ligações para documentos, indicadores, actualizações.
- **Regras:** sinais pendentes não aparecem (só em S-03). Sem logótipo carregado: iniciais (sem pedido de imagem). [Dec-I1]: a % comprometida não aparece na camada 1.

#### S-06 · Decidir pedido de acesso
- **Objectivo:** decidir com segurança sobre alguém que não conhece (pico negativo da jornada, base de UX 3.2; [H-05]).
- **Estrutura:** quem (nome, tipo, "dados declarados pelo investidor") + prazo → "Porque este investidor encaixa" (pontuação + 4 critérios em barra e frase) → nota → "Se aceitar, {Nome} passa a ver:" → Recusar | Aceitar → "Sem resposta até {data}, o pedido expira".
- **Estados:** pendente; aceite (notificação temporária + lembrete sobre a partilha das ligações); recusar (folha com motivo opcional por categoria, [Dec-4]); expirado; retirado pelo investidor; investidor sem conta aprovada nunca chega aqui ([Dec-1]).

#### S-08 · Pipeline
- **Objectivo:** saber a cada momento em que etapa está cada investidor (54% não sabem [D]) e agir sobre relações paradas.
- **Telemóvel (lista por etapa):** separadores Pipeline | Pedidos (n) → linha-resumo ("6 relações activas · 37,5% da ronda comprometido · 1 parada") → grupos por etapa, da mais avançada para a menos avançada, recolhíveis, com contagem → cartão com "Mover" → "Identificado 0 · Term sheet 0 · Fechado 0 · Perdidos (1)".
- **Computador (Kanban):** 7 colunas da esquerda para a direita, Perdidos fora das colunas; "Adicionar investidor de fora" no cabeçalho.
- **Mover:** folha "Mover para…" com todas as etapas; Soft commit e Fechado pedem valor (Kz ou USD), Perdido pede motivo (lista fechada + Outro) e nota privada; Reunião pede data e nota opcional.
- **Arrastar:** só no Kanban e só como atalho; teclado: Espaço selecciona, setas mudam de coluna, Enter confirma, Esc cancela; anúncio "Grupo Kalandula movido para Soft commit" em `aria-live`.
- **Estados:** vazio (adicionar investidor de fora); parada (contorno e chip `warning`, acções "Registar contacto" e "Adiar lembrete"); a sincronizar (movimento guardado no aparelho); conflito (outro membro da equipa moveu: mostra a versão recente); depois de perder ("Registado. A ronda continua…" + Desfazer).

#### S-12 · Publicar actualização
- **Objectivo:** actualização mensal sem ajuda (meta da [H-10]: ≥ 80%).
- **Estrutura:** título com o mês → métricas da fase pré-preenchidas com o valor do mês anterior e a variação → destaques (600) → onde precisamos de ajuda (opcional) → destinatários ("3 investidores com acesso vão receber") → aviso "depois de publicada não se edita" → Pré-visualizar | Publicar.
- **Estados:** rascunho no aparelho (sem rede: Publicar desactivado com explicação); rascunho no servidor; sem destinatários ("ninguém recebe ainda; fica visível a quem tiver acesso no futuro"); publicada; falha parcial de e-mail (lista quem não recebeu).

#### S-13 · Painel de indicadores da ronda
- **Objectivo:** responder em 1 minuto a "quanto já tenho?" e "o que está parado?" (tarefa S10). 71% pediram painéis [D].
- **Estrutura (1280):** cabeçalho com nome da ronda, data de início e "calculado a partir do pipeline" + moeda de visualização (USD | Kz) → ronda comprometida (número grande + barra laterite + detalhe dos compromissos + "indicativo, não vinculativo") → 3 indicadores (tempo até ao 1.º soft commit, relações activas, relações paradas com acção) → conversão por etapa (barras + contagem + % + "Ver como tabela").
- **Estrutura (360):** mesma ordem; indicadores em coluna; a conversão mostra só a tabela (etapa · chegaram · passaram %), sem barras.
- **Fórmulas:** as da base de UX 5.7. Valores em moedas diferentes somam-se na moeda da ronda à taxa de referência, sempre com "≈" e a data da taxa.
- **Estados:** sem valor da ronda; sem soft commits; dados insuficientes (< 3 relações); a carregar; erro.

### 3.4 Investidor

#### I-02 · Mandato
- **Objectivo:** mandato mínimo (sector + fase) em menos de 6 minutos (tarefa I1).
- **Estrutura:** aviso de privacidade ("Só as startups a quem pedir acesso vêem o seu mandato") → Sectores (chips, multi) → Fase (chips, com definição curta) → Valor do cheque (moeda + mínimo + máximo + equivalência) → Geografia (chips: "Angola (todas)" + províncias) → Risco (opcional, "ainda não conta (peso 0)") → contagem honesta de startups compatíveis → "Guardar e ver sugestões".
- **Regras:** listas vêm de D-04 (configuráveis, contexto); campos que a administração desactivar desaparecem sem mudar o código. Guardado automático com hora.
- **Estados:** rascunho; mandato mínimo incompleto (indica o que falta); conta pendente de aprovação ([Dec-1]); 0 compatíveis (mostra a opção de rever o mandato).

#### I-03 · Sugestões com a pontuação explicada
- **Objectivo:** escolher e justificar a startup com maior encaixe (tarefa I2, meta ≥ 80% citam um critério).
- **Estrutura (1280):** cabeçalho com contagem real e resumo do mandato → lista de cartões (2/3) + painel "Porque esta startup" (1/3) da startup seleccionada → "Ver perfil" | "Pedir acesso".
- **Estrutura (360):** lista de cartões; "Porque esta startup" abre o perfil I-04 na secção de compatibilidade.
- **Cartão:** nome; sector · fase · cidade · ronda; pontuação "90 de 100"; decomposição compacta ("Sector 40/40 · Fase 25/25 · Cheque 25/25 · Geografia 0/10"); até 2 sinais validados (selo 16 + texto).
- **Ordem:** pontuação descendente; empate: mais sinais validados, depois actualização mais recente [S].
- **Estados:** erro (mandato guardado, "Tentar de novo"); 0 compatíveis (vazio honesto + parciais + aviso por e-mail + rever mandato); poucas (1–4, com "Ver compatibilidades parciais (n)"); normal; parciais (cada cartão diz o critério que falha).

#### I-05 · Pedido de acesso com nota
- **Estrutura:** nome da startup → "A {Startup} vai ver o seu nome, a sua organização, o seu mandato e esta nota" → nota (300, com exemplo) → "Se aceitar, passa a ver…" → "Enviar pedido".
- **Estados:** a escrever; erro de envio (nota guardada); enviado (prazo); pendente com "Retirar pedido"; bloqueado até {data + 90 dias}; conta por aprovar ([Dec-1]); já existe pedido activo.

#### I-07 · Acompanhamento das relações
- **Estrutura (1280):** selector Kanban | Lista → tabela: startup, etapa (chip), último movimento, actualizações (nova / mês), estado (pedido pendente, acesso concedido, parada, perdido), acções.
- **Estados:** vazio ("Guarde uma sugestão ou peça acesso para começar"); pedido pendente com prazo; acesso revogado ("o histórico fica consigo; contacto e documentos deixam de aparecer"); parada; perdido com motivo privado.

---

## 4. Acessibilidade e desempenho

### 4.1 WCAG 2.2 AA: decisões concretas

| Critério | Decisão |
|---|---|
| 1.1.1 Conteúdo não textual | Selos decorativos com texto visível ao lado; selo isolado com `aria-label` completo; ícones de navegação com rótulo. |
| 1.3.1 Informação e relações | Secções "Verificado" e "Declarado" são `h2`; tabelas com `th scope`; grupos de chips em `fieldset` + `legend`. |
| 1.3.5 Finalidade da entrada | `autocomplete`: `name`, `email`, `username`, `current-password`, `new-password`, `organization`, `tel`. |
| 1.4.1 Utilização da cor | Estados com forma + texto + cor (selos, chips com ícone, etapas com nome e pontos, ligações sublinhadas, erro com "Erro:"). |
| 1.4.3 / 1.4.11 Contraste | Herdado dos tokens (todos AA, medidos no guia 4.2). Contornos de controlos usam `border-strong` (3,62:1 claro, 3,78:1 escuro); `border` só para divisórias. |
| 1.4.4 / 1.4.10 Redimensionar e reflow | Tudo em `rem`; a 320 CSS px (zoom 400% a 1280) nada rola na horizontal excepto tabelas de auditoria em contentor próprio. |
| 1.4.12 Espaçamento do texto | Sem alturas fixas em contentores de texto; cartões crescem com o conteúdo. |
| 1.4.13 Conteúdo em hover | Sem tooltips com informação essencial; explicações ficam visíveis em texto de ajuda. |
| 2.1.1 Teclado | Tudo operável por teclado, incluindo Kanban (2.5.7) e chips de selecção. |
| 2.4.3 / 2.4.7 Ordem e foco visível | Anel `focus` 2 px, afastado 2 px (`:focus-visible`); ordem de tabulação segue a leitura. Folhas prendem o foco e devolvem-no. |
| 2.4.11 Foco não tapado | Conteúdo com espaço inferior igual à barra de navegação fixa; `scroll-padding-bottom` nos formulários. |
| 2.5.7 Movimentos de arrastar | Kanban: "Mover para…" em menu e teclado; arrastar é só atalho. |
| 2.5.8 Tamanho do alvo | Mínimo 44 × 44 (token `touch-target`), acima dos 24 exigidos. |
| 3.2.6 Ajuda consistente | Ligação "Ajuda e privacidade" sempre no mesmo lugar (Conta e rodapé das páginas públicas). |
| 3.3.1 / 3.3.3 Identificação e sugestão de erro | "Erro:" + o que falhou + como corrigir, por campo e no topo do formulário com ligações para cada campo. |
| 3.3.7 Entrada redundante | Rascunhos guardados; dados da entidade e do convite pré-preenchidos (e-mail do convite só leitura). |
| 3.3.8 Autenticação acessível | Sem CAPTCHA de teste cognitivo [S]; colar e gestores de palavras-passe permitidos; "Mostrar" na palavra-passe. |
| 4.1.3 Mensagens de estado | `role="status"` para guardado, copiado, movido; `role="alert"` para erros; `aria-busy` nos esqueletos. |

Testes mínimos por sprint: navegação só com teclado; TalkBack no Android (o aparelho provável da persona [S]); zoom a 200% e 400%; modo escuro; `prefers-reduced-motion`; verificação automática com axe.

### 4.2 Desempenho em redes lentas

| Tema | Decisão |
|---|---|
| **Orçamento por página [S, H-I04]** | HTML + CSS crítico ≤ 50 KB comprimido; JavaScript inicial ≤ 120 KB comprimido; fontes ≤ 2 ficheiros na aplicação; 1.ª pintura de conteúdo < 3 s em "Slow 4G" das ferramentas do Chrome, num Android de gama média. |
| **Renderização** | Conteúdo textual vindo do servidor (HTML pronto), não montado no cliente depois de vários pedidos. |
| **CSS** | Tailwind compilado e purgado; nada de CDN de Tailwind em produção. |
| **Fontes** | Só Inter (subconjunto latino, `font-display: swap`), alojada no próprio servidor (guia 5.1). Lora só nas páginas públicas. A pilha de recurso (`system-ui`) mantém a leitura se a fonte não chegar. |
| **Imagens** | Só logótipos de startups e entidades, opcionais: WebP 96 × 96, ≤ 15 KB, `loading="lazy"`, `width`/`height` declarados. Sem logótipo: iniciais. Sem fotografias no MVP. Ícones e selos em SVG embutido (sprite). |
| **Esqueletos** | Só depois de 300 ms; estáticos; a forma imita o conteúdo final para não haver saltos. |
| **Listas** | 20 itens por página com "Ver mais"; nada de rolagem infinita. |
| **Rede instável** | Formulários e movimentos do pipeline guardados no aparelho e reenviados quando houver rede (base de UX 5.9); aviso "Sem ligação" fixo; botões que dependem de rede ficam desactivados com explicação. |
| **Animações** | Nenhuma funcionalidade depende de animação; transições de 120–200 ms só em cor e opacidade. |
| **Dados móveis** | Sem vídeos, sem pré-carregamento de páginas, sem actualizações automáticas em segundo plano; a lista de notificações carrega quando se abre. |

---

## 5. Formatos locais

| Tipo | Formato | Exemplo | Regra |
|---|---|---|---|
| Milhares | espaço fino inquebrável (U+202F) | `73 600 000` | Agrupar sempre a partir de 4 dígitos (`1 850`, não `1850`), também em tabelas. |
| Decimal | vírgula | `37,5%` | Uma casa nas percentagens quando não é inteira. |
| Moeda | código antes, espaço, valor | `Kz 45 000 000` · `USD 80 000` | Sem cêntimos [S]. Nunca `AOA` nem `$` na interface. |
| Equivalência | `≈` + outra moeda + taxa e data | `≈ USD 54 000 · taxa de referência de 01/11/2026` | Taxa definida em D-05; o valor guardado é o introduzido. |
| Percentagem | sem espaço | `35%` | — |
| Data em listas | `dd/mm/aaaa` | `12/07/2026` | Sempre com zeros à esquerda. |
| Data em texto | dia + mês por extenso + ano | `12 de Julho de 2026` | Mês com maiúscula, como na base de UX. |
| Mês de um marco | mês abreviado + ano | `Ago. 2026` · `Mar.–Jun. 2026` | — |
| Hora | 24 h | `13:51` | — |
| Tempo relativo | "há N dias" até 30 dias; depois a data | `há 5 dias` | Em `<time datetime="…">` com a data completa. |
| Fuso | Africa/Luanda (UTC+1) | — | Prazos fecham às 23:59 de Luanda; guardar em UTC. |
| Telefone | `+244 9XX XXX XXX` | `+244 923 456 789` | — |
| NIF | como introduzido, só dígitos | `5417832019` | — |

**Formatação na engenharia [S, a confirmar no navegador alvo]:** `Intl.NumberFormat('pt-PT')` usa por defeito espaço como separador mas **não agrupa números de 4 dígitos** (`1850`) e o carácter de espaço pode variar entre navegadores. Recomendo uma função própria:

```js
// Formatação única para toda a interface
const SEP = ' ';
export function fmtInt(n) {
  return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, SEP);
}
export function fmtMoney(n, cur) { return `${cur} ${fmtInt(n)}`; }           // 'Kz 45 000 000'
export function fmtPct(x, digits = 1) {                                          // '37,5%'
  const v = Number.isInteger(x) ? String(x) : x.toFixed(digits).replace('.', ',');
  return `${v}%`;
}
export function parseMoney(s) { return Number(String(s).replace(/\D/g, '')); } // aceita '45.000.000' e '45 000 000'
```

---

## 6. Hipóteses e decisões de interface

### 6.1 Hipóteses [H-I] (podem entrar no guia de sessão da base de UX, secção 9.6)

| ID | Hipótese | Como testar | Critério |
|---|---|---|---|
| **H-I01** | Startups usam mais o telemóvel; investidores e aceleradoras mais o computador. | Perguntar o aparelho habitual em cada sessão; depois do lançamento, largura de ecrã por papel (agregada). | ≥ 70% das startups em telemóvel; ≥ 60% dos outros papéis em computador. |
| **H-I02** | A lista por etapa no telemóvel é tão eficaz como o Kanban no computador. | Tarefas S7, S8 e S10 nos dois tamanhos. | Diferença de sucesso < 10 pontos; tempo mediano dentro do alvo. |
| **H-I03** | A percentagem de completude leva a publicar o perfil mínimo sem ajuda. | Tarefa S2. | ≥ 80% publicam em ≤ 8 min. |
| **H-I04** | O orçamento de desempenho chega para uso aceitável em dados móveis pré-pagos. | Medir em 2 aparelhos Android de gama média com a rede de Luanda (não só simulada). | 1.ª pintura < 3 s em ≥ 80% das medições. |
| **H-I05** | A decomposição compacta no cartão ("Sector 40/40 · …") chega para escolher sem abrir o painel. | Tarefa I2 com e sem painel aberto. | ≥ 80% citam um critério correcto sem abrir o painel. |

### 6.2 Decisões de interface em aberto

| ID | Decisão | Opções | Recomendação | Dado |
|---|---|---|---|---|
| **Dec-I1** | A % da ronda comprometida aparece na camada 1? | (a) não, só o valor da ronda; (b) sim, com consentimento da startup | **(a)** no MVP, coerente com a base de UX 5.6; (b) para depois de H-05 | Privacidade em quase todas as respostas [D] |
| **Dec-I2** | Tablet (768–1279) tem Kanban? | (a) não, lista por etapa; (b) sim, com rolagem horizontal | **(a)**: 7 colunas não cabem legíveis e não há dado sobre uso de tablet | — |
| **Dec-I3** | Ícone dos passos feitos na lista de passos | (a) visto neutro; (b) visto verde | **(a)**: o guia proíbe verde perto de sinais e a lista contém o sinal de participação | Guia de marca 6.5 |

---

## 7. Trabalho futuro (interface)

- Versão de telemóvel dedicada para a administração.
- Kanban no tablet (Dec-I2).
- Vista de alto contraste (AAA) nas definições (já no guia como [F]).
- Ilustrações "pontos e trilho" para cada estado vazio de ecrã inteiro.
- Exportação dos indicadores para relatórios de comité (base de UX 11).
- Modo totalmente offline e aplicação nativa (fora do escopo).
- Gráficos de evolução das métricas mês a mês nas actualizações (precisa de 3 ou mais actualizações por startup).

---

## 8. Ecrãs do primeiro sprint, prontos para o desenvolvimento

**Objectivo do sprint:** autenticação com papéis, módulo da aceleradora e verificação de entidades a funcionar de ponta a ponta, com a entrada da startup por convite. É o que a ronda 1 de testes precisa (base de UX 9.3: "código funcional para aceleradora e entrada da startup por convite").

**Fluxo que fica coberto:** a entidade regista-se (E-01) → a administração verifica (D-01, D-02) → a entidade cria a turma (E-04) e convida (E-06) → a startup aceita e cria conta (C-03) → a participação chega à fila (E-07) → a entidade confirma (E-08) → o sinal fica validado. A startup entra num Início provisório (S-01 só com a lista de passos, sem edição de perfil, que é do Sprint 2).

| # | ID | Ecrã | Componentes principais | Estados a implementar | Critérios de aceitação |
|---|---|---|---|---|---|
| 1 | C-00 | Concha por papel | navegação inferior, barra lateral, calha, cabeçalho, aviso de rede, notificação temporária | sem rede, sessão expirada (volta ao formulário sem perder dados) | 4 papéis com os seus 5 destinos; troca de navegação a 768 e 1280; foco nunca tapado pela barra. |
| 2 | C-01 | Entrar | campo, palavra-passe com "Mostrar", botão, ligação, aviso de erro | erro de credenciais, a entrar, sem rede, bloqueio temporário | Redirecciona para a área do papel; mensagem de erro não diz qual campo falhou; colar permitido. |
| 3 | C-02 | Recuperar palavra-passe | campo, botão | enviado ("Se o e-mail existir, enviámos uma ligação"), ligação expirada, palavra-passe fraca | Ligação válida 1 h [S]; não revela se o e-mail existe. |
| 4 | C-03 | Aceitar convite | campo só leitura, caixa de consentimento, botão | válido, expirado, já usado, já tem conta, sessão de outro papel, recusar | Cria conta de startup ligada à turma; cria o sinal de participação em "pendente de validação"; consentimento registado com data (Lei 22/11). |
| 5 | C-04 | Privacidade e termos | página de texto | — | Linguagem simples; contacto para pedidos de titulares. |
| 6 | E-01 | Registo da entidade (3 passos) | passos de formulário, campos, envio de ficheiro (≤ 2 MB), rascunho | rascunho, erro de envio (dados guardados), submetida | Rascunho sobrevive a fechar o navegador; ao submeter, estado "Submetida" e notificação à administração. |
| 7 | E-02 | Início da entidade | cartão de estado, indicador, lista "À espera de si", tabela | 6 estados de verificação, sem turmas, a carregar, erro | Antes de verificada: convites e validações bloqueados com explicação; contagens batem com E-05 e E-07. |
| 8 | E-03 | Turmas (lista) | tabela / lista de cartões | vazio, rascunho, activa | Ordenada pela data de início, mais recente primeiro. |
| 9 | E-04 | Nova turma | campos, campo de data, pré-visualização | erro de datas, rascunho (entidade por verificar) | 3 campos obrigatórios (programa, edição, datas); pré-visualização actualiza ao escrever. |
| 10 | E-05 | Turma (detalhe) | lista de convites, chips de estado | vazio ("convide as startups desta turma"), por estado | Mostra startups aceites e convites com acções (reenviar, cancelar, corrigir). |
| 11 | E-06 | Convidar startups | área de texto, validação por linha, separadores, copiar | e-mail inválido por linha, já existe, já convidado, enviado, erro de envio | Linhas inválidas não bloqueiam as válidas; botão mostra o número de envios; convite expira em 14 dias com lembrete ao 7.º (D-05). |
| 12 | E-07 | Validações | tabela com selecção em lote, painel de detalhe, separadores | vazio, pendente, prazo a expirar, histórico (validado, recusado, retirado) | Lote só para participações; frase exacta visível antes de confirmar. |
| 13 | E-08 | Confirmar / recusar / retirar validação | folha (360) e diálogo (≥ 768) | a enviar, erro | Recusa e retirada exigem motivo; cada decisão entra na auditoria com autor e data. |
| 14 | D-01 | Verificação (lista) | lista com pesquisa e chips | vazio, por estado | Ordenada pelo prazo indicativo mais próximo. |
| 15 | D-02 | Processo de verificação | critérios com selector, notas, registo | 6 estados | "Verificar" só com 4 critérios cumpridos; "Pedir informação" envia notas dos critérios em falta. |
| 16 | S-01 (mín.) | Início provisório da startup | indicador de completude, lista de passos | rascunho | Mostra a participação pendente/validada e os passos seguintes; nenhum beco sem saída. |

**Pronto para desenvolver quando** (definição de pronto, por ecrã): rota e papel definidos; todos os estados da tabela com texto final (microcopy da base de UX 8); componentes só com tokens; teclado e leitor de ecrã verificados; testado a 360, 768 e 1280 nos modos claro e escuro; rascunho local nos formulários; dentro do orçamento de desempenho (4.2).

**Dependências que ficam para a engenharia confirmar:** armazenamento dos comprovativos da entidade (só para verificação, não é cofre de documentos); envio de e-mail com estado de entrega (para "erro de envio"); ligação pessoal de convite de uso único; registo de auditoria desde o primeiro dia.
