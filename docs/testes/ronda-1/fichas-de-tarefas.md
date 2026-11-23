# Fichas de tarefas · sessões de 26 e 27 de Novembro de 2026

As tarefas são as do Capítulo IV, Quadro 13. Ler o cenário em voz alta e entregá-lo por escrito. Tempos-alvo da base
de UX (9.4) [S], a recalibrar com o primeiro participante de cada papel. Base de dados: `infra/demo.sh repor`
(dados de `semear_demo`); palavra-passe de todas as contas de demonstração: `demonstracao-rasto-2026`.

## Entidade validadora

| ID | Cenário (ler ao participante) | Conta / preparação | Critério de sucesso | Tempo-alvo |
|---|---|---|---|---|
| A1 | «Registe a sua aceleradora na plataforma e envie-a para verificação.» | Registo novo («Sou uma aceleradora»); entregar um PDF fictício | Entidade submetida | ≤ 6 min |
| A3 | «Crie a turma do vosso programa deste ano.» | `gestora@kalandula.demo` (entidade já verificada) | Turma criada com datas | ≤ 2 min |
| A4 | «Convide estas 3 startups. Uma delas prefere receber o convite por WhatsApp.» | Entregar 3 e-mails terminados em `.demo` | 2 convites por e-mail e 1 ligação copiada | ≤ 3 min |
| A5 | «Confirme a participação de duas startups. Uma terceira pediu o selo mas não participou: recuse.» | Kitanda e Dikanza pendentes; a Zola Logística pediu o selo e é a que deve ser recusada | 2 validações e 1 recusa com motivo | ≤ 3 min |

## Startup

| ID | Cenário (ler ao participante) | Conta / preparação | Critério de sucesso | Tempo-alvo |
|---|---|---|---|---|
| S1 | «Crie a conta da vossa startup e peça à vossa aceleradora o selo de participação.» | Registo novo («Criar conta da startup»); aceleradora: Kalandula | Pedido de selo enviado | ≤ 5 min |
| S2 | «Deixe o perfil pronto para os investidores verem.» | A mesma conta de S1 | Perfil publicado | ≤ 8 min |
| S4 | «Antes de aceitar alguém, o que é que um investidor já vê sobre vocês? E o que passa a ver se aceitar?» | `ana@mbote.demo` | Distingue as duas camadas | ≤ 3 min |
| S5 | «Chegou um pedido de acesso. Decida se aceita e explique porquê.» | `ana@mbote.demo` (pedido da Marta Lopes) | Decide e cita um elemento do ecrã | ≤ 3 min |
| S7 | «Na semana passada reuniu-se com um investidor que não está na plataforma. Registe isso.» | `ana@mbote.demo` | Investidor de fora em Reunião | ≤ 3 min |
| S9 | «Publique a actualização deste mês.» | `ana@mbote.demo` | Actualização publicada | ≤ 5 min |
| S10 | «Quanto da ronda já está comprometido? Que relação está parada?» | `ana@mbote.demo` | Responde às duas perguntas (20%; Helena Cardoso) | ≤ 1 min |

## Investidor

| ID | Cenário (ler ao participante) | Conta / preparação | Critério de sucesso | Tempo-alvo |
|---|---|---|---|---|
| I1 | «Registe-se e diga à plataforma em que tipo de startups investe.» | Registo novo («Sou investidor»); sugerir *fintech* e *seed* | Mandato mínimo guardado | ≤ 6 min |
| I2 | «Qual destas startups encaixa melhor no seu mandato? Porquê?» | A mesma conta de I1 | Cita pelo menos 1 critério | ≤ 3 min |
| I3 | «Quem confirmou que esta startup participou num programa, e quando?» | Perfil da Mbote Pagamentos | Entidade (Aceleradora Kalandula) e data correctas | ≤ 1 min |
| I4 | «Peça acesso a esta startup.» | Mbote Pagamentos | Pedido enviado com nota | ≤ 3 min |
| I7 | «Mude o mandato para um sector sem startups. O que faz agora?» | A mesma conta | Usa as compatibilidades parciais | ≤ 2 min |

## Métricas por tarefa (base de UX 9.5)

- **Resultado:** `sucesso`, `sucesso_com_ajuda` ou `falha`.
- **Tempo:** do fim da leitura do cenário até ao critério de sucesso (segundos).
- **Erros:** `criticos` (impedem a tarefa) e `nao_criticos` (recuperados).
- **Facilidade (SEQ):** «Quão fácil foi esta tarefa?» de 1 (muito difícil) a 7 (muito fácil).
- **Metas:** ≥ 80% sem ajuda em cada tarefa; 0 erros críticos em S4, S5, I2 e I3; mediana do tempo ≤ tempo-alvo;
  mediana do SEQ ≥ 5.
- **Compreensão:** I3 (sinal), I2 (compatibilidade) e S4 (privacidade): ≥ 80% de respostas correctas.
