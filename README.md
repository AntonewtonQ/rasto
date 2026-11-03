# Rasto

Plataforma web de gestão e ligação entre startups aceleradas e investidores em Angola, com sinais validados por
entidades verificadas (TCC de Engenharia Informática, ISPTEC). Entrega: 30 de Novembro de 2026.

- **Base técnica:** [base-tecnica-rasto.md](base-tecnica-rasto.md) (v1.3: Next.js + Django REST + PostgreSQL).
- **Interface:** [especificacao-interface-rasto.md](especificacao-interface-rasto.md) e [wireframes-rasto.html](wireframes-rasto.html).
- **Relatório do TCC:** [relatorio/](relatorio/) (gerado a partir de `relatorio/src/`).

## Arquitectura

| Peça | Pasta | Função |
|---|---|---|
| Django 5.2 + DRF | raiz (`config/`, `rasto/`) | API JSON em `/api/v1/`, autenticação em `/_allauth/browser/v1/` (allauth *headless*), regras de negócio, permissões, auditoria, e-mail |
| Next.js 16 | `frontend/` | Ecrãs (App Router). Lê a API no servidor com o *cookie* do utilizador e no navegador com CSRF |
| PostgreSQL 16 | contentor `db` | Dados, restrições e *trigger* da auditoria |
| Caddy | `docker/Caddyfile` | TLS; `/api`, `/_allauth`, `/saude` → Django; o resto → Next.js (mesma origem) |

## Desenvolvimento

```bash
# Backend
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
cp .env.exemplo .env
docker compose -f docker/compose.yml up -d db        # PostgreSQL 16 na porta 5433
.venv/bin/python manage.py migrate
.venv/bin/python manage.py semear_demo              # dados fictícios
.venv/bin/python manage.py runserver 8000
.venv/bin/pytest

# Frontend (outra consola) — encaminha /api e /_allauth para o Django em 127.0.0.1:8000
cd frontend && npm install && npm run dev            # http://localhost:3000
```

Contas do `semear_demo` (palavra-passe `demonstracao-rasto-2026`, todos os nomes fictícios):
`admin@demo.rasto` (pede a activação da 2FA na primeira entrada), `gestora@kalandula.demo`,
`centro@universidade.demo`, `nadia@kitanda.demo`, `ana@mbote.demo`.

Tarefas agendadas (contentor `cron`): `expirar_pendentes`, `enviar_emails`, `verificar_auditoria`. Em
desenvolvimento os e-mails aparecem na consola do Django depois de `manage.py enviar_emails`.

Esquema OpenAPI (sessão iniciada): `GET /api/v1/esquema`.

## Implantação

```bash
cp .env.exemplo .env    # DJANGO_DEBUG=0, DJANGO_SECRET_KEY forte, DOMINIO, SITE_URL=https://DOMINIO, EMAIL_*
docker compose -f docker/compose.yml --profile app up -d --build
```
