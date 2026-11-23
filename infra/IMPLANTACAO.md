# Implantação do Rasto (staging e produção)

> **Antes de haver servidor:** `infra/demo.sh` põe a pilha de produção a correr neste computador para as sessões de
> teste, em rede local (`infra/demo.sh rede`) ou com um túnel público da Cloudflare (`infra/demo.sh tunel`).
> Ver os comentários no início do *script*.

## Servidor recomendado

| | Recomendação para o TCC |
|---|---|
| **Fornecedor** | Hetzner Cloud (Alemanha ou Finlândia) |
| **Plano** | CX22: 2 vCPU, 4 GB de RAM, 40 GB de disco · cerca de 4–5 EUR/mês **[CONFIRMAR preço no site]** |
| **Sistema** | Ubuntu 24.04 LTS |
| **Domínio** | Para os testes, `<IP>.sslip.io` (gratuito; o Caddy obtém o certificado TLS sozinho). Para produção, um domínio próprio (`rasto.ao` ou alternativa, guia de marca 2.3) |

**Porquê:** cabe toda a pilha (PostgreSQL, Django, Next.js, Caddy) com folga; custo baixo e previsível; Docker
Compose sem adaptações (ADR-10). Alternativas equivalentes: DigitalOcean, Contabo, OVH. O *Always Free* da Oracle
Cloud é gratuito, mas a criação da conta é incerta e não convém depender dela a 3 semanas da entrega.

**Atenção à Lei n.º 22/11 (Dec-T1, base técnica 9.4):** um servidor na Europa implica transferência internacional
de dados pessoais. Para as rondas de teste com **dados fictícios** não há problema. Antes de usar dados reais,
confirmar com o orientador a autorização da APD ou optar por alojamento em Angola **[CONFIRMAR]**.

**E-mail:** Gmail por SMTP (porta 587) com palavra-passe de aplicação. Limite de cerca de 500 destinatários por
dia, suficiente para o TCC. Alguns fornecedores bloqueiam o envio de e-mail em contas novas; confirmar que a porta
587 está aberta no servidor **[CONFIRMAR com o fornecedor]**.

## Primeira instalação

```bash
# 1. No servidor (como root), uma vez
apt update && apt upgrade -y
apt install -y docker.io docker-compose-v2 git ufw
ufw allow OpenSSH && ufw allow 80 && ufw allow 443 && ufw --force enable
adduser --disabled-password rasto && usermod -aG docker rasto

# 2. Como utilizador rasto
git clone <url-do-repositorio> rasto && cd rasto
cp backend/.env.exemplo backend/.env
nano backend/.env          # ver a tabela abaixo
ln -s backend/.env .env    # o Compose lê daqui a palavra-passe da base (contentor db) — tem de ser a mesma do Django
docker compose --profile app up -d --build
docker compose exec web python manage.py criar_admin email@dominio      # pede a palavra-passe
docker compose exec web python manage.py semear_demo                   # só em staging (dados fictícios)
```

| Variável em `backend/.env` | Valor em staging |
|---|---|
| `DJANGO_DEBUG` | `0` |
| `DJANGO_SECRET_KEY` | `python3 -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DJANGO_ALLOWED_HOSTS` | `<IP>.sslip.io` |
| `DOMINIO` | `<IP>.sslip.io` |
| `SITE_URL` | `https://<IP>.sslip.io` |
| `PGPASSWORD` | uma palavra-passe forte (a mesma é usada pelo contentor `db` na primeira criação) |
| `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | conta Gmail e palavra-passe de aplicação |

## Actualizar

```bash
cd rasto && git pull && docker compose --profile app up -d --build
```

As migrações correm ao arrancar o contentor `web`.

## Cópias de segurança

```bash
crontab -e
# Todas as noites às 02:00 (hora do servidor) e teste de restauro no dia 1 de cada mês
0 2 * * *  cd ~/rasto && infra/copias/copiar.sh >> ~/copias.log 2>&1
0 4 1 * *  cd ~/rasto && infra/copias/testar-restauro.sh >> ~/copias.log 2>&1
```

- A chave fica em `infra/copias/.chave` (criada na primeira cópia). **Guarde uma cópia da chave fora do servidor**;
  sem ela as cópias não se abrem.
- As cópias ficam em `infra/copias/arquivo/` durante 30 dias. Para cumprir a base técnica 7.7 (cópia noutro
  fornecedor), copiar a pasta para um armazenamento externo, por exemplo com `rclone` **[a configurar]**.

## Verificações depois de implantar

- `https://<domínio>/saude` responde `{"estado": "ok"}`.
- A entrada da administração pede a activação da 2FA.
- Um convite enviado chega à caixa de correio (ver também a pasta de spam).
- `docker compose logs -f web cron` sem erros.
