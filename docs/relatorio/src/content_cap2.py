# -*- coding: utf-8 -*-
def p(n, d=24):
    return f"{n} ({n/d*100:.1f}%)".replace(".", ",")

CAP2 = [
("h1", "CAPÍTULO II: METODOLOGIAS"),
("p", "Este capítulo descreve a metodologia científica e a metodologia de desenvolvimento de software adoptadas e "
      "apresenta a análise do inquérito que serviu de diagnóstico."),

("h2", "2.1 Metodologia científica"),
("h3", "2.1.1 Tipo de pesquisa e abordagem"),
("p", "Trata-se de uma pesquisa aplicada, porque procura resolver um problema concreto com a construção de um "
      "artefacto, e de abordagem mista. A componente quantitativa corresponde ao inquérito de diagnóstico e às "
      "métricas dos testes de usabilidade; a componente qualitativa corresponde às respostas abertas do inquérito e "
      "às entrevistas de validação com investidores e aceleradoras."),
("h3", "2.1.2 Design Science Research"),
("p", "O trabalho segue a *Design Science Research* (DSR), um paradigma de investigação em sistemas de informação "
      "em que o conhecimento é produzido através da construção e da avaliação de artefactos que resolvem problemas "
      "relevantes (Hevner *et al.*, 2004). Peffers *et al.* (2007) propuseram um processo com seis actividades: "
      "identificar o problema e a motivação, definir os objectivos da solução, conceber e desenvolver o artefacto, "
      "demonstrá-lo, avaliá-lo e comunicar os resultados. O processo admite iterações: os resultados da avaliação "
      "podem levar à revisão dos objectivos e do desenho. A Figura 4 mostra como cada actividade foi aplicada neste "
      "trabalho."),
("fig", "fig04.png", "Actividades da Design Science Research aplicadas ao projecto",
        "Autor (2026), com base em Peffers *et al.* (2007).", 13.0),
("h3", "2.1.3 Técnicas e instrumentos"),
("p", "O Quadro 3 relaciona cada objectivo específico com a técnica e o instrumento usados."),
("tab", "Quadro", "Objectivos específicos, técnicas e instrumentos",
   ["Objectivo específico", "Técnica", "Instrumento"],
   [["a) Caracterizar o problema", "Pesquisa bibliográfica e documental", "Artigos revistos por pares, relatórios "
     "institucionais e legislação"],
    ["b) Diagnosticar práticas e necessidades", "Inquérito por questionário", "Questionário em linha com 20 "
     "perguntas (Apêndice A)"],
    ["c) Analisar as soluções existentes", "Análise documental comparativa", "Critérios do Quadro 2; sítios oficiais "
     "e notícias de lançamento"],
    ["d) Especificar e modelar a solução", "Levantamento de requisitos e modelação", "Requisitos, casos de uso, "
     "arquitectura e modelo de dados (Capítulo III)"],
    ["e) Implementar o protótipo", "Desenvolvimento iterativo por *sprints*", "Ferramentas descritas no Capítulo III "
     "{{[A INSERIR]}}"],
    ["f) Avaliar e validar", "Testes de usabilidade; entrevistas semiestruturadas", "Guião de tarefas, questionário "
     "SUS e guião de entrevista (Apêndice B)"]],
   "Autor (2026).", [4.6, 5.2, 6.2]),
("p", "Os testes de usabilidade e as entrevistas de validação realizam-se depois do desenvolvimento dos primeiros "
      "módulos, com dados fictícios. Por essa razão, os campos do mandato do investidor e os pesos da "
      "compatibilidade foram concebidos como configuráveis, para poderem ser ajustados aos resultados da validação "
      "sem alterar o código."),
("h3", "2.1.4 Considerações éticas e protecção de dados"),
("p", "O questionário abria com um pedido de consentimento, e todas as respostas analisadas correspondem a "
      "consentimento afirmativo. Os endereços de e-mail deixados pelos respondentes foram separados das respostas "
      "durante a análise e não são publicados. As respostas abertas são apresentadas por categorias, sem citações "
      "que permitam identificar os autores. Nos testes e nas entrevistas, a gravação depende de consentimento "
      "expresso, e o tratamento dos dados segue a Lei n.º 22/11 (Angola, 2011). {{[CONFIRMAR com o orientador se é "
      "necessária aprovação de uma comissão de ética do ISPTEC.]}}"),

("h2", "2.2 Metodologia de desenvolvimento de software"),
("h3", "2.2.1 Escolha da metodologia"),
("p", "As metodologias tradicionais organizam o desenvolvimento em fases sequenciais e exigem requisitos estáveis "
      "desde o início. Neste projecto, parte dos requisitos depende da validação com investidores e aceleradoras, "
      "que só acontece depois dos primeiros módulos estarem prontos. Optou-se, por isso, por um desenvolvimento "
      "iterativo e incremental, organizado em *sprints* segundo o Scrum."),
("h3", "2.2.2 Desenvolvimento por sprints"),
("p", "No Scrum, o trabalho decorre em *sprints*, eventos de duração fixa de um mês ou menos, dentro dos quais se "
      "realizam o planeamento, as reuniões diárias, a revisão e a retrospectiva. O *Product Backlog* é a lista "
      "ordenada do que é necessário para melhorar o produto e cada *sprint* produz um incremento utilizável, que só "
      "é considerado concluído quando cumpre a definição de «pronto» (Schwaber; Sutherland, 2020)."),
("p", "Sendo um projecto individual, os papéis do Scrum foram adaptados: o autor acumula as funções de "
      "desenvolvimento e de gestão do *backlog*, e o orientador e os participantes da validação desempenham o papel "
      "de partes interessadas nas revisões. A Tabela 2 apresenta o planeamento dos *sprints*, que começa pela "
      "autenticação com papéis e pelo módulo da aceleradora, porque são a base de todos os outros módulos e "
      "permitem trazer as primeiras startups para a plataforma."),
("tab", "Tabela", "Planeamento dos sprints",
   ["Sprint", "Objectivo", "Entregáveis principais", "Período"],
   [["1", "Autenticação com papéis", "Registo, entrada, recuperação de acesso; papéis de startup, investidor, "
     "entidade validadora e administração", "{{[A INSERIR]}}"],
    ["2", "Módulo da aceleradora", "Registo e verificação da entidade; turmas; convites; validação da participação",
     "{{[A INSERIR]}}"],
    ["3", "Perfil da startup e sinais", "Perfil; marcos declarados; pedidos de validação; separação entre validado "
     "e declarado", "{{[A INSERIR]}}"],
    ["4", "Mandato e compatibilidade", "Perfil de mandato; cálculo da compatibilidade; pesos e campos configuráveis",
     "{{[A INSERIR]}}"],
    ["5", "Pedido de acesso consentido", "Pedido com nota; aceitar, recusar e revogar; camadas de visibilidade",
     "{{[A INSERIR]}}"],
    ["6", "Acompanhamento", "*Pipeline*; histórico; actualizações periódicas; indicadores; lembretes",
     "{{[A INSERIR]}}"],
    ["7", "Avaliação e implantação", "Testes de usabilidade; correcções; implantação", "{{[A INSERIR]}}"]],
   "Autor (2026).", [1.4, 4.0, 7.6, 3.0]),

("h2", "2.3 Análise do inquérito como diagnóstico"),
("h3", "2.3.1 Instrumento e procedimento"),
("p", "O inquérito foi aplicado através de um formulário em linha, com 20 perguntas organizadas em blocos: "
      "consentimento, perfil do respondente, processo actual de captação, problemas e percepções, utilidade de uma "
      "plataforma e funcionalidades desejadas, requisitos de confiança e disponibilidade para testar o protótipo "
      "(Apêndice A). As respostas foram recebidas entre 5 e 10 de Fevereiro de 2026. O questionário foi divulgado "
      "entre estudantes, colaboradores e directores de startups, investidores e colaboradores de uma organização do "
      "ecossistema; os canais e o número de pessoas convidadas não foram registados, pelo que não é possível "
      "calcular a taxa de resposta. Segue-se a recomendação de divulgar o instrumento, o período, o recrutamento e "
      "as bases das percentagens (AAPOR, [20--])."),
("p", "Foram recebidas 24 respostas, todas com consentimento, sem duplicações. As percentagens são calculadas "
      "sobre o total de 24 respostas; nas perguntas de escolha múltipla, a soma ultrapassa 100%. Nas escalas, "
      "apresentam-se as distribuições completas e, no texto, a soma das duas categorias extremas quando ajuda à "
      "leitura. As respostas abertas foram classificadas em categorias temáticas, e uma resposta pode pertencer a "
      "mais de uma categoria."),
("p", "O questionário foi concebido para a versão inicial deste projecto, centrada na captação de fundos depois "
      "da aceleração. Mede bem o processo de captação e o acompanhamento, mas não pergunta directamente pelos sinais "
      "verificáveis nem pela compatibilidade entre startups e investidores. Estas duas componentes são validadas nas "
      "entrevistas (Capítulo IV)."),

("h3", "2.3.2 Caracterização dos respondentes"),
("p", f"A maioria dos respondentes identificou-se como fundador ou membro de uma startup acelerada, "
      f"{p(17)}. Responderam ainda {p(3)} investidores, {p(2)} representantes de aceleradoras ou incubadoras e "
      f"{p(2)} pessoas com outro perfil (Tabela 3 e Figura 5). Quase todos actuam há pouco tempo no ecossistema: "
      f"{p(22)} há três anos ou menos. A actividade concentra-se em Angola e, dentro do país, em Luanda, referida "
      f"por {p(23)} dos respondentes."),
("tab", "Tabela", "Perfil dos respondentes",
   ["Característica", "Categoria", "n", "%"],
   [["Perfil principal", "Fundador(a) ou membro de startup acelerada", "17", "70,8"],
    ["", "Investidor(a)", "3", "12,5"],
    ["", "Representante de aceleradora ou incubadora", "2", "8,3"],
    ["", "Outro", "2", "8,3"],
    ["Tempo no ecossistema", "Menos de 1 ano", "11", "45,8"],
    ["", "De 1 a 3 anos", "11", "45,8"],
    ["", "De 4 a 6 anos", "1", "4,2"],
    ["", "Mais de 6 anos", "1", "4,2"],
    ["País de actividade", "Angola", "23", "95,8"],
    ["", "Angola e Portugal", "1", "4,2"],
    ["Província", "Luanda", "20", "83,3"],
    ["", "Luanda e outra província", "3", "12,5"],
    ["", "Malanje", "1", "4,2"]],
   "Autor (2026), dados do inquérito (n = 24).", [4.0, 8.0, 2.0, 2.0], {"num_cols": [2, 3]}),
("fig", "fig05_perfil.png", "Perfil principal dos respondentes", "Autor (2026), dados do inquérito (n = 24).", 13.5),
("p", "Com 3 investidores e 2 representantes de aceleradoras, as respostas descrevem sobretudo o ponto de vista dos "
      "fundadores. As percentagens globais não devem ser lidas como opinião de cada perfil."),

("h3", "2.3.3 Processo actual de captação"),
("p", "Apenas 5 respondentes (20,8%) indicaram que existe no seu contexto um processo de captação bem estruturado. "
      "Os restantes indicaram um processo pouco estruturado (41,7%), a ausência de um processo definido (33,3%) ou "
      "não souberam responder (4,2%) (Tabela 4). Entre os 17 fundadores, 13 indicaram um processo pouco estruturado "
      "ou inexistente."),
("tab", "Tabela", "Existência de um processo estruturado de captação",
   ["Resposta", "n", "%"],
   [["Sim, existe um processo bem estruturado", "5", "20,8"],
    ["Existe um processo, mas pouco estruturado", "10", "41,7"],
    ["Não existe um processo claramente definido", "8", "33,3"],
    ["Não sei / não se aplica", "1", "4,2"],
    ["Total", "24", "100,0"]],
   "Autor (2026), dados do inquérito (n = 24).", [11.0, 2.5, 2.5], {"num_cols": [1, 2], "total_row": True}),
("p", "Quanto aos meios usados para gerir a captação (Tabela 5), metade dos respondentes usa o e-mail e metade usa "
      "folhas de cálculo. Um terço usa documentos partilhados e outro terço já usa uma plataforma específica de "
      "gestão de investimento, o que indica que a ideia de uma ferramenta dedicada não é estranha a parte dos "
      "inquiridos. Metade dos respondentes já conhecia alguma plataforma de captação de fundos para startups "
      "aceleradas."),
("tab", "Tabela", "Meios utilizados para gerir a captação (escolha múltipla)",
   ["Meio", "n", "%"],
   [["E-mail", "12", "50,0"],
    ["Ficheiros Excel ou folhas de cálculo", "12", "50,0"],
    ["Documentos partilhados (Google Drive, OneDrive, etc.)", "8", "33,3"],
    ["Plataforma específica para gestão de investimento", "8", "33,3"],
    ["Ferramentas genéricas de gestão de projecto (Trello, Asana, etc.)", "4", "16,7"],
    ["Outra resposta", "2", "8,3"]],
   "Autor (2026), dados do inquérito (n = 24). A soma ultrapassa 100% por se tratar de escolha múltipla.",
   [11.0, 2.5, 2.5], {"num_cols": [1, 2]}),

("h3", "2.3.4 Percepções sobre o processo"),
("p", "A Tabela 6 apresenta o grau de concordância com cinco afirmações sobre a captação depois da aceleração. "
      "Dois terços dos respondentes (66,7%) discordam de que o processo actual seja bem organizado e 58,3% discordam "
      "de que seja fácil acompanhar o estado das negociações com cada investidor. A medição de resultados divide os "
      "respondentes: 45,8% discordam de que seja fácil e 41,7% não concordam nem discordam. Mais de metade (54,2%) "
      "concorda que há perda de oportunidades por falta de acompanhamento estruturado. Das quatro afirmações que "
      "descrevem o estado actual do processo, a centralização da informação e dos documentos é a única em que a "
      "concordância (37,5%) supera a discordância (33,3%), o que sugere que a centralização documental é um "
      "problema menos sentido do que o acompanhamento."),
("tab", "Tabela", "Concordância com afirmações sobre a captação (n = 24)",
   ["Afirmação", "DT", "D", "NCND", "C", "CT"],
   [["O processo actual de captação é bem organizado", "7", "9", "5", "2", "1"],
    ["É fácil acompanhar o estado das negociações com cada investidor", "3", "11", "5", "4", "1"],
    ["As informações e documentos importantes estão centralizados", "3", "5", "7", "9", "0"],
    ["É fácil medir resultados (tempo até compromisso, taxa de conversão, etc.)", "3", "8", "10", "3", "0"],
    ["Há perda de oportunidades por falta de acompanhamento estruturado", "6", "2", "3", "5", "8"]],
   "Autor (2026), dados do inquérito. Legenda: DT = discordo totalmente; D = discordo; NCND = nem concordo nem "
   "discordo; C = concordo; CT = concordo totalmente. Valores em número de respostas.",
   [8.5, 1.5, 1.5, 1.5, 1.5, 1.5], {"num_cols": [1, 2, 3, 4, 5]}),

("h3", "2.3.5 Frequência dos problemas"),
("p", "A Tabela 7 mostra com que frequência os respondentes enfrentam cinco problemas concretos. O problema mais "
      "frequente é a falta de indicadores claros sobre a captação, enfrentada frequentemente ou quase sempre por "
      "58,3%. Seguem-se a dificuldade em saber em que etapa está cada potencial investidor e a falta de registo de "
      "reuniões, decisões ou *soft commits*, ambas com 54,2%, e a dificuldade em partilhar dados e documentos de "
      "forma segura, com 50,0% (Figura 6)."),
("tab", "Tabela", "Frequência dos problemas na captação (n = 24)",
   ["Problema", "Nunca", "Rara- mente", "Às vezes", "Frequen- temente", "Quase sempre"],
   [["Informação dispersa em vários canais (e-mail, mensagens, ficheiros)", "3", "4", "7", "4", "6"],
    ["Dificuldade em saber em que etapa está cada potencial investidor", "1", "4", "6", "8", "5"],
    ["Falta de registo de reuniões, decisões ou *soft commits*", "3", "2", "6", "7", "6"],
    ["Dificuldade em partilhar dados e documentos de forma segura", "4", "4", "4", "8", "4"],
    ["Falta de indicadores claros sobre o desempenho da captação", "5", "3", "2", "6", "8"]],
   "Autor (2026), dados do inquérito. Valores em número de respostas.",
   [7.0, 1.6, 1.8, 1.8, 2.0, 1.8], {"num_cols": [1, 2, 3, 4, 5]}),
("fig", "fig06_problemas.png", "Problemas enfrentados frequentemente ou quase sempre",
        "Autor (2026), dados do inquérito (n = 24).", 15.0),

("h3", "2.3.6 Utilidade e funcionalidades desejadas"),
("p", "Os respondentes avaliaram a utilidade de cinco funções de uma plataforma digital (Tabela 8). Todas foram "
      "consideradas muito ou extremamente úteis por mais de 70% dos respondentes. A função mais valorizada foi "
      "acompanhar o estado de cada potencial investidor (83,3%), seguida da centralização do *data room* e da partilha "
      "segura de informação (79,2% cada)."),
("tab", "Tabela", "Utilidade atribuída a funções de uma plataforma digital (n = 24)",
   ["Uma plataforma que…", "Nada", "Pouco", "Mode- rada", "Muito", "Extre- ma", "Muito ou extrema (%)"],
   [["Centralize o *data room* das startups aceleradas", "1", "0", "4", "8", "11", "79,2"],
    ["Permita acompanhar o estado de cada potencial investidor", "0", "2", "2", "10", "10", "83,3"],
    ["Registe todas as interacções e decisões", "0", "1", "5", "8", "10", "75,0"],
    ["Gere indicadores como o tempo até ao primeiro compromisso e a taxa de conversão", "0", "1", "6", "5", "12",
     "70,8"],
    ["Apoie a partilha segura de informação entre startups, aceleradoras e investidores", "2", "1", "2", "7", "12",
     "79,2"]],
   "Autor (2026), dados do inquérito. Valores em número de respostas, excepto na última coluna.",
   [6.4, 1.3, 1.3, 1.5, 1.4, 1.5, 2.6], {"num_cols": [1, 2, 3, 4, 5, 6]}),
("p", "Quando tiveram de escolher as funcionalidades mais importantes (Tabela 9 e Figura 7), quase todos "
      "escolheram a gestão do perfil da startup (95,8%), seguida dos painéis de indicadores (70,8%) e do registo de "
      "contactos e reuniões com investidores (58,3%). O *data room* com controlo de acessos ficou em último lugar "
      "(45,8%)."),
("tab", "Tabela", "Funcionalidades consideradas mais importantes (escolha múltipla)",
   ["Funcionalidade", "n", "%"],
   [["Gestão de perfil de startup (dados do negócio, sector, estágio)", "23", "95,8"],
    ["Painéis de indicadores (tempo, taxa de conversão, volume de *soft commits*)", "17", "70,8"],
    ["Registo de contactos e reuniões com investidores", "14", "58,3"],
    ["Gestão de rondas de investimento (valores, condições, *milestones*)", "13", "54,2"],
    ["Registo de *soft commits* e estado das negociações", "13", "54,2"],
    ["Integração com assinatura electrónica (para *term sheets*)", "13", "54,2"],
    ["*Data room* com controlo de acessos", "11", "45,8"]],
   "Autor (2026), dados do inquérito (n = 24). A soma ultrapassa 100% por se tratar de escolha múltipla.",
   [11.0, 2.5, 2.5], {"num_cols": [1, 2]}),
("fig", "fig07_funcionalidades.png", "Funcionalidades consideradas mais importantes",
        "Autor (2026), dados do inquérito (n = 24).", 15.0),
("p", "Há uma diferença a assinalar entre as duas perguntas: a centralização do *data room* é considerada útil por "
      "79,2% quando avaliada isoladamente, mas é a funcionalidade menos escolhida quando os respondentes têm de "
      "dar prioridades. A leitura adoptada é que o *data room* é desejável, mas não prioritário, o que sustenta a "
      "decisão de partilhar documentos por ligação externa no produto mínimo viável e de deixar o armazenamento de "
      "documentos para trabalho futuro."),

("h3", "2.3.7 Criticidade e interesse"),
("p", "Numa escala de 1 a 5, 19 respondentes (79,2%) atribuíram 4 ou 5 à importância de melhorar a organização da "
      "captação e 21 (87,5%) atribuíram 4 ou 5 ao potencial de uma plataforma deste tipo para melhorar o processo "
      "(Tabela 10). O interesse em utilizar a plataforma é elevado: 20 respondentes (83,3%) manifestaram muito "
      "interesse ou interesse máximo (Figura 8). Entre os 17 fundadores, 15 manifestaram muito interesse ou "
      "interesse máximo. Vinte e dois respondentes (91,7%) aceitaram ser contactados para testar o protótipo."),
("tab", "Tabela", "Criticidade do problema e potencial de melhoria (n = 24)",
   ["Pergunta", "1", "2", "3", "4", "5"],
   [["Quão crítico é melhorar a organização da captação no seu contexto", "1", "1", "3", "6", "13"],
    ["Em que medida uma plataforma deste tipo poderia melhorar o processo", "0", "0", "3", "6", "15"]],
   "Autor (2026), dados do inquérito. Escala de 1 (mínimo) a 5 (máximo); valores em número de respostas.",
   [9.0, 1.4, 1.4, 1.4, 1.4, 1.4], {"num_cols": [1, 2, 3, 4, 5]}),
("fig", "fig08_interesse.png", "Interesse em utilizar uma plataforma deste tipo",
        "Autor (2026), dados do inquérito (n = 24).", 14.0),

("h3", "2.3.8 Respostas abertas"),
("p", "Duas perguntas abertas foram classificadas por categorias (Tabela 11). Na pergunta sobre um problema "
      "concreto na captação, responderam 11 pessoas. Os temas mais referidos foram a dificuldade em converter o "
      "interesse em compromisso, com atrasos na decisão, e a dificuldade em demonstrar crescimento ou em identificar "
      "as métricas a apresentar (3 respostas cada). Seguiram-se a falta de resposta ou de clareza na comunicação e "
      "a ausência de fundos ou promessas não cumpridas (2 cada)."),
("p", "Na pergunta sobre os requisitos para confiar numa plataforma deste tipo, responderam as 24 pessoas. A "
      "segurança foi referida por 20 (83,3%), seguida da privacidade e da facilidade de uso (9 cada, 37,5%) e dos "
      "aspectos legais (7, 29,2%). Como o enunciado dava como exemplos a segurança, a privacidade, os aspectos legais "
      "e a facilidade de uso, estas frequências podem estar inflacionadas pelos próprios exemplos. Três respostas "
      "referiram meios de pagamento ou rastreabilidade de desembolsos, funções que ficam fora do âmbito, porque a "
      "plataforma não movimenta dinheiro."),
("tab", "Tabela", "Categorias das respostas abertas",
   ["Pergunta", "Categoria", "n", "% (n = 24)"],
   [["Problema concreto na captação (11 respostas com conteúdo)", "Converter interesse em compromisso; atrasos na decisão", "3", "12,5"],
    ["", "Demonstrar crescimento; identificar as métricas a apresentar", "3", "12,5"],
    ["", "Falta de resposta ou de clareza na comunicação", "2", "8,3"],
    ["", "Ausência de fundos ou promessas não cumpridas", "2", "8,3"],
    ["", "Burocracia e exigência de garantias", "1", "4,2"],
    ["", "Acesso a investidores do seu nicho", "1", "4,2"],
    ["", "Relação com investidores, sem detalhe interpretável", "1", "4,2"],
    ["Requisitos de confiança (24 respostas)", "Segurança", "20", "83,3"],
    ["", "Privacidade", "9", "37,5"],
    ["", "Facilidade de uso e experiência", "9", "37,5"],
    ["", "Aspectos legais e protecção de participações", "7", "29,2"],
    ["", "Transparência, rastreabilidade e fidelidade dos dados", "3", "12,5"],
    ["", "Operações financeiras (fora do âmbito)", "3", "12,5"],
    ["", "Suporte e continuidade", "2", "8,3"],
    ["", "Outras (colaboração, eficiência, acessibilidade, certificações)", "1 cada", "4,2 cada"]],
   "Autor (2026), dados do inquérito. Uma resposta pode pertencer a mais de uma categoria.",
   [4.4, 7.6, 1.6, 2.4], {"num_cols": [2, 3]}),
("p", "A classificação foi feita por regras de palavras-chave definidas para cada categoria, sem um "
      "segundo codificador independente. {{[CONFIRMAR: revisão final das categorias pelo autor.]}}"),

("h3", "2.3.9 Dos dados às decisões de escopo"),
("p", "O Quadro 4 liga os principais resultados do inquérito às decisões tomadas no produto mínimo viável. As "
      "duas componentes que o inquérito não mede, os sinais verificáveis e a compatibilidade, ficam como hipóteses "
      "a validar no Capítulo IV."),
("tab", "Quadro", "Rastreabilidade entre o diagnóstico e as decisões de escopo",
   ["Dado do inquérito", "Necessidade", "Decisão no produto mínimo viável"],
   [["75,0% sem processo bem estruturado (Tabela 4)", "Um processo de captação com etapas definidas",
     "*Pipeline* com etapas predefinidas, de «identificado» a «fechado» ou «perdido», com motivo de perda"],
    ["54,2% com dificuldade frequente em saber a etapa de cada investidor; 83,3% consideram útil acompanhá-la "
     "(Tabelas 7 e 8)", "Ver o estado de cada relação", "Vista de *pipeline* e lembretes de relações paradas"],
    ["54,2% com falta frequente de registo; 58,3% pedem registo de contactos e reuniões (Tabelas 7 e 9)",
     "Registar reuniões, decisões e compromissos", "Histórico da relação; registo de *soft commit* com valor"],
    ["58,3% com falta frequente de indicadores; 70,8% pedem painéis (Tabelas 7 e 9)", "Medir a captação sem "
     "trabalho adicional", "Indicadores calculados a partir do *pipeline*"],
    ["95,8% pedem a gestão do perfil da startup (Tabela 9)", "Apresentar a startup de forma organizada",
     "Perfil verificado, com sinais validados separados dos declarados"],
    ["Segurança 83,3% e privacidade 37,5% (Tabela 11); 50,0% com dificuldade frequente na partilha segura "
     "(Tabela 7)", "Controlar quem vê o quê", "Pedido de acesso consentido, camadas de visibilidade e acesso "
     "revogável (Capítulo V)"],
    ["*Data room* em último lugar, 45,8% (Tabela 9)", "Partilhar documentos sem prioridade de armazenamento",
     "Documentos por ligação externa, só após aceitação; armazenamento como trabalho futuro"],
    ["3 respostas sobre pagamentos ou desembolsos (Tabela 11)", "Fora do âmbito",
     "A plataforma não movimenta dinheiro"],
    ["Não medido pelo inquérito", "Credibilidade dos perfis e encaixe com o investidor",
     "Sinais validados e compatibilidade configurável, a validar nas entrevistas (Capítulo IV)"]],
   "Autor (2026).", [5.6, 4.2, 6.2]),

("h3", "2.3.10 Limitações da amostra"),
("p", "Os resultados do inquérito servem de diagnóstico e não permitem generalizações sobre o ecossistema "
      "angolano, pelas seguintes razões:"),
("al", "a) a amostra é pequena (n = 24) e não probabilística, e a taxa de resposta não pode ser calculada;"),
("al", "b) os perfis são autodeclarados e não foi verificada a função profissional dos respondentes nem a "
       "participação efectiva num programa de aceleração;"),
("al", "c) investidores (3) e aceleradoras (2) estão pouco representados, pelo que as percentagens reflectem "
       "sobretudo o ponto de vista dos fundadores;"),
("al", "d) quase todos os respondentes actuam em Luanda e há três anos ou menos no ecossistema;"),
("al", "e) o questionário foi concebido para a versão inicial do projecto e não mede os sinais verificáveis nem a "
       "compatibilidade;"),
("al", "f) algumas perguntas incluíam exemplos que podem ter orientado as respostas, e as escalas não incluíam a "
       "opção «não se aplica»;"),
("al", "g) as respostas abertas foram classificadas por um único codificador."),
("p", "Estas limitações são compensadas, em parte, pelas entrevistas de validação e pelos testes de usabilidade, "
      "que envolvem investidores e aceleradoras de forma directa."),
]

CAP_PENDENTES = [
("h1", "CAPÍTULO III: SOLUÇÃO PROPOSTA"),
("p", "{{[CAPÍTULO EM ELABORAÇÃO]}}"),
("h1", "CAPÍTULO IV: DISCUSSÃO DOS RESULTADOS"),
("p", "{{[CAPÍTULO EM ELABORAÇÃO]}}"),
("h1", "CAPÍTULO V: SEGURANÇA E PROTECÇÃO DE DADOS"),
("p", "{{[CAPÍTULO EM ELABORAÇÃO]}}"),
("h1", "CAPÍTULO VI: IMPLANTAÇÃO"),
("p", "{{[CAPÍTULO EM ELABORAÇÃO]}}"),
("h1", "CONCLUSÕES"),
("p", "{{[EM ELABORAÇÃO]}}"),
("h2", "Trabalhos futuros"),
("p", "{{[EM ELABORAÇÃO]}}"),
]
