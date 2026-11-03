# -*- coding: utf-8 -*-
N = "n.r."
CAP1 = [
("h1", "CAPÍTULO I: FUNDAMENTAÇÃO TEÓRICA"),
("p", "Este capítulo reúne os conceitos que sustentam a solução proposta. Começa pelo financiamento das startups e "
      "pelo papel das aceleradoras, passa à assimetria de informação e à teoria da sinalização e termina com as "
      "plataformas de ligação, o contexto angolano e as soluções existentes."),

("h2", "1.1 Startups e ciclo de financiamento"),
("h3", "1.1.1 Conceito de startup"),
("p", "Neste trabalho, entende-se por startup uma empresa jovem, normalmente de base tecnológica, que procura um "
      "modelo de negócio capaz de crescer depressa e que, nas primeiras fases, depende de capital externo para o "
      "validar. A definição é operacional e coincide, no essencial, com a usada nos estudos sobre o ecossistema "
      "angolano, que contam as startups tecnológicas ou activas no país (Kuester; Webster; Wright, 2023)."),
("p", "Em Angola, o conceito ganhou contornos legais em 2026. A proposta de Lei das Startups, aprovada na "
      "generalidade pela Assembleia Nacional a 19 de Março de 2026, por unanimidade, considera startups as empresas "
      "com volume de negócios inferior ao equivalente em kwanzas a 3,5 milhões de dólares e cria um selo de startup "
      "que dá acesso a incentivos fiscais, com mecanismos de certificação, supervisão e transparência "
      "(Assembleia [...], 2026). {{[CONFIRMAR FONTE: votação final global, número e data de publicação da lei.]}}"),

("h3", "1.1.2 Fases e fontes de financiamento"),
("p", "As necessidades de capital de uma empresa mudam à medida que esta cresce. Berger e Udell (1998) descrevem "
      "um ciclo de crescimento financeiro em que estruturas de capital diferentes são adequadas a pontos diferentes "
      "do ciclo, consoante a dimensão e a idade da empresa. Nas primeiras fases, a informação disponível sobre a "
      "empresa é escassa e as fontes de capital são sobretudo próximas dos fundadores; com o crescimento, entram "
      "investidores profissionais."),
("p", "No vocabulário corrente das startups, estas fases designam-se por pré-*seed*, *seed*, Série A e séries "
      "seguintes. A Figura 1 resume as fontes de capital típicas de cada fase, tal como são consideradas neste "
      "trabalho."),
("fig", "fig01.png", "Ciclo de financiamento de uma startup", "Autor (2026), com base em Berger e Udell (1998).", 15.5),
("p", "Os investidores anjo são pessoas que investem capital próprio em empresas em fase inicial. Os fundos de "
      "capital de risco investem capital de terceiros e, quando pertencem a uma empresa não financeira, designam-se "
      "por capital de risco empresarial (CVC). Para os fundadores angolanos, a passagem da fase de ideia para a fase "
      "*seed* é a mais difícil: 32% das startups inquiridas pelo INAPEM e pela Unitel encontravam-se em pré-*seed* "
      "(INAPEM; Unitel, 2023 *apud* Manuel, 2023)."),

("h3", "1.1.3 Processo de captação"),
("p", "O capital de risco desenvolveu práticas próprias para investir em empresas jovens e com pouca informação "
      "pública: a selecção cuidadosa das oportunidades, o investimento faseado e o acompanhamento próximo das "
      "empresas financiadas (Gompers; Lerner, 2001). Do lado da startup, a captação é um processo com etapas que "
      "se repete com cada investidor."),
("p", "Para efeitos deste trabalho, consideram-se as seguintes etapas: identificado, contactado, reunião, "
      "análise, *soft commit*, *term sheet* e fechado ou perdido. O *soft commit* é um compromisso indicativo e não "
      "vinculativo de investir um determinado valor. A *term sheet* é uma proposta escrita com os termos principais "
      "do investimento. Distinguir estas etapas é importante, porque um compromisso indicativo não equivale a capital "
      "recebido."),

("h2", "1.2 Aceleração de startups"),
("p", "As aceleradoras são programas de duração limitada, organizados por turmas, que combinam mentoria e "
      "formação e que terminam normalmente num evento público de apresentação a investidores, o *demo day* "
      "(Cohen; Hochberg, 2014). O desenho destes programas varia bastante entre aceleradoras e essa variação "
      "influencia os resultados das startups que neles participam (Cohen *et al.*, 2019)."),
("p", "Para além da formação, as aceleradoras funcionam como intermediárias de informação. Mayya e Huang (2025) "
      "estudaram o que acontece aos investimentos de capital de risco empresarial quando uma aceleradora entra numa "
      "região. Os autores observaram que estes investidores passam a investir em startups menos próximas do negócio "
      "da empresa-mãe e atribuem o efeito a dois mecanismos: os sinais de qualidade emitidos pelas aceleradoras e a "
      "mentoria que estas prestam. Em termos simples, a selecção e a passagem por um programa dizem ao investidor "
      "algo que ele não conseguiria saber sozinho."),
("p", "Esta função é central para a plataforma proposta. Se a participação num programa é um sinal de qualidade, "
      "então a confirmação dessa participação pela própria aceleradora, com data, é informação útil para o "
      "investidor. É por isso que, no produto mínimo viável, as entidades validadoras são aceleradoras e "
      "universidades verificadas."),

("h2", "1.3 Assimetria de informação e teoria da sinalização"),
("h3", "1.3.1 O mercado de «limões»"),
("p", "Akerlof (1970) mostrou, com o exemplo do mercado de automóveis usados, o que acontece quando o vendedor "
      "conhece a qualidade do bem e o comprador não. O comprador, sem forma de distinguir os bons automóveis dos "
      "maus (os «limões»), está disposto a pagar apenas um preço médio. Os vendedores de automóveis bons, que valem "
      "mais do que esse preço, abandonam o mercado, a qualidade média desce e, no limite, o mercado pode deixar de "
      "funcionar."),
("p", "O financiamento de startups tem esta estrutura. O fundador conhece melhor do que ninguém a tracção, a equipa "
      "e os riscos da empresa, e o investidor depende do que lhe é apresentado. Se não conseguir distinguir as "
      "startups, o investidor desconta o valor de todas ou simplesmente não investe, o que prejudica sobretudo as "
      "melhores."),

("h3", "1.3.2 Sinalização"),
("p", "Spence (1973) propôs uma saída para este problema: a parte mais informada pode emitir um sinal, isto é, "
      "uma característica observável que o receptor usa para inferir a qualidade escondida. Para o sinal ser "
      "credível, o seu custo tem de ser diferente consoante a qualidade de quem o emite; caso contrário, todos o "
      "emitiriam e o sinal deixaria de distinguir. Connelly *et al.* (2011) sistematizaram os elementos da teoria: "
      "o emissor, que detém a informação; o sinal; e o receptor, que tem de interpretar o sinal e decidir."),
("p", "A investigação empírica sobre o financiamento de startups confirma o valor dos sinais. Courtney, Dutta e Li "
      "(2017) mostraram, em campanhas de financiamento colaborativo, que os sinais emitidos pela própria empresa "
      "reduzem a incerteza sobre a qualidade do projecto e a credibilidade do fundador, e que o endosso de terceiros "
      "valida e complementa esses sinais. Yang *et al.* (2023), com dados de 163 startups digitais na China, "
      "concluíram que os sinais fortes, como o número de descargas da aplicação e a reputação do investidor da "
      "ronda anterior, estão positivamente associados ao financiamento por capital de risco, e que os sinais fortes "
      "podem diminuir o efeito dos sinais fracos, como a experiência dos fundadores."),
("p", "Em mercados emergentes, a falta de sinais fiáveis tende a ser compensada por redes pessoais. Kabengele e "
      "Hahn (2025), num estudo de métodos mistos sobre o capital de risco em África, identificaram a localização da "
      "startup, a origem do fundador e as redes internacionais como determinantes do financiamento, e observaram "
      "que os investidores recorrem à proximidade com fundadores de perfil semelhante para compensar o risco "
      "associado a lacunas institucionais. Uma plataforma com sinais verificáveis pode reduzir a dependência dessas "
      "redes, ao tornar a informação acessível a quem não pertence a elas."),

("h3", "1.3.3 Assimetria nos dois sentidos"),
("p", "A literatura citada trata sobretudo da informação que falta ao investidor. Neste trabalho, considera-se que "
      "a assimetria também existe no sentido inverso: a startup desconhece o mandato do investidor, isto é, os "
      "sectores, a fase, o valor do investimento, a geografia e o risco que este aceita. Sem essa informação, a "
      "startup contacta investidores que nunca investiriam na sua fase ou sector. A Figura 2 representa as duas "
      "direcções da assimetria e o papel do terceiro verificado."),
("fig", "fig02.png", "Assimetria de informação nos dois sentidos e papel dos sinais verificáveis",
        "Autor (2026), com base em Akerlof (1970) e Spence (1973).", 14.5),
("p", "A plataforma actua nas duas direcções. Do lado do investidor, separa o que a startup declara do que foi "
      "confirmado por uma entidade verificada. Do lado da startup, torna o mandato do investidor explícito e "
      "explica porque é que cada par é compatível."),

("h2", "1.4 Plataformas de ligação entre startups e investidores"),
("h3", "1.4.1 Mercados de dois lados"),
("p", "Uma plataforma que liga startups e investidores é um mercado de dois lados: o seu valor para cada grupo "
      "depende do número e da qualidade dos participantes do outro grupo. Rochet e Tirole (2003) mostraram que, "
      "nestes mercados, a plataforma tem de atrair os dois lados ao mesmo tempo e que a forma como distribui custos "
      "e benefícios entre eles determina a adesão. Daqui decorre o problema do arranque: nenhum dos lados quer "
      "entrar numa plataforma vazia."),
("p", "Na solução proposta, este problema é tratado por duas vias, desenvolvidas no Capítulo III. As aceleradoras "
      "trazem turmas inteiras de startups com um sinal já confirmável, e cada tipo de utilizador obtém valor mesmo "
      "sem o outro lado: a startup, por exemplo, pode organizar no *pipeline* os investidores que contactou fora da "
      "plataforma."),

("h3", "1.4.2 Plataformas de investidores anjo"),
("p", "Viglialoro *et al.* (2026) analisaram plataformas de investidores anjo através de um estudo de casos "
      "múltiplos e descrevem-nas como um novo modelo de organização do financiamento empreendedor, que combina a "
      "selectividade e a profundidade relacional dos grupos tradicionais de anjos com a escala das plataformas "
      "digitais. Segundo os autores, estas plataformas reduzem as barreiras à entrada de novos investidores e "
      "facilitam a participação de investidores de outros países."),
("p", "Este resultado reforça uma das escolhas da solução proposta: a plataforma não substitui a relação pessoal "
      "entre fundador e investidor, mas organiza-a e torna-a acessível a quem não pertence às redes existentes."),

("h3", "1.4.3 Mandato do investidor e correspondência"),
("p", "O mandato de um investidor é o conjunto de critérios que delimita onde este investe. Neste trabalho, o "
      "mandato é descrito por cinco campos: sectores, fase, valor do investimento por startup (o «cheque»), "
      "geografia e nível de risco. A correspondência entre o mandato e o perfil da startup é calculada por regras "
      "explícitas, com pesos configuráveis, para que cada sugestão possa ser explicada critério a critério."),
("p", "A escolha de regras em vez de modelos de aprendizagem automática tem três razões: o volume de dados do "
      "ecossistema é pequeno, a explicação da sugestão é parte da proposta de confiança e os campos e pesos ainda "
      "têm de ser validados com investidores (Capítulo IV). Acresce que a Lei n.º 22/11 reconhece aos titulares de "
      "dados o direito de não ficarem sujeitos a decisões com efeitos significativos tomadas apenas com base em "
      "tratamento automatizado (Angola, 2011, art. 29.º); as sugestões da plataforma apoiam a decisão humana, não "
      "a substituem."),

("h2", "1.5 Contexto angolano"),
("h3", "1.5.1 Caracterização do ecossistema"),
("p", "Os dados disponíveis sobre o ecossistema angolano provêm de estudos com datas, universos e métodos "
      "diferentes, pelo que os números não são directamente comparáveis. A Tabela 1 reúne os principais "
      "indicadores com a respectiva fonte."),
("tab", "Tabela", "Indicadores do ecossistema angolano de startups, por fonte",
   ["Fonte e ano", "Método", "Indicador"],
   [["Kuester, Webster e Wright (2023), Startup Genome e IFC", "Avaliação do ecossistema, com foco em Luanda",
     "Cerca de 125 startups tecnológicas ou activas; início da fase de activação"],
    ["INAPEM e Unitel (2023 *apud* Manuel, 2023)", "Inquérito a 115 startups (universo de 163; taxa de resposta de 38%)",
     "32% em pré-*seed*; falta de financiamento apontada como ameaça por 62%"],
    ["PNUD ([2024])", "Mapeamento com base em estudos anteriores",
     "Mais de 200 startups identificadas; 2% obtiveram capital de risco"]],
   "Autor (2026), com base nas fontes indicadas.", [5.0, 5.0, 6.0]),
("p", "As diferenças entre as contagens (125, 115 inquiridas num universo de 163, mais de 200) reflectem critérios "
      "de inclusão diferentes e confirmam a observação do PNUD de que é difícil acompanhar com exactidão os volumes "
      "e os números do ecossistema (PNUD, [2024]). O mesmo relatório situa Angola atrás do Botswana, do Malawi, da "
      "Namíbia e da Zâmbia em volume de negócios de investimento."),
("p", "A Figura 3 apresenta as ameaças apontadas pelas startups inquiridas pelo INAPEM e pela Unitel. A falta de "
      "financiamento destaca-se das restantes."),
("fig", "fig03_ameacas.png", "Principais ameaças apontadas pelas startups angolanas",
        "Adaptado de Manuel (2023), com base em INAPEM e Unitel (2023).", 14.0),
("p", "Entre as recomendações da avaliação da Startup Genome contam-se a criação de um «centro de gravidade» em "
      "Luanda que impulsione a ligação local entre os intervenientes, o apoio à formação de investidores anjo e das "
      "suas redes e a criação de um fundo de fundos (Kuester; Webster; Wright, 2023). Uma plataforma de ligação "
      "e acompanhamento contribui para a primeira recomendação no plano digital e pode servir as redes de anjos "
      "referidas na segunda."),

("h3", "1.5.2 Enquadramento legal"),
("p", "Três instrumentos legais condicionam a solução. O Quadro 1 resume o seu estado e as implicações para a "
      "plataforma."),
("tab", "Quadro", "Enquadramento legal e implicações para a plataforma",
   ["Instrumento", "Estado e conteúdo relevante", "Implicação para a plataforma"],
   [["Proposta de Lei das Startups", "Aprovada na generalidade a 19/03/2026, por unanimidade (181 votos). Define "
     "startup por volume de negócios inferior ao equivalente a 3,5 milhões de USD; cria um selo de startup e "
     "incentivos fiscais (Assembleia [...], 2026). {{[CONFIRMAR FONTE: estado final.]}}",
     "O selo poderá, no futuro, ser apresentado como sinal no perfil da startup, depois de confirmado pela entidade "
     "competente."],
    ["Proposta de Lei do Regime Jurídico do Financiamento Colaborativo", "Aprovada na generalidade; adopta apenas o "
     "modelo «tudo ou nada»; supervisão da ANIESA para as modalidades não financeiras (Gonga, 2026).",
     "A plataforma não recolhe nem movimenta fundos e não realiza campanhas de financiamento colaborativo. "
     "{{[CONFIRMAR com aconselhamento jurídico que fica fora do âmbito do regime.]}}"],
    ["Lei n.º 22/11, de 17 de Junho (Lei da Protecção de Dados Pessoais)", "Exige consentimento livre, específico, "
     "explícito e informado ou outra base legal; notificação ou autorização da APD; direitos de informação, acesso, "
     "oposição e rectificação; medidas de segurança; regras para transferências internacionais (Angola, 2011).",
     "Registo de consentimentos, camadas de visibilidade, pedido de acesso consentido, notificação à APD, escolha "
     "do alojamento e direitos dos titulares (Capítulo V)."]],
   "Autor (2026), com base nas fontes indicadas.", [4.0, 6.5, 5.5]),

("h2", "1.6 Soluções existentes"),
("p", "Foram analisadas cinco soluções com funções próximas das da plataforma proposta. A informação provém dos "
      "sítios das empresas e de notícias de lançamento, pelo que descreve funcionalidades declaradas e não "
      "resultados de avaliações independentes."),
("h3", "1.6.1 Investable.Africa"),
("p", "A Investable.Africa abriu a sua versão beta a 28 de Outubro de 2026. Liga startups de todos os 54 países "
      "africanos a investidores e disponibiliza uma base pesquisável com mais de 4 000 entidades investidoras. Os "
      "fundadores criam perfis com problema, solução, tracção, equipa e ronda actual, que a própria empresa verifica "
      "antes de publicar. Os investidores filtram startups por região, país, sector, fase, tipo de ronda e valor, "
      "pedem acesso às salas de dados e podem seguir startups para receber actualizações por e-mail. Os fundadores "
      "pagam 99 USD por mês ou 299 USD por ano para listar o perfil; os investidores usam a plataforma "
      "gratuitamente depois de verificados. A empresa não cobra percentagem sobre a captação nem movimenta fundos "
      "(El Alaoui, 2026). É o concorrente mais directo da solução proposta."),
("h3", "1.6.2 Gust"),
("p", "A Gust apresenta-se como uma plataforma global, em regime de serviço, para fundar, gerir e investir em "
      "empresas de crescimento rápido. Oferece aos investidores ferramentas para acompanhar oportunidades e gerir "
      "contactos e declara ser a plataforma oficial de várias redes de investidores anjo e aceleradoras, com "
      "utilizadores de 192 países (Gust, [20--])."),
("h3", "1.6.3 AngelList"),
("p", "A AngelList descreve-se como um sistema financeiro para os mercados privados. A sua oferta centra-se na "
      "administração de veículos de investimento (fundos de capital de risco, *rolling funds*, *scout funds* e "
      "veículos de investimento específicos), com subscrições digitais e sala de dados (AngelList, [20--]). "
      "Serve sobretudo quem gere e investe através desses veículos."),
("h3", "1.6.4 Pitchwise"),
("p", "A Pitchwise é uma ferramenta de captação orientada para fundadores africanos. Permite criar uma sala de "
      "dados, partilhar a apresentação por uma ligação única e personalizável, controlar o acesso (por exemplo, "
      "pela exigência de e-mail ou pelo bloqueio de descargas) e receber notificações em tempo real quando um documento é aberto, "
      "com estatísticas por diapositivo (Pitchwise, 2024)."),
("h3", "1.6.5 VC4A"),
("p", "A VC4A (*Venture Capital for Africa*) é uma organização em rede, activa desde 2007, cuja plataforma liga "
      "empreendedores africanos a investidores e mentores. Disponibiliza ainda cursos através da VC4A Startup "
      "Academy e um guia de programas e eventos do ecossistema (BMZ Digital.Global, [20--])."),

("h2", "1.7 Comparação das soluções"),
("p", "O Quadro 2 compara as soluções analisadas com a solução proposta segundo os critérios que decorrem dos "
      "problemas identificados na Introdução."),
("tab", "Quadro", "Comparação das soluções existentes com a solução proposta",
   ["Critério", "Investable. Africa", "Gust", "AngelList", "Pitchwise", "VC4A", "Rasto"],
   [["Foco geográfico", "África (54 países)", "Global", N, "Fundadores africanos", "África", "Angola"],
    ["Verificação dos perfis", "Pela própria plataforma", N, N, N, N, "Por terceiros verificados, com nome e data"],
    ["Mandato do investidor e correspondência", "Filtros por região, sector, fase e valor", N, N, N, N,
     "Compatibilidade por regras, com pesos configuráveis e explicação"],
    ["Acesso consentido à informação", "Pedido de acesso à sala de dados", N, "Sala de dados",
     "Controlo de acesso por ligação", N, "Pedido com nota; a startup aceita ou recusa"],
    ["Acompanhamento depois da ligação", "Actualizações por e-mail", "Seguimento de oportunidades e gestão de contactos",
     N, "Notificações de abertura de documentos", N, "*Pipeline*, histórico, actualizações e lembretes"],
    ["Indicadores de captação", N, N, N, "Estatísticas de leitura dos documentos", N,
     "Conversão por etapa, tempo até ao 1.º *soft commit*, % da ronda comprometida"],
    ["Português e kwanzas", N, N, N, N, N, "Sim"]],
   "Autor (2026), com base em El Alaoui (2026), Gust ([20--]), AngelList ([20--]), Pitchwise (2024) e BMZ "
   "Digital.Global ([20--]). Nota: n.r. = não referido nas fontes consultadas, o que não significa que a "
   "funcionalidade não exista.", [3.0, 2.3, 2.3, 1.8, 2.2, 1.5, 2.9], {"small": True}),
("p", "A comparação mostra duas lacunas. Nenhuma das soluções consultadas declara verificação dos perfis por "
      "terceiros identificados; a Investable.Africa, a mais próxima, verifica os perfis ela própria. E o "
      "acompanhamento depois da ligação limita-se, nas fontes consultadas, a actualizações por e-mail, à gestão de "
      "contactos ou a estatísticas de leitura de documentos, sem um *pipeline* com etapas e indicadores de "
      "captação. Nenhuma tem foco em Angola. Estas três lacunas correspondem aos diferenciais da solução proposta."),
]
