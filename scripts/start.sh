#!/bin/bash

set -e

echo "Starting PostgreSQL service"
sudo service postgresql start

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/env_loader.sh"

psql 