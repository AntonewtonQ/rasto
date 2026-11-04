#!/usr/bin/env bash
# Cópia de segurança cifrada da base de dados e dos comprovativos (base técnica 7.7).
# Uso: infra/copias/copiar.sh [pasta-destino]   (por omissão: infra/copias/arquivo/)
# A chave fica em infra/copias/.chave (fora do Git, permissões 600). Sem a chave, as cópias não se abrem.
# Retenção: 30 dias (coerente com a eliminação de dados pessoais, base técnica 7.6).
set -euo pipefail
cd "$(dirname "$0")/../.."
DESTINO="${1:-infra/copias/arquivo}"
CHAVE="infra/copias/.chave"
MEDIA="${MEDIA:-backend/media}"
mkdir -p "$DESTINO"
if [ ! -f "$CHAVE" ]; then
  umask 077 && head -c 48 /dev/urandom | base64 > "$CHAVE"
  echo "Chave nova criada em $CHAVE. Guarde uma cópia fora do servidor."
fi
DATA="$(date -u +%Y%m%dT%H%M%SZ)"
TMP="$(mktemp -d)"; trap 'rm -r -- "$TMP"' EXIT

docker compose exec -T db pg_dump -U rasto -d rasto -Fc > "$TMP/base.dump"
if [ -d "$MEDIA" ]; then tar -C "$MEDIA" -czf "$TMP/media.tgz" .; else tar -czf "$TMP/media.tgz" -T /dev/null; fi
tar -C "$TMP" -cf "$TMP/rasto.tar" base.dump media.tgz
gpg --batch --yes --quiet --pinentry-mode loopback --passphrase-file "$CHAVE" \
    --symmetric --cipher-algo AES256 -o "$DESTINO/rasto-$DATA.tar.gpg" "$TMP/rasto.tar"
sha256sum "$DESTINO/rasto-$DATA.tar.gpg" > "$DESTINO/rasto-$DATA.tar.gpg.sha256"
find "$DESTINO" -name 'rasto-*.tar.gpg*' -mtime +30 -delete
echo "Cópia: $DESTINO/rasto-$DATA.tar.gpg ($(du -h "$DESTINO/rasto-$DATA.tar.gpg" | cut -f1))"
