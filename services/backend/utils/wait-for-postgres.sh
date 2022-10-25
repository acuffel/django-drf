#!/bin/sh
set -e
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Postgres is unavailable - sleeping"
    sleep 1
done
echo "Postgres is up - continue"
exec "$@"
