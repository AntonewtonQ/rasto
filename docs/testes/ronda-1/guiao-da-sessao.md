# Ronda 1 de testes · Guião da sessão

**Quando:** 9 e 10 de Novembro de 2026 · **Duração:** 45 a 60 minutos por participante
**Quem:** 2 a 4 entidades validadoras (aceleradoras ou universidades) e 3 a 5 fundadores
**O quê:** o fluxo da aceleradora (registo, turma, convites, validação) e a entrada da startup por convite
**Onde:** presencial (ISPTEC ou espaço da aceleradora) ou por videochamada com partilha de ecrã
**Base:** base de UX, secções 9.3 a 9.7; especificação de interface, secção 8

## Antes da sessão

- [ ] Ambiente de teste no ar, com dados fictícios (`manage.py semear_demo`); nunca dados reais.
- [ ] Uma conta de entidade nova por participante de entidade (o participante regista-a na tarefa A1).
- [ ] Para os fundadores: um convite por ligação criado na turma de demonstração, pronto a enviar por WhatsApp.
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
2. «Prefere que a plataforma o trate por "tu" ou "você"?» (H-15)

## 55–60 min · Fecho

- «Há alguma coisa que não perguntei e devia ter perguntado?»
- Agradecer. Explicar quando haverá a versão seguinte (ronda 2, 24 a 26 de Novembro).

## Depois da sessão

- Classificar cada problema na escala de severidade de Nielsen (0 a 4) e registar a alteração proposta.
- Corrigir os problemas de severidade 3 e 4 antes da ronda 2.
- Calcular os resultados com `python3 calcular.py` (SUS por papel, sucesso e tempos por tarefa).
- Gravações apagadas depois da defesa; transcrições sem nomes.
