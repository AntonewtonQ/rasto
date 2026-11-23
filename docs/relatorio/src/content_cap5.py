# -*- coding: utf-8 -*-
CAP5 = [
("h1", "CAPÍTULO V: SEGURANÇA E PROTECÇÃO DE DADOS"),
("p", "A segurança foi o requisito de confiança mais citado no inquérito (83,3%) e a privacidade surgiu em 37,5% "
      "das respostas (Capítulo II). Para o Rasto, a segurança é também parte do produto: se uma validação pudesse "
      "ser forjada, ou se a camada privada de uma startup chegasse a quem não foi autorizado, a plataforma deixaria "
      "de cumprir a sua proposta. Este capítulo descreve as ameaças consideradas e as medidas implementadas."),

("h2", "5.1 Modelo de ameaças"),
("p", "O Quadro 14 lista as ameaças específicas do domínio, para além das comuns a qualquer aplicação web."),
("tab", "Quadro", "Ameaças do domínio e medidas implementadas",
   ["Ameaça", "Medida"],
   [["Entidade falsa a registar-se como aceleradora para emitir selos", "Verificação manual pela administração com "
     "4 critérios e comprovativos; uma entidade por verificar não convida nem valida; a administração pode suspender"],
    ["Validação falsa ou alterada depois de emitida", "Só a entidade da turma valida; a frase validada fica guardada tal "
     "como foi vista; a validação regista pessoa e data; a retirada exige motivo e fica na auditoria"],
    ["Startup a pedir selo a uma turma em que não participou", "Só turmas de entidades verificadas; um pedido por "
     "turma; a recusa impede novo pedido"],
    ["Fuga da camada 2 (contacto, documentos, actualizações)", "Pedido de acesso consentido; o endereço dos "
     "documentos nunca sai na resposta ao investidor; redireccionamento que confirma o acesso e regista a abertura"],
    ["Pedidos de acesso repetidos a uma startup que recusou", "Um pedido pendente por par; 90 dias de bloqueio "
     "depois de recusa ou expiração"],
    ["Enumeração de convites ou de objectos", "*Tokens* aleatórios de 32 bytes guardados só como *hash*, de uso "
     "único e com prazo; identificadores UUID; resposta 404 fora do âmbito"],
    ["Alteração silenciosa de dados sensíveis", "Registo de auditoria só de acréscimo, com cadeia de *hash*"]],
   "Autor (2026).", [5.6, 10.4], {"small": True}),

("h2", "5.2 Controlo de acesso"),
("p", "O controlo de acesso tem duas camadas, aplicadas sempre as duas. A primeira é o papel: cada vista da API "
      "declara os papéis que a podem usar, e as restantes recebem 403. A segunda é o objecto: as consultas são feitas "
      "a partir do âmbito do utilizador (por exemplo, as turmas da sua entidade ou as relações do seu lado do "
      "*pipeline*), e um objecto fora desse âmbito responde 404, para não revelar que existe. O Quadro 15 resume a "
      "matriz para os objectos principais."),
("tab", "Quadro", "Matriz de permissões (resumo)",
   ["Objecto · acção", "Startup", "Investidor", "Entidade", "Administração"],
   [["Turma, convite · criar e gerir", "—", "—", "as suas, se verificada", "administrador interno"],
    ["Sinal · validar, recusar, retirar", "—", "—", "das suas turmas", "—"],
    ["Perfil · camada 1", "o seu", "publicados", "—", "administrador interno"],
    ["Perfil · camada 2", "o seu", "com pedido aceite", "—", "—"],
    ["Pedido de acesso · criar, retirar", "—", "os seus", "—", "—"],
    ["Pedido de acesso · decidir, revogar", "dirigidos a si", "—", "—", "—"],
    ["Relação do *pipeline*", "lado da startup", "lado do investidor", "—", "—"],
    ["Pesos, listas, taxa, prazos", "—", "—", "—", "sim"]],
   "Autor (2026).", [4.8, 2.6, 2.8, 3.0, 2.8], {"small": True}),
("p", "Um teste automático percorre todas as rotas da API para os quatro papéis e para um pedido sem sessão. Cada "
      "rota tem de estar associada a uma regra ou fazer parte de uma lista curta de rotas públicas revista à mão; "
      "uma rota nova sem regra faz o teste falhar. O frontend nunca decide permissões: esconde o que o papel não "
      "usa, mas quem recusa é a API."),

("h2", "5.3 Autenticação e sessões"),
("al", "a) **Palavras-passe:** mínimo de 12 caracteres, recusa das mais comuns, das só numéricas e das parecidas "
       "com os dados da conta, sem regras de composição; guardadas com Argon2."),
("al", "b) **Força bruta:** 5 falhas por par e-mail e endereço IP bloqueiam novas tentativas durante 15 minutos."),
("al", "c) **Dois passos:** TOTP (M'Raihi *et al.*, 2011) com 10 códigos de recuperação de uso único; opcional para "
       "startups, investidores e entidades e obrigatório para a administração, que sem ele só vê o ecrã de "
       "activação. Activar exige confirmar a palavra-passe."),
("al", "d) **Sessões:** guardadas no servidor; *cookie* `HttpOnly`, `Secure` e `SameSite=Lax`, com o prefixo "
       "`__Host-` em produção; 14 dias de duração e 2 horas para a administração."),
("al", "e) **CSRF:** o Django exige o *token* em todos os pedidos que alteram dados; o frontend envia-o num "
       "cabeçalho."),
("al", "f) **Recuperação:** a ligação vale 1 hora e é de uso único; a resposta é igual quer o e-mail exista ou não."),

("h2", "5.4 OWASP Top 10"),
("p", "O Quadro 16 relaciona os riscos da edição de 2025 do OWASP Top 10 (OWASP Foundation, 2025) com as medidas "
      "implementadas."),
("tab", "Quadro", "Riscos do OWASP Top 10:2025 e medidas no Rasto",
   ["Risco", "Medidas"],
   [["A01 Quebra de controlo de acesso", "Duas camadas (papel e objecto); 404 fora do âmbito; UUID; teste da matriz; "
     "o servidor nunca pede os URLs dos documentos"],
    ["A02 Configuração insegura", "`check --deploy` na integração contínua; HSTS; `X-Frame-Options: DENY`; "
     "`nosniff`; política de *referrer*; administrador interno num caminho próprio e com 2FA"],
    ["A03 Falhas na cadeia de fornecimento de *software*", "Versões fixadas; `pip-audit` na integração contínua; imagens "
     "construídas na integração contínua a partir do repositório"],
    ["A04 Falhas criptográficas", "TLS com HSTS; Argon2; *tokens* guardados como *hash*; cópias de segurança "
     "cifradas; segredos fora do repositório"],
    ["A05 Injecção", "ORM com parâmetros ligados; escape automático do React; política de segurança de conteúdos "
     "sem `unsafe-inline` nem `unsafe-eval`, com *nonce* por pedido; validação de URLs e de ficheiros"],
    ["A06 Desenho inseguro", "Modelo de ameaças do domínio (Quadro 14); estados, prazos e regras na base de dados"],
    ["A07 Falhas de autenticação", "Secção 5.3"],
    ["A08 Falhas de integridade de *software* ou de dados", "Auditoria com cadeia de *hash*; frase validada e "
     "actualizações publicadas imutáveis"],
    ["A09 Falhas de registo e alerta", "Auditoria das acções sensíveis; IP truncado; {{[A FAZER: alertas de erros e "
     "de falhas de entrada repetidas.]}}"],
    ["A10 Tratamento incorrecto de condições excepcionais", "Erros da API num formato único, sem detalhes internos; "
     "transacções que garantem que uma acção e o seu e-mail ficam juntos ou nenhum fica"]],
   "Autor (2026), com base em OWASP Foundation (2025).", [5.0, 11.0], {"small": True}),
("p", "Os comprovativos enviados pelas entidades estão limitados a 2 MB, o tipo (PDF, JPEG ou PNG) é verificado "
      "pelos primeiros bytes do ficheiro e não pela extensão, e são servidos apenas à própria entidade e à "
      "administração."),

("h2", "5.5 Auditoria"),
("p", "As acções sensíveis ficam num registo só de acréscimo: verificação e suspensão de entidades, validação, "
      "recusa e retirada de sinais, convites, decisões e revogações de pedidos de acesso, abertura de documentos, "
      "movimentos no *pipeline*, publicação de actualizações e acções administrativas. Cada registo guarda o actor, a "
      "acção, o objecto, o estado antes e depois (sem palavras-passe nem *tokens*), o endereço IP truncado e a data. "
      "Cada registo guarda também o *hash* do anterior e o seu próprio *hash*, pelo que apagar ou alterar um registo "
      "no meio quebra a cadeia. Um *trigger* na base de dados recusa alterações e eliminações, e o comando "
      "`verificar_auditoria` recalcula a cadeia; o teste mensal de restauro das cópias de segurança corre-o sobre a "
      "cópia restaurada."),

("h2", "5.6 Protecção de dados pessoais"),
("p", "O tratamento segue a Lei n.º 22/11 (Angola, 2011), resumida no Quadro 1. As medidas implementadas e as que "
      "ficam por fazer estão no Quadro 17."),
("tab", "Quadro", "Protecção de dados: medidas implementadas e pendentes",
   ["Tema", "Medida", "Estado"],
   [["Minimização", "Só os dados necessários a cada papel; sem documentos de identificação nem dados de pagamento",
     "Implementado"],
    ["Consentimento", "Registado na criação de cada conta, com a versão do aviso e a data", "Implementado"],
    ["Transparência", "Aviso de privacidade antes de criar conta; «Como o investidor vê»; lista de investidores com "
     "acesso", "Implementado"],
    ["Controlo pelo titular", "A startup decide quem vê a camada 2 e pode revogar", "Implementado"],
    ["Decisões automatizadas", "A compatibilidade só ordena sugestões; quem decide é sempre uma pessoa", "Implementado"],
    ["Dados de terceiros", "Investidores de fora introduzidos pela startup ficam só no seu *pipeline*", "Implementado"],
    ["Acesso, rectificação e eliminação", "Exportação dos dados e eliminação da conta pelo titular", "Pendente"],
    ["Notificação à APD e transferência internacional", "Confirmar antes de usar dados reais e de escolher o país do "
     "servidor {{[CONFIRMAR com o orientador e o texto da lei]}}", "Pendente"],
    ["Retenção", "Cópias de segurança apagadas aos 30 dias; restantes prazos por definir", "Parcial"]],
   "Autor (2026).", [3.8, 9.4, 2.8], {"small": True}),
("p", "Durante o trabalho, todas as demonstrações e sessões de teste usam dados fictícios, criados por um comando "
      "próprio, pelo que não houve tratamento de dados pessoais reais na plataforma."),

("h2", "5.7 Cópias de segurança"),
("p", "Uma cópia diária da base de dados e dos comprovativos é cifrada com AES-256 (GnuPG, chave guardada fora do "
      "repositório) e acompanhada do seu *hash* SHA-256; as cópias com mais de 30 dias são apagadas, o que mantém a "
      "coerência com a eliminação de dados. Um *script* de teste restaura a cópia mais recente num contentor "
      "descartável e verifica a cadeia da auditoria, e deve correr todos os meses. O envio das cópias para outro "
      "fornecedor fica para a implantação em produção (Capítulo VI)."),
]
