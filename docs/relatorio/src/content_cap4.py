# -*- coding: utf-8 -*-
# Capítulo IV: os resultados das sessões só entram quando houver dados reais (instruções do relatório, secção 3).
R = "{{[RESULTADO A INSERIR]}}"
CAP4 = [
("h1", "CAPÍTULO IV: DISCUSSÃO DOS RESULTADOS"),
("p", "Este capítulo apresenta a avaliação do protótipo em duas partes. A primeira é a verificação técnica, feita "
      "com testes automáticos sobre o código entregue. A segunda é a avaliação com utilizadores: testes de "
      "usabilidade com tarefas, o questionário SUS e entrevistas de validação com investidores e aceleradoras. Os "
      "resultados com utilizadores dependem das sessões de teste e só são apresentados quando houver registos "
      "reais."),

("h2", "4.1 Verificação técnica"),
("p", "A verificação técnica confirma que o código cumpre os requisitos que se conseguem testar de forma automática. "
      "Os resultados da Tabela 16 foram obtidos na versão entregue, com os comandos de teste do repositório; o "
      "peso dos ecrãs foi medido no navegador do Playwright, a 390 px."),
("tab", "Tabela", "Resultados da verificação técnica",
   ["Verificação", "Critério", "Resultado"],
   [["Testes do servidor (pytest)", "Todos passam", "109 de 109"],
    ["Matriz de permissões", "Todas as rotas da API têm regra para os 4 papéis", "Passa"],
    ["Testes ponta a ponta (Playwright)", "Fluxos da aceleradora, da startup, do investidor e da conta", "5 de 5"],
    ["Acessibilidade (axe, WCAG 2.2 AA)", "0 violações graves ou críticas, a 390 e a 1280 px", "0 em 8 verificações"],
    ["Exemplo da HU19", "% comprometida de 37,5", "37,5%"],
    ["Imutabilidade", "A base de dados recusa alterar uma actualização publicada e o registo de auditoria", "Passa"],
    ["Análise estática (Ruff, ESLint)", "Sem erros", "Sem erros"],
    ["Peso inicial dos ecrãs (RNF01)", "HTML e CSS ≤ 50 KB; JavaScript inicial ≤ 120 KB, comprimidos",
     "9,4 a 13,1 KB; 142,5 a 148,8 KB (não cumpre)"]],
   "Autor (2026).", [5.4, 7.4, 3.2], {"small": True}),
("p", "O desempenho em rede lenta (RNF01) tem duas partes. A primeira é o peso do que cada ecrã descarrega. Foi "
      "medida na versão de produção, com a compressão gzip do servidor, em quatro ecrãs: a página inicial, a "
      "entrada, as sugestões do investidor e o *pipeline* da startup. O HTML e o CSS ficam entre 9,4 e 13,1 KB, "
      "dentro do limite de 50 KB. O JavaScript inicial fica entre 142,5 e 148,8 KB, acima do limite de 120 KB, "
      "pelo que esta parte do requisito não é cumprida. A causa está na base comum a todos os ecrãs: o React e o "
      "*router* do Next.js somam 131,3 KB comprimidos, antes de qualquer código da aplicação, que acrescenta entre 11 e "
      "20 KB por ecrã. Nem o empacotador webpack nem a compressão brotli baixam o total para menos de 120 KB, pelo que "
      "o limite, definido antes da escolha da *stack*, não é compatível com ela. A segunda parte, a primeira pintura de conteúdo em menos de "
      "3 segundos numa rede móvel lenta, exige uma medição com o Lighthouse e ainda não foi feita. "
      "{{[RESULTADO A INSERIR: primeira pintura de conteúdo em «Slow 4G», medida com o Lighthouse.]}} A "
      "disponibilidade (RNF10) só se mede com a plataforma alojada."),

("h2", "4.2 Protocolo da avaliação com utilizadores"),
("p", "A avaliação segue as tarefas e as métricas da base de experiência do utilizador, adaptadas ao que o código "
      "implementa. Cada sessão dura entre 45 e 60 minutos e tem cinco momentos: consentimento, entrevista de "
      "contexto, tarefas com pensamento em voz alta, questionário SUS e entrevista de validação. As sessões usam "
      "apenas dados fictícios, de preferência no telemóvel do participante. O guião e o termo de consentimento "
      "estão no Apêndice B."),
("p", "Em cada tarefa registam-se o resultado (sucesso, sucesso com ajuda ou falha), o tempo, os erros críticos e "
      "não críticos e a facilidade percebida, numa escala de 1 a 7. A usabilidade percebida mede-se com o "
      "questionário SUS (Brooke, 1996), na versão em português europeu validada por Martins *et al.* (2015). A "
      "pontuação de cada participante calcula-se pela regra de Brooke (itens ímpares menos 1, 5 menos os itens "
      "pares, soma multiplicada por 2,5) e apresenta-se a média, o mínimo e o máximo por papel. Como referência, "
      "Bangor, Kortum e Miller (2008) obtiveram uma média de 70,1 numa amostra de 2324 questionários. Com amostras "
      "desta dimensão não se tiram conclusões estatísticas: os valores descrevem o grupo testado."),
("p", "O SUS mede a usabilidade percebida, não a confiança. Por isso, a redução da assimetria de informação "
      "avalia-se com três métricas de compreensão: do sinal (o participante nomeia quem validou e quando), da "
      "compatibilidade (explica por que critério uma startup aparece) e da privacidade (distingue o que o investidor "
      "vê antes e depois de a startup aceitar). O Quadro 13 lista as tarefas."),
("tab", "Quadro", "Tarefas da avaliação por papel",
   ["Papel", "Tarefa", "Critério de sucesso"],
   [["Entidade", "A1 Registar a aceleradora e enviá-la para verificação", "Entidade submetida"],
    ["Entidade", "A3 Criar a turma do programa deste ano", "Turma criada com datas"],
    ["Entidade", "A4 Convidar 3 startups, uma por WhatsApp", "2 convites por e-mail e 1 ligação copiada"],
    ["Entidade", "A5 Confirmar a participação de duas startups e recusar um pedido de selo", "2 validações e 1 recusa "
     "com motivo"],
    ["Startup", "S1 Criar a conta da startup e pedir o selo à aceleradora", "Pedido de selo enviado"],
    ["Startup", "S2 Deixar o perfil pronto para os investidores", "Perfil publicado"],
    ["Startup", "S4 Dizer o que o investidor vê antes e depois de aceitar", "Distingue as duas camadas"],
    ["Startup", "S5 Decidir um pedido de acesso e explicar porquê", "Decide e cita um elemento do ecrã"],
    ["Startup", "S7 Registar uma reunião com um investidor de fora", "Investidor de fora em Reunião"],
    ["Startup", "S9 Publicar a actualização do mês", "Actualização publicada"],
    ["Startup", "S10 Dizer quanto da ronda está comprometido e que relação está parada", "Responde às duas perguntas"],
    ["Investidor", "I1 Registar-se e definir o mandato", "Mandato mínimo guardado"],
    ["Investidor", "I2 Escolher a startup que melhor encaixa e explicar porquê", "Cita pelo menos 1 critério"],
    ["Investidor", "I3 Dizer quem confirmou a participação de uma startup e quando", "Entidade e data correctas"],
    ["Investidor", "I4 Pedir acesso a uma startup", "Pedido enviado com nota"],
    ["Investidor", "I7 Mudar o mandato para um sector sem startups e decidir o que fazer", "Usa as compatibilidades "
     "parciais"]],
   "Autor (2026), adaptado da base de experiência do utilizador do projecto.", [2.4, 8.4, 5.2], {"small": True}),
("p", "As metas são: pelo menos 80% de sucesso sem ajuda em cada tarefa; nenhum erro crítico nas tarefas S4, S5, I2 "
      "e I3; mediana da facilidade de pelo menos 5; pelo menos 80% de respostas correctas em cada métrica de "
      "compreensão; e SUS de pelo menos 70 por papel. Estas metas são suposições de partida, definidas antes dos "
      "testes. A Tabela 17 indica os participantes por papel."),
("tab", "Tabela", "Participantes por papel",
   ["Papel", "Participantes", "Sessões presenciais", "Sessões remotas"],
   [["Entidade validadora", R, R, R], ["Startup", R, R, R], ["Investidor", R, R, R], ["Total", R, R, R]],
   "Autor (2026).", [5.2, 3.6, 3.6, 3.6], {"total_row": True, "small": True}),

("h2", "4.3 Resultados dos testes de usabilidade"),
("p", R + " Sucesso, tempo, erros e facilidade por tarefa (Tabela 18); SUS por papel (Tabela 19); problemas "
      "encontrados, classificados pela gravidade, e as correcções feitas."),
("tab", "Tabela", "Sucesso, tempo e facilidade por tarefa",
   ["Tarefa", "Sucesso sem ajuda", "Tempo (mediana)", "Erros críticos", "Facilidade (mediana)"],
   [[t, R, R, R, R] for t in ("A1", "A3", "A4", "A5", "S1", "S2", "S4", "S5", "S7", "S9", "S10", "I1", "I2", "I3", "I4",
                              "I7")],
   "Autor (2026), registos das sessões.", [2.0, 3.6, 3.4, 3.2, 3.8], {"small": True}),
("tab", "Tabela", "Pontuação SUS por papel",
   ["Papel", "n", "Média", "Mínimo", "Máximo"],
   [["Entidade validadora", R, R, R, R], ["Startup", R, R, R, R], ["Investidor", R, R, R, R], ["Todos", R, R, R, R]],
   "Autor (2026), calculado com a regra de Brooke (1996).", [4.8, 1.6, 3.2, 3.2, 3.2], {"total_row": True, "small": True}),

("h2", "4.4 Validação com investidores e aceleradoras"),
("p", "As entrevistas de validação testam as hipóteses de desenho que o inquérito não cobria: os campos do mandato e "
      "os pesos da compatibilidade (o investidor distribui 100 pontos pelos critérios e ordena três cartões de "
      "startups, que se comparam com a ordem do algoritmo), a frase de validação que a aceleradora assina, os marcos "
      "que as aceleradoras aceitam confirmar e a confiança dos investidores na informação validada. A Tabela 20 "
      "compara a distribuição dos 100 pontos com os pesos propostos. " + R),
("tab", "Tabela", "Distribuição dos 100 pontos pelos critérios face aos pesos propostos",
   ["Critério", "Peso proposto", "Média dos investidores", "Diferença"],
   [["Sector", "40", R, R], ["Fase", "25", R, R], ["Valor do cheque", "25", R, R], ["Geografia", "10", R, R],
    ["Risco", "0", R, R]],
   "Autor (2026), entrevistas de validação.", [4.0, 3.6, 4.6, 3.8], {"num_cols": [1], "small": True}),

("h2", "4.5 Compreensão dos sinais, da compatibilidade e da privacidade"),
("p", R + " Percentagem de participantes que nomeiam a entidade e a data de um sinal validado (I3), que explicam a "
      "compatibilidade por pelo menos um critério (I2) e que distinguem as duas camadas do perfil (S4)."),

("h2", "4.6 Discussão"),
("p", "A verificação técnica mostra que as regras de que depende a confiança estão garantidas no código e na base "
      "de dados: um sinal validado tem sempre entidade, pessoa e data; nada da camada privada chega ao investidor "
      "sem consentimento; as acções sensíveis ficam num registo que não se altera; e toda a pontuação se decompõe "
      "em critérios. Isto é condição necessária, mas não suficiente, para que os sinais reduzam a assimetria de "
      "informação: segundo a teoria da sinalização, um sinal só é útil se o receptor o compreender e lhe atribuir "
      "valor (Spence, 1973; Connelly *et al.*, 2011). Essa parte depende das métricas de compreensão e de confiança "
      "da avaliação com utilizadores. " + R),
("p", "A avaliação tem limitações conhecidas: a amostra é pequena e de conveniência; as sessões usam dados fictícios "
      "e decorrem numa única ronda, sem uso prolongado; e a relevância das sugestões só poderá ser medida com "
      "pedidos de acesso reais, quando a plataforma estiver em uso."),
]
