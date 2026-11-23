# Testes de usabilidade · Guião da sessão

**Quando:** 26 e 27 de Novembro de 2026 · **Duração:** 45 a 60 minutos por participante
**Quem:** 2 a 4 entidades validadoras (aceleradoras ou universidades), 3 a 5 fundadores e 2 a 4 investidores
**O quê:** as tarefas do Capítulo IV, Quadro 13 (`fichas-de-tarefas.md`): aceleradora (registo, turma, convites,
validação), startup (conta, selo, perfil, pedido de acesso, pipeline, actualização) e investidor (mandato, sugestões,
sinais, pedido de acesso)
**Onde:** presencial (ISPTEC ou espaço da aceleradora) ou por videochamada com partilha de ecrã
**Base:** base de UX, secções 9.3 a 9.7; especificação de interface, secção 8

## Antes da sessão

- [ ] Ambiente de teste no ar com dados fictícios: `infra/demo.sh repor` antes de cada participante (repõe os
      cenários das fichas); nunca dados reais.
- [ ] Entidades: o participante regista uma entidade nova em A1 e usa `gestora@kalandula.demo` de A3 em diante.
- [ ] Fundadores: registo novo em S1–S2; `ana@mbote.demo` de S4 em diante.
- [ ] Investidores: registo novo em I1; a Mbote Pagamentos serve para I3 e I4.
- [ ] Termo de consentimento impresso ou em formulário; folhas de registo (`registo-sessoes.csv`, `respostas-sus.csv`).
- [ ] Preferir o telemóvel do próprio participante (rede e aparelho reais). Em computador, simular rede lenta.
- [ ] Atribuir um código ao participante (ex.: E01, F01). **O nome nunca entra nas folhas de registo.**

## 0–5 min · Boas-vindas e consentimento

> «Estamos a testar a plataforma, não a si. Se algo for difícil, o problema é nosso. Pode pensar em voz alta: diga o que procura, o que espera que aconteça e o que o surpreende.»

- Explicar para que serve a sessão, o que se grava, onde fica guardado, por quanto tempo, e que pode desistir a qualquer momento.
- Assinar o termo de consentimento. Gravação só com a caixa própria marcada.

## 5–12 min · Entrevista de contexto

**Entidades validadoras**
1. Como confirmam hoje que uma startup participou num programa?
2. O que estariam dispostos a confirmar além da participação?
3. Quanto tempo por mês podiam dedicar a validações?
4. O que vos preocupa em associar o nome da entidade a uma startup?

**Fundadores**
1. Conte-me a última vez que contactou um investidor. O que aconteceu a seguir?
2. Que prova de credibilidade gostaria de mostrar e hoje não consegue?
3. O que nunca partilharia com um investidor antes de o conhecer?

## 12–40 min · Tarefas com pensamento em voz alta

- Ler cada cenário em voz alta e entregá-lo por escrito (`fichas-de-tarefas.md`).
- Perguntas neutras apenas: «O que está a pensar?», «O que esperava que acontecesse?», «Onde procuraria?»
- Não ajudar antes de 2 minutos de bloqueio; nesse caso, registar «sucesso com ajuda».
- Depois de cada tarefa, perguntar a facilidade de 1 (muito difícil) a 7 (muito fácil) — SEQ.
- Registar em `registo-sessoes.csv`: resultado, tempo, erros (críticos e não críticos), SEQ e uma nota curta (sem nomes).

## 40–45 min · Questionário SUS

Entregar `questionario-sus.md`. Registar as 10 respostas em `respostas-sus.csv`.

## 45–55 min · Entrevista de validação

**Entidades validadoras** (hipóteses H-06 e H-07 da base de UX)
1. Mostrar a frase de validação: «{Startup} participou no {Programa} {Edição} ({período}).» — «Assinaria isto? O que mudaria?»
2. «Que marcos se sentem confortáveis a confirmar (ex.: MVP lançado, primeiro cliente pagante, constituição legal)?»
3. «Quanto tempo acha razoável para responder a um pedido de validação?» (H-08)

**Fundadores**
1. «Aceitaria um pedido de um investidor que não conhece? O que precisaria de ver?» (H-05)
2. «As métricas sugeridas na actualização são as que mostraria a um investidor? O que falta?» (H-10)

**Investidores** (H-01, H-02)
1. «Que campos faltam no mandato para descrever onde investe?»
2. «Distribua 100 pontos pelos critérios: sector, fase, valor do cheque, geografia e risco.»
3. Mostrar três cartões de startups: «Ordene-as do mais para o menos interessante para si.»
4. «Usaria esta informação para decidir marcar uma reunião?» (1 a 7)

## 55–60 min · Fecho

- «Há alguma coisa que não perguntei e devia ter perguntado?»
- Agradecer.

## Depois da sessão

- Classificar cada problema na escala de severidade de Nielsen (0 a 4) e registar a alteração proposta.
- Corrigir os problemas de severidade 3 e 4 antes da ronda 2.
- Calcular os resultados com `python3 calcular.py` (SUS por papel, sucesso e tempos por tarefa).
- Gravações apagadas depois da defesa; transcrições sem nomes.
- Resultados no Capítulo IV: SUS e tarefas com `calcular.py`; entrevistas resumidas por hipótese, sem nomes.
