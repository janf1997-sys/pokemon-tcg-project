#!/bin/bash

set -e

#!/bin/bash

# Ermittelt den absoluten Pfad des Ordners, in dem env_loader.sh liegt (also /scripts)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Geht von /scripts aus genau eine Ebene höher ins Hauptverzeichnis zur .env
ENV_FILE="$SCRIPT_DIR/../.env"

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "❌ Fehler: .env-Datei wurde unter folgendem Pfad nicht gefunden:"
    echo "   $ENV_FILE"
    return 1 2>/dev/null || exit 1
fi

export PGHOST=${DB_HOST:-$PGHOST}
export PGDATABASE=${DB_NAME:-$PGDATABASE}
export PGUSER=${DB_USER:-$PGUSER}
export PGPASSWORD=${DB_PASSWORD:-$PGPASSWORD}
export PGPORT=${DB_PORT:-$PGPORT}
