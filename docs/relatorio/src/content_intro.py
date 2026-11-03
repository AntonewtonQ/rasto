# -*- coding: utf-8 -*-
INTRO = [
("h1", "INTRODUÇÃO"),
("p", "As startups são empresas jovens que procuram crescer depressa com base num modelo de negócio ainda por "
      "provar e que, por isso, dependem de capital externo nas primeiras fases. Em Angola, este tipo de empresa é "
      "recente. A avaliação do ecossistema realizada pela Startup Genome, em parceria com a IFC, identificou cerca de "
      "125 startups tecnológicas e situou o país no início da fase de activação do ciclo de desenvolvimento de "
      "ecossistemas (Kuester; Webster; Wright, 2023). O mapeamento do PNUD refere que, de mais de 200 startups "
      "identificadas em estudos anteriores, apenas 2% obtiveram capital de risco (PNUD, [2024])."),
("p", "Num mercado assim, o encontro entre quem procura e quem oferece capital é difícil. O investidor não consegue "
      "distinguir com segurança as boas startups das restantes e a startup não sabe que investidores procuram empresas "
      "como a sua. Este problema corresponde ao que a teoria económica designa por assimetria de informação "
      "(Akerlof, 1970) e tem uma resposta conhecida: sinais que a parte menos informada consiga verificar "
      "(Spence, 1973; Connelly *et al.*, 2011). As aceleradoras desempenham parte deste papel, porque a selecção e a "
      "passagem por um programa funcionam como sinal de qualidade (Mayya; Huang, 2025)."),
("p", "Ao mesmo tempo, a ligação entre uma startup e um investidor não termina no primeiro contacto. Segue-se um "
      "processo de reuniões, análise, compromissos indicativos e negociação que, quando não é registado, se perde "
      "entre mensagens e ficheiros. O inquérito realizado para este trabalho, em Fevereiro de 2026, mostrou que a "
      "maioria dos respondentes não dispõe de um processo de captação bem estruturado e que mais de metade enfrenta "
      "com frequência dificuldades em acompanhar o estado de cada investidor."),
("p", "Neste contexto, o presente trabalho propõe o Rasto, uma plataforma web de gestão e ligação entre startups "
      "aceleradas e investidores em Angola. A plataforma assenta em duas ideias: perfis de startups com sinais "
      "confirmados por terceiros verificados, com a indicação de quem confirmou e quando, e o acompanhamento da "
      "relação depois da ligação."),

("h2", "Pergunta de partida"),
("p", "De que forma uma plataforma web baseada em sinais verificáveis por terceiros e no acompanhamento da relação "
      "pode reduzir a assimetria de informação entre startups aceleradas e investidores em Angola?"),

("h2", "Problemas"),
("p", "A partir da literatura, dos relatórios sobre o ecossistema e do inquérito de diagnóstico, identificam-se os "
      "seguintes problemas:"),
("al", "a) **Dificuldade de acesso ao financiamento.** Num estudo do INAPEM e da Unitel com 115 startups, a falta "
       "de financiamento foi a ameaça mais apontada (62%), à frente da regulação (47%) e da tributação (40%) "
       "(INAPEM; Unitel, 2023 *apud* Manuel, 2023). Apenas 2% das startups identificadas pelo PNUD obtiveram "
       "capital de risco (PNUD, [2024])."),
("al", "b) **Informação pouco fiável do lado do investidor.** A informação que a startup apresenta é, na maior "
       "parte, declarada por ela própria. O PNUD assinala que é difícil acompanhar com exactidão os volumes e os "
       "números do investimento em Angola (PNUD, [2024]), o que agrava a dificuldade de comparar oportunidades."),
("al", "c) **Desconhecimento do investidor certo do lado da startup.** Sem informação sobre o mandato de cada "
       "investidor (sectores, fase, valor do investimento), a startup dirige-se a investidores que não investiriam "
       "na sua fase ou sector. Uma das respostas abertas do inquérito refere precisamente a dificuldade de aceder a "
       "investidores do seu nicho."),
("al", "d) **Processo de captação pouco estruturado.** No inquérito, 75,0% dos respondentes indicaram que o "
       "processo de captação no seu contexto é pouco estruturado (41,7%) ou não está definido (33,3%). Metade usa o "
       "e-mail e metade usa folhas de cálculo para gerir a captação."),
("al", "e) **Falta de acompanhamento e de indicadores.** Mais de metade dos respondentes enfrenta com frequência "
       "dificuldades em saber a etapa de cada investidor (54,2%), em registar reuniões, decisões ou compromissos "
       "indicativos (54,2%) e em obter indicadores claros sobre a captação (58,3%); 54,2% concordam que há perda de "
       "oportunidades por falta de acompanhamento estruturado."),

("h2", "Justificativa"),
("p", "A plataforma proposta responde aos problemas anteriores com três escolhas. A primeira é a confiança por "
      "sinais verificáveis: o perfil da startup separa o que é declarado pela própria startup do que foi confirmado "
      "por uma aceleradora ou universidade verificada, com o nome de quem validou e a data. Esta escolha segue a "
      "teoria da sinalização, segundo a qual um sinal só reduz a incerteza se for difícil de falsificar "
      "(Spence, 1973), e a evidência de que endossos de terceiros complementam os sinais emitidos pela própria "
      "empresa (Courtney; Dutta; Li, 2017)."),
("p", "A segunda escolha é o acompanhamento depois da ligação: um *pipeline* com etapas definidas, histórico da "
      "relação, actualizações periódicas, indicadores e lembretes. Responde directamente aos 75,0% sem processo "
      "estruturado e às dificuldades de registo e de medição descritas na alínea e). As plataformas consultadas, "
      "entre as quais a Investable.Africa, lançada em Outubro de 2026, concentram-se no directório de startups, na sala de "
      "dados e no primeiro contacto (El Alaoui, 2026)."),
("p", "A terceira escolha é o foco em Angola: português, valores em kwanzas e dólares, utilização prioritária no "
      "telemóvel e funcionamento em redes lentas. O inquérito sugere que existe procura: 83,3% dos respondentes "
      "manifestaram muito interesse ou interesse máximo em utilizar uma plataforma deste tipo e 22 aceitaram ser "
      "contactados para testar o protótipo. Do ponto de vista académico, o trabalho aplica a teoria da sinalização "
      "à concepção de um sistema de informação num mercado pouco estudado."),

("h2", "Objectivo geral"),
("p", "Desenvolver uma plataforma web de gestão e ligação entre startups aceleradas e investidores em Angola, "
      "baseada em sinais verificáveis por terceiros e no acompanhamento da relação depois do primeiro contacto."),

("h2", "Objectivos específicos"),
("al", "a) Caracterizar o problema da ligação entre startups e investidores em Angola, com base na literatura e "
       "nos dados disponíveis sobre o ecossistema;"),
("al", "b) Diagnosticar as práticas e as necessidades de fundadores, investidores e aceleradoras através de um "
       "inquérito;"),
("al", "c) Analisar as soluções existentes e identificar a lacuna que a plataforma vem preencher;"),
("al", "d) Especificar os requisitos e modelar a solução: casos de uso, arquitectura, modelo de dados e "
       "algoritmo de compatibilidade;"),
("al", "e) Implementar um protótipo funcional do produto mínimo viável;"),
("al", "f) Avaliar a usabilidade do protótipo e validá-lo com investidores e aceleradoras."),

("h2", "Delimitação do problema"),
("h3", "Objecto de estudo"),
("p", "O processo de ligação e de acompanhamento da relação entre startups aceleradas e investidores em Angola."),
("h3", "Campo de acção"),
("p", "A concepção, o desenvolvimento e a avaliação de uma plataforma web de gestão e ligação entre startups "
      "aceleradas, investidores e entidades validadoras (aceleradoras e universidades)."),
("p", "O produto mínimo viável inclui o perfil verificado da startup, com validadores de nível alto (aceleradoras "
      "e universidades verificadas pela administração); o perfil de mandato do investidor; as sugestões por "
      "compatibilidade, calculadas por regras com pesos configuráveis; o pedido de acesso consentido; o "
      "acompanhamento da relação; e o painel da aceleradora. Ficam fora do âmbito o armazenamento de documentos, "
      "as mensagens e a agenda internas, os pagamentos e a movimentação de fundos, o financiamento colaborativo, a "
      "inteligência artificial e a aplicação nativa para telemóvel. A plataforma não movimenta dinheiro."),

("h2", "Organização do trabalho"),
("p", "Para além desta Introdução, o trabalho está organizado em seis capítulos, seguidos das Conclusões."),
("p", "O Capítulo I apresenta a fundamentação teórica: o ciclo de financiamento das startups, o papel das "
      "aceleradoras, a assimetria de informação e a teoria da sinalização, as plataformas de ligação entre startups "
      "e investidores, o contexto angolano e as soluções existentes."),
("p", "O Capítulo II descreve as metodologias científica e de desenvolvimento de software e analisa o inquérito "
      "de diagnóstico, com as limitações da amostra."),
("p", "O Capítulo III apresenta a solução proposta: requisitos, casos de uso, arquitectura, modelo de dados, "
      "algoritmo de compatibilidade, identidade visual, interface e implementação."),
("p", "O Capítulo IV discute os resultados dos testes de usabilidade, da validação com investidores e "
      "aceleradoras e da relevância das sugestões de compatibilidade."),
("p", "O Capítulo V trata da segurança e da protecção de dados pessoais e o Capítulo VI descreve a implantação "
      "da plataforma."),
("p", "Por fim, as Conclusões respondem a cada objectivo específico e apresentam os trabalhos futuros."),
]
