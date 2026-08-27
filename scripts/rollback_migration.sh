#!/usr/bin/env bash
# The source database is never written to, so "rollback" only ever means
# dropping and recreating the target database. Re-run alembic + migrate_data
# afterwards to try again.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

: "${DB__HOST:?DB__HOST not set}"
: "${DB__PORT:?DB__PORT not set}"
: "${DB__USER:?DB__USER not set}"
: "${DB__PASSWORD:?DB__PASSWORD not set}"
: "${DB__DATABASE:?DB__DATABASE not set}"

echo "Dropping and recreating target database ${DB__DATABASE} ..."
mysql -h"${DB__HOST}" -P"${DB__PORT}" -u"${DB__USER}" -p"${DB__PASSWORD}" -e \
  "DROP DATABASE IF EXISTS ${DB__DATABASE}; CREATE DATABASE ${DB__DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "Done. Now run:"
echo "  uv run alembic upgrade head"
echo "  uv run python scripts/migrate_data.py --source-url <source-url> --with-media"
