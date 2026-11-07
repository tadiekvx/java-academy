#!/usr/bin/env bash
# A project-local PostgreSQL 18 for development and tests (no system service).
#   scripts/db.sh start   initialise on first use, then start (port 5433)
#   scripts/db.sh stop
#   scripts/db.sh status
# Data lives in .data/postgres (git-ignored). Local connections are trusted; never expose this port.
set -euo pipefail
cd "$(dirname "$0")/.."
PG_BIN=/opt/homebrew/opt/postgresql@18/bin
DATA="$PWD/.data/postgres"
PORT=5433

case "${1:-}" in
  start)
    if [ ! -f "$DATA/PG_VERSION" ]; then
      mkdir -p "$DATA"
      "$PG_BIN/initdb" -D "$DATA" -U academy --auth=trust --encoding=UTF8 --locale=en_US.UTF-8 > /dev/null
    fi
    if ! "$PG_BIN/pg_ctl" -D "$DATA" status > /dev/null 2>&1; then
      "$PG_BIN/pg_ctl" -D "$DATA" -l "$DATA/server.log" -w \
        -o "-p $PORT -c listen_addresses=localhost -c unix_socket_directories='$DATA'" start > /dev/null
    fi
    for db in academy academy_test; do
      "$PG_BIN/psql" -h localhost -p $PORT -U academy -d postgres -tAc "select 1 from pg_database where datname = '$db'" | grep -q 1 \
        || "$PG_BIN/createdb" -h localhost -p $PORT -U academy "$db"
    done
    echo "PostgreSQL running on localhost:$PORT (databases: academy, academy_test)"
    ;;
  stop)
    "$PG_BIN/pg_ctl" -D "$DATA" -w stop
    ;;
  status)
    "$PG_BIN/pg_ctl" -D "$DATA" status
    ;;
  *)
    echo "usage: $0 start|stop|status" >&2
    exit 1
    ;;
esac
