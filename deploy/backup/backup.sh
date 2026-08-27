#!/usr/bin/env bash
# ==============================================================================
# The Admirable - Automated Backup Script
# Performs MySQL database dumps (daily, keep 14) and media archives (weekly, keep 4)
# ==============================================================================

set -euo pipefail

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DAY_OF_WEEK=$(date +"%u") # 1 (Monday) .. 7 (Sunday)

BACKUP_DIR="${BACKUP_DIR:-/backups}"
MEDIA_DIR="${MEDIA_DIR:-/media}"

DB_HOST="${DB_HOST:-mysql}"
DB_NAME="${DB_NAME:-admirable}"
DB_USER="${DB_USER:-admirable}"
DB_PASSWORD="${DB_PASSWORD:-secret}"

RETENTION_DB_DAYS="${RETENTION_DB_DAYS:-14}"
RETENTION_MEDIA_WEEKS="${RETENTION_MEDIA_WEEKS:-4}"

mkdir -p "${BACKUP_DIR}"

log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $*"
}

log "=== Starting Backup Process [${TIMESTAMP}] ==="

# 1. Database Backup (mysqldump + gzip)
DB_BACKUP_FILE="${BACKUP_DIR}/db_${DB_NAME}_${TIMESTAMP}.sql.gz"
log "Dumping MySQL database '${DB_NAME}' from host '${DB_HOST}'..."

export MYSQL_PWD="${DB_PASSWORD}"
mysqldump \
    -h "${DB_HOST}" \
    -u "${DB_USER}" \
    --single-transaction \
    --quick \
    --routines \
    --triggers \
    --default-character-set=utf8mb4 \
    "${DB_NAME}" | gzip -9 > "${DB_BACKUP_FILE}"

DB_SIZE=$(du -h "${DB_BACKUP_FILE}" | cut -f1)
log "Database backup created: ${DB_BACKUP_FILE} (${DB_SIZE})"

# 2. Media Backup (tar + gzip) - run on Sundays (DAY_OF_WEEK=7) or if forced
FORCE_MEDIA="${1:-}"
if [ "${DAY_OF_WEEK}" = "7" ] || [ "${FORCE_MEDIA}" = "--with-media" ]; then
    if [ -d "${MEDIA_DIR}" ] && [ "$(ls -A "${MEDIA_DIR}" 2>/dev/null)" ]; then
        MEDIA_BACKUP_FILE="${BACKUP_DIR}/media_${TIMESTAMP}.tar.gz"
        log "Archiving media directory '${MEDIA_DIR}'..."
        tar -czf "${MEDIA_BACKUP_FILE}" -C "${MEDIA_DIR}" .
        MEDIA_SIZE=$(du -h "${MEDIA_BACKUP_FILE}" | cut -f1)
        log "Media archive created: ${MEDIA_BACKUP_FILE} (${MEDIA_SIZE})"
    else
        log "Media directory is empty or not found. Skipping media archive."
    fi
fi

# 3. Retention & Cleanup
log "Pruning database backups older than ${RETENTION_DB_DAYS} days..."
find "${BACKUP_DIR}" -name "db_${DB_NAME}_*.sql.gz" -type f -mtime +"${RETENTION_DB_DAYS}" -exec rm -f {} +

log "Pruning media archives older than $((RETENTION_MEDIA_WEEKS * 7)) days..."
find "${BACKUP_DIR}" -name "media_*.tar.gz" -type f -mtime +"$((RETENTION_MEDIA_WEEKS * 7))" -exec rm -f {} +

log "=== Backup Process Completed Successfully ==="
