#!/usr/bin/env bash
# Runs the automated content publication gates (docs/curriculum/03-content-standards.md §6).
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/dev-env.sh
mvn -q -B -f backend/pom.xml test -Dtest=ContentValidationTest -Dsurefire.failIfNoSpecifiedTests=false
