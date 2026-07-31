#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/env_loader.sh"

CSV_PATH="$SCRIPT_DIR/../CSV/pokedex.csv"

psql -c "\copy pokedex(pokedex_id, generation, pokemon_name) FROM '$CSV_PATH' WITH (FORMAT csv, HEADER true, DELIMITER ',');"