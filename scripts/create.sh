#!/bin/bash
set -e

# 1. Lädt env_loader.sh zuverlässig aus demselben Ordner (scripts/)
source "$(dirname "$0")/env_loader.sh"

echo "Creating Tables"

# 2. Greift auf sheme.sql im Hauptverzeichnis (eine Ebene höher) zu
#    Zusätzlich: Vereinfachter psql-Aufruf, da env_loader.sh bereits PGHOST/PGUSER/PGDATABASE exportiert!
psql -f "$(dirname "$0")/../sheme.sql"

echo "Done"