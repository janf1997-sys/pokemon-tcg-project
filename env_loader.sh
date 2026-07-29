#!/bin/bash

set -e

if [ -f .env ]; then    
    export $(cat .env | xargs)
else   
    echo "Error .env file not found"
    exit 1
fi

export PGPASSWORD=${DB_PASSWORD:-$PGPASSWORD}
