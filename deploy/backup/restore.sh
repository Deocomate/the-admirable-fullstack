#!/usr/bin/env bash
# ==============================================================================
# The Admirable - Disaster Recovery & Database Restore Script
# Restores MySQL database dumps and media archives from backup files
# ==============================================================================

set -euo pipefail

log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $*"
}

usage() {
    echo "Usage:"
    echo "  $0 --db <path-to-db-backup.sql.gz> [--target-db <db_name>]"
    echo "  $0 --media <path-to-media-backup.tar.gz> [--target-media-dir <dir>]"
    echo "  $0 --all --db <path-to-db-backup.sql.gz> --media <path-to-media-backup.tar.gz>"
    exit 1
}

DB_HOST="${DB_HOST:-mysql}"
DB_USER="${DB_USER:-admirable}"
DB_PASSWORD="${DB_PASSWORD:-secret}"
TARGET_DB="${DB_NAME:-admirable}"
TARGET_MEDIA_DIR="${MEDIA_DIR:-/media}"

DB_FILE=""
MEDIA_FILE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --db)
            DB_FILE="$2"
            shift 2
            ;;
        --target-db)
            TARGET_DB="$2"
            shift 2
            ;;
        --media)
            MEDIA_FILE="$2"
            shift 2
            ;;
        --target-media-dir)
            TARGET_MEDIA_DIR="$2"
            shift 2
            ;;
        --all)
            shift
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "${DB_FILE}" ] && [ -z "${MEDIA_FILE}" ]; then
    usage
fi

export MYSQL_PWD="${DB_PASSWORD}"

if [ -n "${DB_FILE}" ]; then
    if [ ! -f "${DB_FILE}" ]; then
        log "ERROR: Database backup file not found: ${DB_FILE}"
        exit 1
    fi
    log "Restoring database '${TARGET_DB}' from '${DB_FILE}'..."
    # If restoring from .gz or plain .sql
    if [[ "${DB_FILE}" == *.gz ]]; then
        gunzip -c "${DB_FILE}" | mysql -h "${DB_HOST}" -u "${DB_USER}" "${TARGET_DB}"
    else
        mysql -h "${DB_HOST}" -u "${DB_USER}" "${TARGET_DB}" < "${DB_FILE}"
    fi
    log "Database '${TARGET_DB}' restore completed successfully."
fi

if [ -n "${MEDIA_FILE}" ]; then
    if [ ! -f "${MEDIA_FILE}" ]; then
        log "ERROR: Media backup file not found: ${MEDIA_FILE}"
        exit 1
    fi
    mkdir -p "${TARGET_MEDIA_DIR}"
    log "Restoring media archive to '${TARGET_MEDIA_DIR}' from '${MEDIA_FILE}'..."
    tar -xzf "${MEDIA_FILE}" -C "${TARGET_MEDIA_DIR}"
    log "Media restore completed successfully."
fi

log "=== All Restore Operations Completed ==="
