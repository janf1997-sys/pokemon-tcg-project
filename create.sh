#!/bin/bash
set -e

if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

export PGPASSWORD=$DB_PASSWORD

echo "Creating Tables"

psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f sheme.sql

echo "Done"