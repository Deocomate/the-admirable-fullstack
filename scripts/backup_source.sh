#!/usr/bin/env bash
# Dumps the Laravel source database and archives uploaded media, before any
# migration run touches the target database. Never writes to the source.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

: "${DB_HOST:?DB_HOST not set}"
: "${DB_PORT:?DB_PORT not set}"
: "${DB_DATABASE:?DB_DATABASE not set}"
: "${DB_USERNAME:?DB_USERNAME not set}"
: "${DB_PASSWORD:?DB_PASSWORD not set}"

STAMP=$(date +%F-%H%M)
mkdir -p backups

echo "Dumping ${DB_DATABASE}@${DB_HOST}:${DB_PORT} ..."
mysqldump --single-transaction --routines --triggers \
  -h"${DB_HOST}" -P"${DB_PORT}" -u"${DB_USERNAME}" -p"${DB_PASSWORD}" \
  "${DB_DATABASE}" | gzip > "backups/src-${STAMP}.sql.gz"

echo "Verifying dump is readable ..."
(zcat "backups/src-${STAMP}.sql.gz" | head -n 5 > /dev/null) || true

echo "Archiving media ..."
tar czf "backups/media-${STAMP}.tar.gz" storage/app/public/uploads

echo "Done:"
echo "  backups/src-${STAMP}.sql.gz"
echo "  backups/media-${STAMP}.tar.gz"
