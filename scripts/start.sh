#!/usr/bin/env bash
# Builds the frontend and starts the platform on http://localhost:8080.
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/dev-env.sh
scripts/db.sh start
(cd frontend && { [ -d node_modules ] || npm install; } && npm run build)
cd backend && mvn -q -B spring-boot:run
