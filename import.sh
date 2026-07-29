#!/bin/bash

set -e

source ./env_loader.sh

psql -c "\copy pokedex(pokedex_id, generation, pokemon_name) FROM './pokedex.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');"