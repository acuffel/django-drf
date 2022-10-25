#!/bin/sh
set -e
while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
    echo "RabbitMQ is unavailable - sleeping"
    sleep 1
done
echo "RabbitMQ is up - continue"
exec "$@"
