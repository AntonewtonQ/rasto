# -*- coding: utf-8 -*-
# Capítulo III: descreve o sistema tal como está no código (repositório, commit c44f6e4 e seguintes).
CAP3 = [
("h1", "CAPÍTULO III: SOLUÇÃO PROPOSTA"),
("p", "Este capítulo apresenta o Rasto tal como foi implementado: os papéis, os requisitos, os casos de uso, a "
      "arquitectura, o modelo de dados, o algoritmo de compatibilidade, o pedido de acesso, o acompanhamento da "
      "relação, a interface e a implementação. Sempre que o planeamento e o código divergem, descreve-se o código e "
      "indica-se a diferença."),

("h2", "3.1 Visão geral e papéis"),
("p", "O Rasto é uma plataforma web com quatro papéis. Cada conta tem um só papel, e a navegação, as permissões e "
      "os dados visíveis dependem dele. O Quadro 5 resume o que cada papel faz no produto mínimo viável."),
("tab", "Quadro", "Papéis da plataforma e principais acções",
   ["Papel", "Quem é", "Principais acções"],
   [["Startup", "Fundadores e equipa de uma startup", "Cria a conta e convida a equipa; pede à aceleradora o selo de "
     "participação; edita e publica o perfil; decide os pedidos de acesso; gere o *pipeline*; publica actualizações "
     "mensais"],
    ["Investidor", "Investidor anjo, fundo ou empresa", "Define o mandato; vê as startups compatíveis e a explicação da "
     "pontuação; pede acesso; gere o seu *pipeline*; lê as actualizações das startups que lhe deram acesso"],
    ["Entidade validadora", "Aceleradora ou universidade", "Regista-se e é verificada; cria turmas; convida startups; "
     "valida, recusa ou retira sinais; gere a equipa da entidade"],
    ["Administração", "Equipa da plataforma", "Verifica as entidades; define pesos, listas, prazos e a taxa de câmbio de "
     "referência no administrador interno; lê a auditoria"]],
   "Autor (2026).", [3.0, 4.0, 9.0]),
("p", "Em relação ao planeamento inicial, a entrada das startups mudou. A base de experiência do utilizador previa "
      "que as startups só entrassem por convite da aceleradora. Por decisão do autor, a startup passou a criar a "
      "conta sozinha e a pedir à aceleradora o selo de participação numa das turmas dela; o convite pela aceleradora "
      "continua disponível como alternativa. Também o investidor passou a ter a conta activa logo após o registo, em "
      "vez de esperar por aprovação manual, porque nada da camada privada de uma startup lhe chega sem o "
      "consentimento desta (secção 3.7). As duas alterações estão registadas no histórico de decisões do projecto."),

("h2", "3.2 Requisitos"),
("p", "Os requisitos derivam do diagnóstico do Capítulo II e da base de experiência do utilizador. O Quadro 6 lista "
      "os requisitos funcionais e o estado de cada um no código à data da entrega; o Quadro 7 lista os requisitos "
      "não funcionais e a forma como são verificados."),
("tab", "Quadro", "Requisitos funcionais e estado de implementação",
   ["ID", "Requisito", "Estado"],
   [["RF01", "Entrada por e-mail e palavra-passe, com encaminhamento para a área do papel", "Implementado"],
    ["RF02", "Recuperação da palavra-passe sem revelar se o e-mail existe", "Implementado"],
    ["RF03", "Autenticação em dois passos (TOTP) com códigos de recuperação; obrigatória para a administração",
     "Implementado"],
    ["RF04", "Registo do consentimento na criação de cada conta", "Implementado"],
    ["RF05–RF07", "Registo da entidade em 3 passos; verificação pela administração com 4 critérios; turmas em "
     "rascunho antes da verificação", "Implementado"],
    ["RF08–RF11", "Turmas, convites por e-mail ou por ligação, estados dos convites, entrada da startup pelo convite",
     "Implementado"],
    ["—", "Registo próprio da startup, equipa da startup e pedido do selo à aceleradora (alteração do autor)",
     "Implementado"],
    ["RF12, RF13", "Validação, recusa e retirada de sinais; frase validada guardada tal como a entidade a viu",
     "Implementado"],
    ["RF14", "Marcos declarados pela startup com pedido de validação", "Só no modelo de dados; sem ecrã"],
    ["RF15", "Sinais validados em secção separada e anterior à dos declarados", "Implementado"],
    ["RF16–RF18", "Perfil com 6 campos obrigatórios e completude; ver como o investidor vê; ligações para "
     "documentos", "Implementado"],
    ["RF19, RF20", "Registo do investidor e mandato; sugestões ordenadas e explicadas", "Implementado"],
    ["RF21, RF22", "Pesos, parâmetros e listas configuráveis pela administração", "Parcial: no administrador "
     "interno, sem pré-visualização"],
    ["RF23–RF25", "Pedido de acesso com nota; aceitar, recusar, revogar; bloqueio de 90 dias", "Implementado"],
    ["RF26–RF30", "*Pipeline* privado, investidores de fora, registo de interacções, indicadores, relações paradas",
     "Implementado"],
    ["RF31", "Actualizações mensais com métricas da fase; correcção em vez de edição", "Implementado"],
    ["RF32", "Notificações na aplicação e por e-mail", "Parcial: só e-mail"],
    ["RF33", "Expiração dos pendentes e lembretes", "Implementado"],
    ["RF34", "Prazos e taxa de câmbio de referência definidos pela administração", "Implementado"],
    ["RF35", "Exportação e eliminação dos dados pelo titular", "Não implementado"],
    ["RF36", "Auditoria só de acréscimo das acções sensíveis", "Implementado"]],
   "Autor (2026), a partir da base técnica do projecto e do código.", [2.2, 10.0, 3.8], {"small": True}),
("tab", "Quadro", "Requisitos não funcionais e verificação",
   ["ID", "Requisito", "Como se verifica"],
   [["RNF02", "Telemóvel primeiro: ecrãs utilizáveis a 360 px", "Testes ponta a ponta a 390 px e a 1280 px"],
    ["RNF03", "Acessibilidade WCAG 2.2 AA", "Verificação automática com axe em todos os ecrãs, nos dois tamanhos"],
    ["RNF04", "Nenhum formulário perde dados por falha de rede", "Rascunho no aparelho nos formulários longos; aviso "
     "«Sem ligação»; o movimento no *pipeline* sem rede não fica guardado"],
    ["RNF05", "Controlo de acesso em todos os pontos de entrada", "Teste da matriz de permissões sobre todas as rotas"],
    ["RNF06, RNF07", "TLS, HSTS, Argon2id e bloqueio após falhas", "Configuração verificada por `check --deploy` na "
     "integração contínua"],
    ["RNF08", "Auditoria só de acréscimo com cadeia de *hash*", "*Trigger* na base de dados e comando "
     "`verificar_auditoria`"],
    ["RNF09", "Toda a pontuação se decompõe em critérios", "Testes do domínio da compatibilidade"],
    ["RNF13", "Formatos de Angola (Kz, separador de milhares, dd/mm/aaaa, fuso de Luanda)", "Testes de formatação"],
    ["RNF15", "Implantação com `docker compose` num servidor Linux", "Construção das imagens na integração contínua"]],
   "Autor (2026).", [2.4, 6.6, 7.0], {"small": True}),

("h2", "3.3 Casos de uso"),
("p", "A Figura 9 apresenta os casos de uso por papel. A gestão do *pipeline* é comum à startup e ao investidor, mas "
      "cada um gere o seu, sem ver o do outro."),
("fig", "fig10_casos_uso.png", "Diagrama de casos de uso", "Autor (2026).", 15.0),
("p", "O Quadro 8 descreve os três casos de uso centrais, porque são os que sustentam a confiança e a privacidade: "
      "a confirmação da participação pela aceleradora, o pedido de acesso pelo investidor e a decisão da startup."),
("tab", "Quadro", "Descrição dos casos de uso centrais",
   ["Caso de uso", "Fluxo principal", "Regras e alternativas"],
   [["Pedir e validar o selo de participação", "A startup escolhe uma aceleradora verificada e uma das suas turmas e "
     "envia o pedido com uma nota opcional. A aceleradora vê o pedido na fila de validações e confirma. A startup passa "
     "a fazer parte da turma e o sinal fica validado com o nome da entidade, a pessoa e a data.",
     "Só turmas de entidades verificadas aceitam pedidos; um pedido por turma; a recusa exige motivo e impede novo "
     "pedido à mesma turma; sem resposta em 30 dias, o pedido expira. A aceleradora pode retirar a validação mais "
     "tarde, com motivo."],
    ["Pedir acesso", "O investidor abre o perfil de uma startup publicada, lê a explicação da compatibilidade e envia "
     "o pedido com uma nota até 300 caracteres. A equipa da startup recebe um e-mail.",
     "Exige o mandato mínimo (sector e fase); um pedido pendente por par; a pontuação, a decomposição e a versão dos "
     "pesos ficam guardadas no pedido; o investidor pode retirar o pedido enquanto pendente."],
    ["Decidir o pedido de acesso", "A startup vê quem pede, o mandato declarado, a nota e porque o investidor encaixa, "
     "e aceita ou recusa.", "Aceitar abre a camada 2 e põe a relação nos dois *pipelines* em Contactado; recusar aceita "
     "um motivo opcional, só partilhado se a startup quiser; sem resposta em 14 dias, o pedido expira; recusa e "
     "expiração bloqueiam novo pedido do mesmo investidor durante 90 dias; o acesso pode ser revogado."]],
   "Autor (2026).", [3.4, 6.6, 6.0], {"small": True}),

("h2", "3.4 Arquitectura"),
("p", "A plataforma segue uma arquitectura em duas aplicações servidas na mesma origem (Figura 10). O Django, com o "
      "Django REST Framework, contém as regras de negócio, as permissões, a auditoria e a API JSON (`/api/v1/`). O "
      "Next.js desenha os ecrãs no servidor e envia ao navegador apenas o código dos componentes interactivos. O "
      "Caddy recebe todos os pedidos por HTTPS e encaminha `/api/` e `/_allauth/` para o Django e o resto para o "
      "Next.js, pelo que o navegador vê um só domínio."),
("fig", "fig09_arquitectura.png", "Arquitectura da plataforma", "Autor (2026).", 15.5),
("p", "Esta organização tem três consequências. Primeiro, as sessões continuam num *cookie* `HttpOnly` da mesma "
      "origem, protegido por CSRF, sem *tokens* guardados no navegador. Segundo, o Next.js não decide permissões: "
      "quando desenha uma página no servidor, faz o pedido à API com o *cookie* do utilizador, e a API responde só "
      "com o que esse utilizador pode ver. Terceiro, a mesma API pode servir no futuro uma aplicação nativa."),
("p", "Dentro do Django, o código está dividido por módulos de domínio (organizações, turmas, sinais, startups, "
      "investidores, compatibilidade, acessos, *pipeline*, actualizações, auditoria). As regras vivem nos ficheiros "
      "de serviços de cada módulo; as vistas da API só validam a entrada e chamam esses serviços. Cada vista declara "
      "os papéis que a podem usar, e as consultas são sempre feitas dentro do âmbito do utilizador: um objecto fora "
      "do âmbito responde 404, para não revelar que existe. As tarefas periódicas (expirações, lembretes e envio de "
      "e-mails) correm num contentor próprio, e os e-mails são gravados numa fila na base de dados, na mesma "
      "transacção da acção que os origina. O Quadro 9 lista as tecnologias usadas."),
("tab", "Quadro", "Tecnologias utilizadas",
   ["Camada", "Tecnologia", "Função"],
   [["Interface", "Next.js 16 (React), CSS próprio com *tokens* de cor e tipografia", "Ecrãs desenhados no servidor; "
     "componentes interactivos (formulários, Kanban)"],
    ["API e regras", "Python, Django 5.2 LTS, Django REST Framework", "API JSON, serviços, permissões, administrador "
     "interno"],
    ["Autenticação", "django-allauth (modo *headless*), django-axes, Argon2", "Entrada, recuperação, 2FA por TOTP, "
     "bloqueio após falhas"],
    ["Dados", "PostgreSQL 16", "Restrições `CHECK`, índices parciais e *triggers*"],
    ["Servidor", "Caddy, Gunicorn, Docker Compose", "HTTPS automático, mesma origem, implantação reprodutível"],
    ["Qualidade", "pytest, Playwright, axe-core, Ruff, ESLint, GitHub Actions", "Testes, acessibilidade, análise "
     "estática e integração contínua"]],
   "Autor (2026).", [2.8, 6.4, 6.8], {"small": True}),
("p", "A escolha da *stack* foi do autor. Na comparação inicial da base técnica, a opção recomendada era um só "
      "Django com páginas desenhadas no servidor; a separação entre Next.js e Django acrescenta uma aplicação e um "
      "contrato de API, mas dá componentes interactivos sem recarregar a página e deixa as regras num único sítio."),

("h2", "3.5 Modelo de dados"),
("p", "A Figura 11 apresenta as entidades principais e as suas relações. Todas as chaves primárias são "
      "identificadores aleatórios (UUID), excepto as do registo de auditoria, que precisam de ordem. Os valores "
      "monetários guardam-se como inteiros na moeda em que foram introduzidos (Kz ou USD) e só se convertem para "
      "comparar ou somar, com a taxa de referência e a data visíveis."),
("fig", "fig11_modelo_dados.png", "Modelo de dados simplificado", "Autor (2026), a partir das migrações do código.", 16.0),
("p", "As regras que sustentam a confiança estão na própria base de dados, para que um erro no código não consiga "
      "gravar um estado proibido. O Quadro 10 resume-as."),
("tab", "Quadro", "Regras de integridade garantidas pela base de dados",
   ["Regra", "Mecanismo"],
   [["Os pesos da compatibilidade somam 100; só uma configuração activa", "Restrição `CHECK` e índice único parcial"],
    ["Um só pedido de acesso pendente por par investidor × startup", "Índice único parcial"],
    ["Etapa do *pipeline* entre 1 e 7; relação perdida tem motivo; *soft commit* ou mais tem valor", "Restrições `CHECK`"],
    ["Relação do lado da startup tem investidor da plataforma ou contacto externo", "Restrição `CHECK`"],
    ["Uma ronda aberta por startup; um rascunho de actualização por startup", "Índices únicos parciais"],
    ["Actualização publicada não muda", "*Trigger* que recusa `UPDATE`"],
    ["Registo de auditoria só aceita acréscimos", "*Trigger* que recusa `UPDATE`, `DELETE` e `TRUNCATE`"]],
   "Autor (2026).", [9.0, 7.0], {"small": True}),
("p", "A Figura 12 mostra os estados do sinal e do pedido de acesso. O sinal de participação nasce pendente, quando "
      "a startup aceita um convite ou pede o selo; só a entidade o valida, e um sinal validado pode ser retirado com "
      "motivo. O pedido de acesso tem prazo de 14 dias; a recusa e a expiração bloqueiam um novo pedido do mesmo "
      "investidor durante 90 dias."),
("fig", "fig12_estados.png", "Estados do sinal e do pedido de acesso", "Autor (2026), a partir do código.", 16.0),

("h2", "3.6 Algoritmo de compatibilidade"),
("p", "A compatibilidade mede o encaixe entre o perfil publicado de uma startup e o mandato de um investidor. É uma "
      "função determinística, sem aprendizagem automática, por duas razões: há poucos dados para treinar um modelo e "
      "cada pontuação tem de ser explicada ao utilizador. A função está num módulo de domínio sem dependências do "
      "Django e é testada à parte. A pontuação é a soma, por critério, do peso multiplicado pelo grau de encaixe "
      "(entre 0 e 1), arredondada ao inteiro mais próximo. A Tabela 12 apresenta os pesos de partida e as regras."),
("tab", "Tabela", "Critérios, pesos de partida e regras de encaixe",
   ["Critério", "Peso", "Encaixe total", "Encaixe parcial", "Sem restrição"],
   [["Sector", "40", "Sector da startup no mandato", "—", "—"],
    ["Fase", "25", "Fase no mandato", "0,5 se a fase for vizinha", "—"],
    ["Valor do cheque", "25", "Cheque cobre a parcela típica da ronda", "Sobreposição proporcional",
     "Sem limites: total"],
    ["Geografia", "10", "Província no mandato ou «Angola»", "—", "Sem preferência: total"],
    ["Risco", "0", "Não calculado com peso 0", "—", "—"]],
   "Autor (2026), a partir da configuração activa (versão 1).", [2.8, 1.4, 4.4, 3.8, 3.6], {"num_cols": [1], "small": True}),
("p", "No cheque, a parcela típica que a startup procura é o intervalo entre 10% e 100% do valor da ronda; o encaixe "
      "é a parte desse intervalo coberta pelo intervalo de cheque do investidor. Os valores em Kz convertem-se para "
      "USD com a taxa de referência; sem taxa, o critério fica «sem dados» em vez de assumir um valor. Uma startup é "
      "**compatível** quando o sector encaixa e a pontuação chega a 60; é **parcial** entre 30 e 60, e só aparece se "
      "o investidor o pedir. Os pesos e os limiares são configuráveis e versionados, e cada pedido de acesso guarda a "
      "versão com que foi pontuado."),
("p", "A Tabela 13 mostra o cálculo feito pelo código real para uma startup fictícia dos dados de demonstração "
      "(sector *fintech*, fase *seed*, Luanda, ronda de USD 150 000) e dois mandatos fictícios. Para o primeiro "
      "investidor, a parcela típica é [15 000; 150 000] e o cheque [20 000; 80 000]; a sobreposição é de 60 000 em "
      "135 000, ou seja 0,444, e 25 × 0,444 dá 11 pontos."),
("tab", "Tabela", "Exemplo de pontuação calculado pelo código",
   ["Critério", "Investidor A: cheque USD 20 000–80 000, sem geografia", "Investidor B: cheque USD 50 000–200 000, Luanda"],
   [["Sector (40)", "40", "40"], ["Fase (25)", "25", "25"], ["Valor do cheque (25)", "11", "19"],
    ["Geografia (10)", "10 (sem preferência)", "10"], ["Risco (0)", "0", "0"],
    ["Total", "86 · compatível", "94 · compatível"]],
   "Autor (2026), saída do serviço `explicar` sobre os dados de demonstração.", [4.0, 6.0, 6.0],
   {"num_cols": [1, 2], "total_row": True}),
("p", "O investidor vê sempre a pontuação decomposta, com uma frase em linguagem simples por critério e o aviso de "
      "que a pontuação mede o encaixe com o mandato e não a qualidade da startup (Figura 13). A startup vê a mesma "
      "decomposição quando decide um pedido. A compatibilidade apenas ordena sugestões: nunca aceita, recusa nem "
      "bloqueia nada sozinha."),
("fig", "ecras/i04-porque.png", "Explicação «Porque esta startup» no perfil visto pelo investidor",
 "Autor (2026), dados fictícios.", 7.5),

("h2", "3.7 Pedido de acesso e camadas de visibilidade"),
("p", "O perfil da startup tem duas camadas (Quadro 11). A camada 1 é vista por qualquer investidor autenticado "
      "quando o perfil está publicado. A camada 2 só abre com um pedido de acesso aceite e não revogado."),
("tab", "Quadro", "O que cada camada do perfil mostra",
   ["Camada", "Conteúdo", "Quem vê"],
   [["1", "Nome, sector, fase, província e cidade, resumo, ronda; sinais validados (com a entidade e a data) e, em "
     "secção separada, os declarados", "Investidores autenticados, com o perfil publicado"],
    ["2", "Contacto do fundador, ligações para documentos, actualizações mensais", "Investidores com pedido aceite e "
     "não revogado"],
    ["—", "Sinais pendentes, rascunhos, notas de perda e *pipeline*", "Só a equipa da startup"]],
   "Autor (2026).", [1.6, 9.0, 5.4], {"small": True}),
("p", "Os documentos são ligações externas (por exemplo, numa pasta partilhada) e o investidor nunca recebe o "
      "endereço directo. A ligação que lhe é mostrada aponta para a API, que confirma o acesso, regista a abertura "
      "na auditoria e só então redirecciona, sem enviar o endereço de origem. A Figura 14 mostra o ecrã em que a "
      "startup decide um pedido."),
("fig", "ecras/s06-pedido.png", "Decisão de um pedido de acesso pela startup", "Autor (2026), dados fictícios.", 6.5),

("h2", "3.8 Acompanhamento da relação"),
("p", "Quando a startup aceita um pedido, a relação entra em Contactado nos dois *pipelines*. Cada lado tem o seu e "
      "o outro nunca sabe em que etapa está. As etapas são Identificado, Contactado, Reunião, Análise, *Soft commit* "
      "(compromisso indicativo), *Term sheet* (proposta de termos) e Fechado. Perdido não é uma etapa: a relação "
      "mantém a etapa onde estava, com a data e o motivo da perda, e a perda pode ser desfeita. A partir de *Soft "
      "commit*, a relação exige valor e moeda. A startup pode juntar investidores de fora da plataforma, que só "
      "existem no seu *pipeline*."),
("p", "No computador, o *pipeline* aparece como um quadro Kanban em que as relações se arrastam entre colunas; no "
      "telemóvel, como grupos por etapa (Figura 15). Em ambos, o botão «Mover» abre uma lista de etapas, o que "
      "permite mudar de etapa sem arrastar e só com o teclado. Se duas pessoas da equipa moverem a mesma relação ao "
      "mesmo tempo, a segunda recebe um aviso e vê a versão mais recente, porque cada relação tem um número de "
      "versão verificado a cada alteração."),
("fig", "ecras/s08-pipeline.png", "*Pipeline* da startup no computador, com os indicadores da ronda",
 "Autor (2026), dados fictícios.", 16.0),
("p", "Os indicadores da ronda são calculados a partir do *pipeline*, sem introdução duplicada de dados (Tabela 14). "
      "O exemplo da história de utilizador HU19 da base técnica (compromissos de Kz 18 400 000 e USD 10 000 numa "
      "ronda de USD 80 000, com a taxa de 920 Kz por USD) é verificado por um teste automático, que obtém 37,5%."),
("tab", "Tabela", "Indicadores da ronda",
   ["Indicador", "Definição", "Mostrado quando"],
   [["% da ronda comprometida", "Soma dos valores das relações em *Soft commit* ou além, não perdidas, convertidos "
     "para a moeda da ronda, sobre o valor da ronda", "Há ronda; sem taxa de referência, não se mostra a percentagem"],
    ["Dias até ao 1.º *soft commit*", "Data do primeiro movimento para *Soft commit* ou além menos a data de início da "
     "ronda", "Existe pelo menos um *soft commit*"],
    ["Conversão por etapa", "Relações que passaram da etapa *n* sobre as que chegaram a ela", "Pelo menos 3 relações"],
    ["Relações paradas", "Relações activas sem movimento nem interacção há 21 dias e sem lembrete adiado", "Sempre"]],
   "Autor (2026).", [3.6, 8.0, 4.4], {"small": True}),
("p", "Uma relação parada gera um lembrete por e-mail, que pode ser adiado 7 dias. A startup publica ainda uma "
      "actualização mensal com métricas sugeridas para a sua fase, pré-preenchidas com os valores da actualização "
      "anterior e com a variação. Ao publicar, a actualização segue por e-mail para os investidores com acesso. Uma "
      "actualização publicada não se edita: corrige-se com uma nova, marcada como correcção. Se faltar a "
      "actualização do mês anterior, a startup recebe um lembrete a partir do dia 3 de cada mês. A lista de métricas "
      "por fase é uma suposição de partida, a validar nos testes."),

("h2", "3.9 Interface e identidade visual"),
("p", "A interface foi desenhada primeiro para o telemóvel: até 767 px, a navegação é uma barra inferior com no "
      "máximo cinco destinos por papel; a partir de 768 px passa a calha lateral e, a partir de 1280 px, a barra "
      "lateral. A startup tem Início, Investidores, Actualizações, Perfil e Conta; o investidor tem Início, Sugestões, "
      "*Pipeline*, Mandato e Conta; a entidade tem Início, Turmas, Validações, Entidade e Conta. Os formulários longos "
      "guardam um rascunho no aparelho, e uma sessão expirada devolve o utilizador ao formulário depois de entrar."),
("p", "A identidade segue o guia de marca do projecto: o nome Rasto, a assinatura «Confiança que se verifica», a cor "
      "tinta para o que foi verificado e a laterite para os valores de capital, e um selo próprio para os sinais "
      "validados, que nunca depende só da cor. Os sinais validados aparecem com contorno contínuo e o nome de quem "
      "validou; os declarados, com contorno tracejado e neutro. As Figuras 16 e 17 mostram a fila de validações da "
      "aceleradora e as sugestões do investidor."),
("fig", "ecras/e02-validacoes.png", "Fila de validações da aceleradora", "Autor (2026), dados fictícios.", 7.0),
("fig", "ecras/i03-sugestoes.png", "Sugestões de startups para o investidor", "Autor (2026), dados fictícios.", 7.0),
("p", "Todos os ecrãs passam na verificação automática de acessibilidade com o axe, sem violações graves ou críticas "
      "das regras WCAG 2.2 AA (W3C, 2023), a 390 px e a 1280 px de largura. A verificação manual com leitor de ecrã "
      "não foi feita. {{[A FAZER: verificação com TalkBack num Android.]}}"),

("h2", "3.10 Implementação"),
("p", "O repositório está organizado em `backend/` (Django), `frontend/` (Next.js), `infra/` (Caddy, cópias de "
      "segurança e modo de demonstração) e `docs/` (produto, marca, base técnica e relatório). As principais "
      "decisões de arquitectura estão registadas no Quadro 12."),
("tab", "Quadro", "Principais decisões de arquitectura",
   ["Decisão", "Alternativa rejeitada", "Consequência"],
   [["Monólito modular no Django, com regras nos serviços", "Microsserviços", "Uma base de dados e transacções "
     "simples; fronteiras entre módulos explícitas"],
    ["Next.js e Django na mesma origem", "Django com páginas no servidor; Next.js de ponta a ponta", "Duas aplicações e "
     "um contrato de API; regras só no Django"],
    ["Sessões por *cookie*, sem JWT; 2FA por TOTP", "*Tokens* no navegador; SMS", "Revogação imediata; sem *tokens* "
     "expostos a XSS"],
    ["Regras de integridade no PostgreSQL", "Regras só no código", "Estados proibidos recusados pela base de dados"],
    ["Compatibilidade determinística com pesos versionados", "Aprendizagem automática", "Resultados reproduzíveis e "
     "explicáveis"],
    ["Documentos por ligação externa com redireccionamento auditado", "Cofre de documentos próprio", "A plataforma não "
     "guarda documentos; cada abertura fica registada"],
    ["Tarefas por comandos periódicos e fila de e-mails na base", "Celery e Redis", "Menos um serviço; nenhuma acção "
     "fica sem o seu e-mail"],
    ["Auditoria só de acréscimo com cadeia de *hash*", "Registos em ficheiro", "Prova verificável de que nada foi "
     "alterado"]],
   "Autor (2026), a partir do registo de decisões da base técnica.", [5.6, 4.4, 6.0], {"small": True}),
("p", "O desenvolvimento decorreu por *sprints* (Capítulo II, Tabela 2), e cada incremento só foi integrado com os "
      "testes a passar. A Tabela 15 resume os testes automáticos à data da entrega. O teste da matriz de permissões "
      "percorre todas as rotas da API para os quatro papéis e falha se uma rota nova não tiver regra de acesso; os "
      "testes ponta a ponta e de acessibilidade correm o fluxo completo num navegador real."),
("tab", "Tabela", "Testes automáticos à data da entrega",
   ["Nível", "O que cobre", "Testes"],
   [["Domínio", "Função de compatibilidade; formatos de Angola", "15"],
    ["Serviços com base de dados", "Entidades, turmas, convites, sinais, startups, investidores, pedidos de acesso, "
     "*pipeline*, actualizações, lembretes, auditoria, e-mail, dados de demonstração", "81"],
    ["API", "Fluxos completos com CSRF; matriz de permissões sobre todas as rotas", "13"],
    ["Ponta a ponta", "Fluxos da aceleradora, da startup, do investidor e da conta, num navegador", "5"],
    ["Acessibilidade", "axe em todos os ecrãs, a 390 px e a 1280 px", "8"]],
   "Autor (2026), contagem do pytest e do Playwright.", [3.4, 10.6, 2.0], {"num_cols": [2], "small": True}),
]
