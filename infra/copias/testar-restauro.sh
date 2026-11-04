#!/usr/bin/env bash
# Testa o restauro da cópia mais recente numa base temporária, sem tocar na base em uso (RNF11).
# Confirma: a cópia abre com a chave, a base restaura, e a cadeia de hash da auditoria continua válida.
set -euo pipefail
cd "$(dirname "$0")/../.."
DESTINO="${1:-infra/copias/arquivo}"
CHAVE="infra/copias/.chave"
ULTIMA="$(ls -t "$DESTINO"/rasto-*.tar.gpg | head -1)"
sha256sum -c "$ULTIMA.sha256" >/dev/null
TMP="$(mktemp -d)"; trap 'rm -r -- "$TMP"; docker compose exec -T db dropdb -U rasto --if-exists rasto_restauro' EXIT
gpg --batch --quiet --pinentry-mode loopback --passphrase-file "$CHAVE" -d "$ULTIMA" > "$TMP/rasto.tar"
tar -C "$TMP" -xf "$TMP/rasto.tar"
tar -tzf "$TMP/media.tgz" >/dev/null
docker compose exec -T db dropdb -U rasto --if-exists rasto_restauro
docker compose exec -T db createdb -U rasto rasto_restauro
docker compose exec -T db pg_restore -U rasto -d rasto_restauro --no-owner < "$TMP/base.dump"
CONTAGENS="$(docker compose exec -T db psql -U rasto -d rasto_restauro -At -c \
  "select (select count(*) from contas_utilizador) || ' utilizadores, ' || (select count(*) from organizacoes_organizacao) || ' entidades, ' || (select count(*) from auditoria_registoauditoria) || ' registos de auditoria'")"
( cd backend && PGDATABASE=rasto_restauro .venv/bin/python manage.py verificar_auditoria )
echo "Restauro de $(basename "$ULTIMA") verificado: $CONTAGENS."
