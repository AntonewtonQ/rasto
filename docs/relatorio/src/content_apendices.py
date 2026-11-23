# -*- coding: utf-8 -*-
# Apêndices. O B resume docs/testes/ronda-1/ (guião, fichas e termo); o C descreve os ecrãs que o código tem.
APPX = [
("h1", "APÊNDICE A — QUESTIONÁRIO DO INQUÉRITO"),
("p", "{{[A INSERIR: questionário completo, tal como foi aplicado em Fevereiro de 2026, sem respostas individuais.]}}"),

("h1", "APÊNDICE B — GUIÃO DAS SESSÕES DE TESTE E TERMO DE CONSENTIMENTO"),
("h2", "B.1 Guião da sessão"),
("p", "Cada sessão dura entre 45 e 60 minutos, com um participante de cada vez, de preferência no seu telemóvel, e "
      "usa apenas dados fictícios, repostos antes de cada participante."),
("al", "a) **Boas-vindas e consentimento (5 min).** Explicar que se testa a plataforma e não a pessoa, o que se grava, "
       "onde fica e por quanto tempo, e que pode desistir a qualquer momento. Assinar o termo (B.3)."),
("al", "b) **Entrevista de contexto (7 min).** Entidades: como confirmam hoje a participação num programa e o que as "
       "preocupa em associar o nome a uma startup. Fundadores: o que aconteceu no último contacto com um investidor e "
       "o que nunca partilhariam antes de o conhecer."),
("al", "c) **Tarefas com pensamento em voz alta (28 min).** As tarefas do Quadro 13, lidas em voz alta e entregues por "
       "escrito. Só perguntas neutras; nenhuma ajuda antes de 2 minutos de bloqueio. Depois de cada tarefa, a "
       "facilidade de 1 a 7."),
("al", "d) **Questionário SUS (5 min).** Versão portuguesa de Martins *et al.* (2015)."),
("al", "e) **Entrevista de validação (10 min).** Entidades: a frase de validação e os marcos que aceitariam confirmar. "
       "Fundadores: o que precisariam de ver para aceitar um investidor desconhecido e se as métricas sugeridas servem. "
       "Investidores: campos do mandato, distribuição de 100 pontos pelos critérios, ordenação de três cartões de "
       "startups e confiança na informação (1 a 7)."),
("al", "f) **Fecho (5 min).** «Há alguma coisa que não perguntei e devia ter perguntado?»"),
("p", "Depois de cada sessão, os problemas são classificados pela gravidade e registados sem nomes; os de gravidade "
      "alta são corrigidos antes da sessão seguinte."),
("h2", "B.2 Preparação das tarefas"),
("p", "As tarefas de registo (A1, S1, S2, I1) começam com uma conta nova. As restantes usam contas fictícias criadas "
      "pelo comando de dados de demonstração: uma aceleradora verificada com duas participações pendentes e um "
      "pedido de selo a recusar (A3 a A5); uma startup publicada com um pedido de acesso pendente, investidores de "
      "fora no *pipeline* e uma relação parada (S4 a S10); e duas startups publicadas com sinais validados para o "
      "investidor (I2 a I7)."),
("h2", "B.3 Termo de consentimento informado"),
("p", "**Projecto:** Rasto, plataforma web de gestão e ligação entre startups aceleradas e investidores em Angola. "
      "Trabalho de Conclusão de Curso de Engenharia Informática do ISPTEC. **Investigador:** Antonewton Emanuel "
      "Lungoge Quima. **Orientador:** Sediangani Sofrimento."),
("p", "**O que vai acontecer.** Vai usar um protótipo da plataforma durante cerca de 45 a 60 minutos, a fazer algumas "
      "tarefas e a dizer em voz alta o que pensa. No fim, responde a um questionário curto e a algumas perguntas. "
      "Estamos a avaliar a plataforma, não a si."),
("p", "**Que dados recolhemos e para quê.** O tempo e o resultado de cada tarefa, as respostas aos questionários e "
      "notas do que disser. Servem apenas para avaliar e melhorar a plataforma e para o relatório do TCC. No registo e "
      "no relatório, é identificado só por um código. O protótipo só tem dados fictícios; não lhe pedimos dados reais "
      "da sua organização ou startup."),
("p", "**Gravação (opcional).** Se aceitar, gravamos o ecrã e o áudio da sessão. As gravações ficam com o "
      "investigador e são apagadas depois da defesa do TCC; as transcrições não têm nomes."),
("p", "**Os seus direitos.** A participação é voluntária. Pode desistir a qualquer momento, sem dar explicações, e "
      "pedir que os seus dados sejam apagados, contactando o investigador (Angola, 2011)."),
("p", "☐ Li e compreendi este termo e aceito participar.   ☐ Aceito que a sessão seja gravada (opcional)."),
("p", "Código do participante: ________   Data: ___/___/2026   Assinatura: ______________________________"),

("h1", "APÊNDICE C — MANUAL DE UTILIZAÇÃO"),
("p", "Este manual resume, por papel, o que cada utilizador faz no Rasto. A plataforma funciona no navegador do "
      "telemóvel ou do computador; a navegação mostra só os destinos do papel da conta."),
("h2", "C.1 Startup"),
("al", "a) **Criar conta:** na página inicial, «Criar conta da startup»; indicar o nome da startup, o nome, o e-mail e "
       "uma palavra-passe com pelo menos 12 caracteres."),
("al", "b) **Equipa:** em Conta, «Gerir a equipa», convidar os membros por e-mail; só os fundadores convidam."),
("al", "c) **Selo da aceleradora:** em Perfil, «Gerir selos», escolher a aceleradora e a turma e enviar o pedido. O "
       "selo aparece como validado quando a aceleradora confirmar."),
("al", "d) **Perfil:** em Perfil, preencher sector, fase, província e cidade, resumo e ronda; juntar ligações para "
       "documentos; «Publicar» fica disponível com os 6 campos obrigatórios. «Como o investidor vê» mostra a camada 1."),
("al", "e) **Pedidos de acesso:** em Investidores, separador Pedidos, ler quem pede, a nota e porque encaixa, e "
       "aceitar ou recusar. Em «Com acesso», retirar o acesso quando quiser."),
("al", "f) ***Pipeline*:** em Investidores, separador *Pipeline*, «Mover» cada relação para a etapa certa (no "
       "computador também se pode arrastar); *Soft commit* e seguintes pedem valor e moeda; «Adicionar investidor de "
       "fora» para quem não está na plataforma; abrir a relação para registar contactos ou adiar o lembrete."),
("al", "g) **Actualizações:** em Actualizações, confirmar as métricas pré-preenchidas, escrever os destaques e "
       "«Publicar». Para corrigir, escolher «Correcção à de …»."),
("h2", "C.2 Investidor"),
("al", "a) **Criar conta:** na página de entrada, «Sou investidor»; indicar como investe."),
("al", "b) **Mandato:** em Mandato, escolher pelo menos um sector e uma fase; o cheque e a geografia são opcionais."),
("al", "c) **Sugestões:** em Sugestões, ver as startups compatíveis; «Incluir parciais» mostra as que encaixam em "
       "parte. Cada startup mostra «Porque esta startup», critério a critério."),
("al", "d) **Pedir acesso:** no perfil da startup, escrever uma nota curta e «Pedir acesso». Com o pedido aceite, "
       "aparecem o contacto do fundador, os documentos e as actualizações."),
("al", "e) ***Pipeline*:** em *Pipeline*, mover cada startup pelas etapas e registar contactos; a startup não vê esta "
       "informação."),
("h2", "C.3 Entidade validadora"),
("al", "a) **Registo:** «Sou uma aceleradora»; preencher a entidade, juntar comprovativos (PDF, JPEG ou PNG até 2 MB) e "
       "submeter. Até a administração verificar, só se criam turmas em rascunho."),
("al", "b) **Turmas e convites:** em Turmas, criar a turma com programa, edição e datas; convidar startups por e-mail "
       "ou copiar uma ligação pessoal para enviar por WhatsApp; reenviar ou cancelar convites."),
("al", "c) **Validações:** em Validações, ler a frase que vai ser publicada e confirmar ou recusar com motivo; as "
       "participações podem ser confirmadas em lote. No histórico, retirar uma validação com motivo."),
("al", "d) **Equipa:** em Entidade, o responsável convida e retira membros."),
("h2", "C.4 Administração"),
("al", "a) **Primeira entrada:** activar a autenticação em dois passos, obrigatória para este papel."),
("al", "b) **Verificações:** em Verificações, avaliar os 4 critérios de cada entidade e verificar, pedir informação, "
       "recusar ou suspender."),
("al", "c) **Configuração:** no administrador interno, alterar listas de sectores, fases e geografias, pesos da "
       "compatibilidade, prazos e a taxa de câmbio de referência."),
]
