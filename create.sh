#!/bin/bash
set -e

source ./env_loader.sh

echo "Creating Tables"

psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f sheme.sql

echo "Done"