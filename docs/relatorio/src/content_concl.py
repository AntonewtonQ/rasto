# -*- coding: utf-8 -*-
CONCL = [
("h1", "CONCLUSÕES"),
("p", "O trabalho partiu da pergunta: de que forma uma plataforma web baseada em sinais verificáveis por terceiros e "
      "no acompanhamento da relação pode reduzir a assimetria de informação entre startups aceleradas e investidores "
      "em Angola? Para lhe responder, definiram-se seis objectivos específicos, retomados a seguir."),
("al", "a) **Caracterizar o problema.** A literatura e os relatórios sobre o ecossistema mostram um mercado em fase "
       "inicial, com poucas startups financiadas por capital de risco e informação difícil de verificar (Capítulo I). "
       "A teoria da sinalização indica a resposta: sinais que o investidor consiga verificar e que sejam caros de "
       "falsificar."),
("al", "b) **Diagnosticar práticas e necessidades.** O inquérito (n = 24) mostrou que 75,0% dos respondentes não têm "
       "um processo de captação bem estruturado, que mais de metade tem dificuldade frequente em saber a etapa de "
       "cada investidor e em registar reuniões e compromissos, e que a segurança é o requisito de confiança mais "
       "citado (Capítulo II)."),
("al", "c) **Analisar as soluções existentes.** As plataformas analisadas concentram-se no directório de startups e "
       "no primeiro contacto; nenhuma combina sinais confirmados por entidades verificadas com o acompanhamento da "
       "relação no contexto angolano (Capítulo I, Quadro 2)."),
("al", "d) **Especificar e modelar a solução.** Os requisitos, os casos de uso, a arquitectura, o modelo de dados e o "
       "algoritmo de compatibilidade foram especificados e estão descritos no Capítulo III, com as regras de confiança "
       "levadas para a própria base de dados."),
("al", "e) **Implementar o protótipo.** O produto mínimo viável foi implementado com Next.js, Django e PostgreSQL e "
       "cobre os quatro papéis: verificação das entidades, turmas e selos, perfil da startup em duas camadas, mandato "
       "e sugestões explicadas, pedido de acesso consentido, *pipeline* com indicadores e lembretes, e actualizações "
       "mensais. Ficaram por implementar os marcos declarados com validação (RF14), as notificações na aplicação "
       "(RF32) e a exportação e eliminação dos dados pelo titular (RF35)."),
("al", "f) **Avaliar e validar.** " + "{{[RESULTADO A INSERIR: resultados dos testes de usabilidade, do SUS e das "
       "entrevistas de validação (Capítulo IV).]}}"),
("p", "Em resposta à pergunta de partida, o trabalho mostra que é possível construir uma plataforma em que cada sinal "
      "mostrado ao investidor indica quem o confirmou e quando, em que a informação privada da startup só circula com "
      "o seu consentimento e em que a relação continua registada depois do primeiro contacto. Se estes mecanismos "
      "reduzem de facto a assimetria de informação depende de os utilizadores compreenderem e confiarem nos sinais. "
      "{{[RESULTADO A INSERIR: o que a avaliação mostrou sobre a compreensão e a confiança.]}}"),
("p", "As principais limitações são a amostra pequena e de conveniência do inquérito e da avaliação, a ausência de "
      "uso real prolongado da plataforma, os pesos da compatibilidade e as métricas por fase ainda por validar com "
      "mais investidores, e a dependência de as aceleradoras aderirem à plataforma, sem as quais não há sinais "
      "validados."),

("h2", "Trabalhos futuros"),
("al", "a) Marcos declarados pela startup e confirmados pela aceleradora (RF14), para alargar os sinais para além da "
       "participação num programa;"),
("al", "b) Exportação e eliminação dos dados pelo titular e definição dos prazos de retenção (RF35), antes da entrada "
       "em produção com dados reais;"),
("al", "c) Notificações dentro da aplicação e, eventualmente, por WhatsApp ou SMS;"),
("al", "d) Funcionamento sem rede no *pipeline*, com os movimentos guardados no aparelho e enviados quando a rede "
       "voltar, e arrastar no Kanban só com o teclado;"),
("al", "e) Validadores de nível intermédio (mentores, investidores) e básico (clientes, parceiros), com pesos "
       "diferentes na confiança;"),
("al", "f) Pesos da compatibilidade personalizados por investidor e medição da relevância das sugestões com pedidos "
       "reais;"),
("al", "g) Cofre de documentos com controlo de acesso, em substituição das ligações externas;"),
("al", "h) Painel da aceleradora com os resultados de captação agregados por turma, com o consentimento das "
       "startups;"),
("al", "i) Aplicação nativa para telemóvel, a partir da mesma API."),
]
