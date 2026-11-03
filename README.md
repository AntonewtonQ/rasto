# Rasto

Plataforma web de gestão e ligação entre startups aceleradas e investidores em Angola, com sinais validados por
entidades verificadas.

Trabalho de Conclusão de Curso de Engenharia Informática, Instituto Superior Politécnico de Tecnologias e Ciências
(ISPTEC). Autor: Antonewton Emanuel Lungoge Quima. Orientador: Sediangani Sofrimento. Entrega: 30 de Novembro de 2026.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| [`backend/`](backend/) | Django 5.2 + Django REST Framework: API JSON (`/api/v1/`), autenticação (`/_allauth/`), regras de negócio, permissões, auditoria, e-mail, testes |
| [`frontend/`](frontend/) | Next.js 16: todos os ecrãs |
| [`docs/`](docs/) | Documentação: [produto](docs/produto/), [marca](docs/marca/), [técnica](docs/tecnica/base-tecnica-rasto.md) e [relatório do TCC](docs/relatorio/) |
| [`infra/`](infra/) | Configuração do Caddy (TLS e encaminhamento) |
| `compose.yml` | Contentores: base de dados, backend, tarefas agendadas, frontend e Caddy |
| `.github/workflows/` | Integração contínua |

## Arquitectura

```
Navegador ──HTTPS──▶ Caddy ──/api, /_allauth, /saude──▶ Django (backend) ──▶ PostgreSQL
                         └──── tudo o resto ─────────▶ Next.js (frontend) ──▶ Django (com o cookie da sessão)
```

O navegador vê uma só origem, por isso as sessões ficam em *cookie* `HttpOnly` com CSRF, sem *tokens* no
navegador. As regras de negócio e as permissões estão só no Django. Detalhes na
[base técnica](docs/tecnica/base-tecnica-rasto.md), secção 1.5.

## Correr em desenvolvimento

Pré-requisitos: Python 3.12+, Node.js 24, Docker.

```bash
# Base de dados (PostgreSQL 16 na porta 5433)
docker compose up -d db

# Backend (http://127.0.0.1:8000)
cd backend
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
cp .env.exemplo .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py semear_demo     # dados fictícios para demonstração
.venv/bin/python manage.py runserver 8000

# Frontend (http://localhost:3000), noutra consola
cd frontend
npm install
npm run dev
```

Em desenvolvimento, o Next.js encaminha `/api` e `/_allauth` para o Django.

Contas criadas pelo `semear_demo` (palavra-passe `demonstracao-rasto-2026`; todos os nomes são fictícios):

| Conta | Papel |
|---|---|
| `admin@demo.rasto` | Administração (pede a activação da 2FA na primeira entrada) |
| `gestora@kalandula.demo` | Entidade verificada |
| `centro@universidade.demo` | Entidade à espera de verificação |
| `nadia@kitanda.demo`, `joao@dikanza.demo` | Startups com participação pendente |
| `ana@mbote.demo` | Startup com participação validada |

## Testes

```bash
cd backend && .venv/bin/pytest        # serviços, auditoria, API e matriz de permissões
cd frontend && npm run lint && npm run build
```

## Implantação

```bash
cp backend/.env.exemplo backend/.env   # DJANGO_DEBUG=0, DJANGO_SECRET_KEY forte, DOMINIO, SITE_URL=https://DOMINIO, EMAIL_*
docker compose --profile app up -d --build
```

## Relatório do TCC

O relatório é gerado a partir de `docs/relatorio/src/` com `cd docs/relatorio && ./build.sh`. As decisões e os
marcadores por resolver estão em [`DECISOES.md`](docs/relatorio/DECISOES.md) e [`PENDENTES.md`](docs/relatorio/PENDENTES.md).
