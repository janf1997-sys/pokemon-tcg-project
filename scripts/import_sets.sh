#!/bin/bash

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/env_loader.sh"

CSV_PATH="$SCRIPT_DIR/../CSV/sets.csv"

echo "Importing TCG sets"

psql -v ON_ERROR_STOP=1 <<EOF
CREATE TEMP TABLE temp_tcg_sets (
set_id VARCHAR(20),
set_name VARCHAR(100),
base_set INT,
master_set INT
);

\copy temp_tcg_sets FROM '$CSV_PATH' WITH (FORMAT csv, HEADER true, DELIMITER ',');

INSERT INTO tcg_sets (set_id, set_name, base_set, master_set)
SELECT set_id, set_name, base_set, master_set FROM temp_tcg_sets
ON CONFLICT (set_id) DO NOTHING;

DROP TABLE temp_tcg_sets;

EOF

echo "Import done"