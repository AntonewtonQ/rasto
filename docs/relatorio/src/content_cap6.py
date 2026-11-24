# -*- coding: utf-8 -*-
CAP6 = [
("h1", "CAPÍTULO VI: IMPLANTAÇÃO"),
("p", "Este capítulo descreve como a plataforma é posta a funcionar: os serviços, os ambientes, a integração "
      "contínua, os custos e a operação. A implantação foi desenhada para um único servidor Linux de baixo custo, "
      "com toda a pilha definida num ficheiro do Docker Compose, para que mudar de fornecedor ou de país seja repetir "
      "os mesmos passos."),

("h2", "6.1 Serviços"),
("p", "O Quadro 18 lista os serviços definidos no ficheiro `compose.yml` do repositório. A arquitectura lógica "
      "correspondente está na Figura 10."),
("tab", "Quadro", "Serviços da implantação",
   ["Serviço", "Imagem", "Função"],
   [["db", "PostgreSQL 16", "Base de dados, num volume persistente"],
    ["web", "Construída a partir de `backend/`", "Aplica as migrações e corre o Django com o Gunicorn"],
    ["cron", "A mesma do `web`", "A cada 5 minutos: expira pendentes, envia lembretes e envia a fila de e-mails"],
    ["frontend", "Construída a partir de `frontend/`", "Servidor do Next.js"],
    ["caddy", "Caddy 2", "HTTPS automático, cabeçalhos de segurança e encaminhamento na mesma origem"]],
   "Autor (2026), a partir do ficheiro `compose.yml`.", [2.6, 5.0, 8.4], {"small": True}),
("p", "Os segredos (chave do Django, palavra-passe da base de dados e do e-mail) ficam num ficheiro de ambiente fora "
      "do repositório. O e-mail é enviado por SMTP; os endereços de domínios reservados para testes nunca são "
      "enviados, o que evita mensagens para endereços fictícios dos dados de demonstração."),

("h2", "6.2 Ambientes e integração contínua"),
("p", "Existem três ambientes (Quadro 19). Até haver servidor, as sessões de teste correm num computador pessoal "
      "com a mesma pilha de produção e uma base de dados separada, acessível pela rede local ou por um túnel com "
      "HTTPS; só se usam dados fictícios."),
("tab", "Quadro", "Ambientes",
   ["Ambiente", "Onde", "Dados", "Uso"],
   [["Desenvolvimento", "Computador pessoal; PostgreSQL em contentor", "Fictícios", "Programação e testes"],
    ["Demonstração", "Computador pessoal com a pilha de produção (`infra/demo.sh`), em rede local ou por túnel",
     "Fictícios", "Sessões de teste e revisão do orientador"],
    ["Produção", "Servidor virtual com Docker Compose", "Reais, depois da secção 5.6 resolvida",
     "Piloto com aceleradoras {{[A INSERIR: data de entrada em produção]}}"]],
   "Autor (2026).", [3.0, 6.2, 3.0, 3.8], {"small": True}),
("p", "A integração contínua corre no GitHub Actions a cada envio para o repositório, em quatro tarefas: o servidor "
      "(análise estática com o Ruff, verificação de migrações em falta, testes com PostgreSQL, `check --deploy` e "
      "`pip-audit`); o frontend (ESLint e construção); os testes ponta a ponta e de acessibilidade contra a pilha "
      "completa com dados de demonstração; e a construção das imagens Docker. A versão entregue passa nas quatro "
      "tarefas."),

("h2", "6.3 Custos"),
("p", "A Tabela 21 estima o custo mensal do piloto, com os preços das páginas dos fornecedores a 24 de Novembro de "
      "2026 (Hetzner, [2026]; Backblaze, [2026]). O servidor previsto, o CX23, aparece nessa data com disponibilidade "
      "limitada; os preços mudaram duas vezes em 2026 e têm de ser confirmados antes da contratação."),
("tab", "Tabela", "Custo mensal estimado",
   ["Peça", "Escolha prevista", "Custo mensal"],
   [["Servidor", "Servidor virtual com 2 vCPU, 4 GB de RAM e 40 GB de disco (Hetzner CX23)", "5,99 € sem IVA"],
    ["E-mail", "SMTP de uma conta existente, com limite diário suficiente para o MVP", "0"],
    ["Cópias de segurança fora do servidor", "Backblaze B2 (6,95 USD por TB; os primeiros 10 GB são gratuitos). "
     "Volume do piloto estimado abaixo de 10 GB", "0"],
    ["Domínio", "Subdomínio gratuito no piloto; domínio .ao próprio antes da produção "
     "{{[CONFIRMAR preço no registo .ao]}}", "0"],
    ["Total", "", "5,99 € sem IVA"]],
   "Autor (2026).", [4.0, 8.4, 3.6], {"total_row": True, "small": True}),
("p", "A localização do servidor está por decidir. Um servidor na Europa é mais barato e tem mais oferta, mas implica "
      "transferência internacional de dados pessoais, o que pode exigir autorização da autoridade de protecção de "
      "dados; o alojamento em Angola evita a transferência, mas a oferta e os preços estão por levantar. Para as "
      "sessões com dados fictícios, a questão não se coloca. {{[CONFIRMAR com o orientador antes da produção.]}}"),

("h2", "6.4 Operação"),
("p", "A operação diária assenta em quatro rotinas: as tarefas periódicas do contentor `cron`; a cópia de segurança "
      "diária cifrada; o teste mensal de restauro, que verifica também a cadeia da auditoria; e a actualização das "
      "dependências quando a integração contínua assinala vulnerabilidades. O Django expõe um ponto `/saude` para um "
      "monitor externo de disponibilidade. Ficam por configurar a monitorização de erros da aplicação e os alertas "
      "por falha das tarefas agendadas ou das cópias. {{[A FAZER na implantação em produção.]}}"),
("p", "O primeiro administrador é criado por um comando próprio e tem de activar a autenticação em dois passos na "
      "primeira entrada. As listas de sectores, fases e províncias, os pesos da compatibilidade e os prazos vêm com "
      "valores de partida e podem ser alterados no administrador interno sem mudar o código."),
]
