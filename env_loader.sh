#!/bin/bash

set -e

if [ -f .env ]; then    
    export $(cat .env | xargs)
else   
    echo "Error .env file not found"
    exit 1
fi

export PGHOST=${DB_HOST:-$PGHOST}
export PGDATABASE=${DB_NAME:-$PGDATABASE}
export PGUSER=${DB_USER:-$PGUSER}
export PGPASSWORD=${DB_PASSWORD:-$PGPASSWORD}
export PGPORT=${DB_PORT:-$PGPORT}
