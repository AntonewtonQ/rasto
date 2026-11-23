#!/usr/bin/env bash
# Modo de demonstração neste computador, enquanto não há servidor (sessões de teste com dados fictícios).
#
#   infra/demo.sh rede     participantes na mesma rede Wi-Fi: http://<IP-deste-computador>
#   infra/demo.sh tunel    sessões remotas: endereço público https://….trycloudflare.com (muda a cada arranque)
#   infra/demo.sh repor    volta a pôr a base de demonstração no estado inicial (entre participantes)
#   infra/demo.sh estado   mostra o endereço e o que está a correr
#   infra/demo.sh parar    fecha o túnel e pára os contentores (a base de dados continua)
#
# Usa a pilha de produção (DEBUG=0) e a base de dados «rasto_demo», separada da de desenvolvimento.
# Os e-mails saem pela conta configurada em backend/.env; endereços .demo/.test nunca são enviados.
# O túnel põe este computador acessível a partir da Internet: abrir só durante as sessões e fechar a seguir.
set -euo pipefail
cd "$(dirname "$0")/.."
PASTA="infra/demo"
ENV="$PASTA/.env"
LOG_TUNEL="$PASTA/tunel.log"
PID_TUNEL="$PASTA/tunel.pid"
mkdir -p "$PASTA"

ip_local() { hostname -I | awk '{print $1}'; }

gerar_env() {  # $1 = SITE_URL  $2 = anfitrião  $3 = sem_https (0|1)
  local chave
  chave="$(grep -s '^DJANGO_SECRET_KEY=' "$ENV" | cut -d= -f2- || true)"
  [ -n "$chave" ] || chave="$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')"
  {
    echo "# Gerado por infra/demo.sh — não editar à mão; não vai para o Git."
    grep -E '^(EMAIL_HOST|EMAIL_PORT|EMAIL_HOST_USER|EMAIL_HOST_PASSWORD|DEFAULT_FROM_EMAIL)=' backend/.env || true
    echo "DJANGO_DEBUG=0"
    echo "DJANGO_SECRET_KEY=$chave"
    echo "DJANGO_ALLOWED_HOSTS=$2"
    echo "DJANGO_SEM_HTTPS=$3"
    echo "SITE_URL=$1"
    echo "DOMINIO=:80"
    echo "PGDATABASE=rasto_demo"
    echo "PGUSER=rasto"
    echo "PGPASSWORD=rasto"
  } > "$ENV"
  chmod 600 "$ENV"
}

base_demo() {
  docker compose up -d db >/dev/null
  until docker compose exec -T db pg_isready -U rasto >/dev/null 2>&1; do sleep 1; done
  if ! docker compose exec -T db psql -U rasto -d postgres -Atc "select 1 from pg_database where datname='rasto_demo'" | grep -q 1; then
    docker compose exec -T db createdb -U rasto rasto_demo
  fi
}

arrancar() {
  base_demo
  RASTO_ENV="$ENV" docker compose --profile app up -d --build --force-recreate web cron frontend caddy >/dev/null 2>&1
  echo -n "A arrancar"
  until curl -s -o /dev/null -w '%{http_code}' http://localhost/saude 2>/dev/null | grep -q 200; do echo -n "."; sleep 2; done
  echo
  if ! RASTO_ENV="$ENV" docker compose exec -T web python manage.py shell -c \
      "from rasto.contas.models import Utilizador as U; import sys; sys.exit(0 if U.objects.filter(email='admin@demo.rasto').exists() else 1)" >/dev/null 2>&1; then
    RASTO_ENV="$ENV" docker compose exec -T web python manage.py semear_demo | tail -7
  fi
}

parar_tunel() {
  if [ -f "$PID_TUNEL" ]; then kill "$(cat "$PID_TUNEL")" 2>/dev/null || true; rm -f "$PID_TUNEL"; fi
}

cloudflared_bin() {
  if command -v cloudflared >/dev/null; then command -v cloudflared; return; fi
  local b="$HOME/.local/bin/cloudflared"
  if [ ! -x "$b" ]; then
    echo "A descarregar o cloudflared (binário oficial da Cloudflare)…" >&2
    mkdir -p "$(dirname "$b")"
    curl -fsSL -o "$b" https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    chmod +x "$b"
  fi
  echo "$b"
}

case "${1:-}" in
  rede)
    parar_tunel
    IP="$(ip_local)"
    gerar_env "http://$IP" "$IP,localhost" 1
    arrancar
    echo "Pronto. Nos telemóveis (mesma rede Wi-Fi): http://$IP"
    echo "Sem HTTPS, o botão «Copiar mensagem» do convite não funciona nos telemóveis; o resto funciona."
    ;;
  tunel)
    parar_tunel
    CF="$(cloudflared_bin)"
    : > "$LOG_TUNEL"
    nohup "$CF" tunnel --no-autoupdate --url http://localhost:80 > "$LOG_TUNEL" 2>&1 &
    echo $! > "$PID_TUNEL"
    echo -n "A abrir o túnel"
    for _ in $(seq 1 60); do
      URL="$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' "$LOG_TUNEL" | head -1 || true)"
      [ -n "$URL" ] && break; echo -n "."; sleep 1
    done
    echo
    [ -n "${URL:-}" ] || { echo "Não foi possível abrir o túnel. Ver $LOG_TUNEL"; parar_tunel; exit 1; }
    gerar_env "$URL" "${URL#https://},localhost" 0
    arrancar
    echo "Pronto. Endereço público (só enquanto o túnel estiver aberto): $URL"
    echo "Fechar no fim da sessão: infra/demo.sh parar"
    ;;
  repor)
    [ -f "$ENV" ] || { echo "Arranque primeiro com «rede» ou «tunel»."; exit 1; }
    RASTO_ENV="$ENV" docker compose --profile app stop web cron >/dev/null
    docker compose exec -T db dropdb -U rasto --if-exists rasto_demo
    docker compose exec -T db createdb -U rasto rasto_demo
    arrancar
    echo "Base de demonstração reposta."
    ;;
  estado)
    [ -f "$ENV" ] && grep '^SITE_URL=' "$ENV" || echo "Modo de demonstração não configurado."
    [ -f "$PID_TUNEL" ] && kill -0 "$(cat "$PID_TUNEL")" 2>/dev/null && echo "Túnel: aberto" || echo "Túnel: fechado"
    docker compose --profile app ps --format '{{.Service}}: {{.Status}}'
    ;;
  parar)
    parar_tunel
    RASTO_ENV="${ENV}" docker compose --profile app stop web cron frontend caddy >/dev/null 2>&1 || true
    echo "Túnel fechado e contentores parados."
    ;;
  *)
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac
