#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/env_loader.sh"

echo "Starte Pokedex-ID Matching..."

psql -v ON_ERROR_STOP=1 <<'EOF'
UPDATE card_catalog c
SET pokedex_id = (
    SELECT p.pokedex_id 
    FROM pokedex p
    WHERE LOWER(c.card_name) LIKE '%' || LOWER(p.pokemon_name) || '%'
    ORDER BY LENGTH(p.pokemon_name) DESC
    LIMIT 1
)
WHERE c.pokedex_id IS NULL;
EOF

echo "Matching done"