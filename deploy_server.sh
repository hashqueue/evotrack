#!/bin/bash

echo "Checking the MySQL config."
echo "MYSQL_HOST: $DB_HOST - MYSQL_PORT: $DB_PORT"
while ! nc -z $DB_HOST $DB_PORT ; do
    echo "Waiting for the MySQL service to be deployed."
    sleep 3
done
echo "MySQL service has been deployed."

ENV_PATH=.env.prod python3 -u create_database.py \
    && ENV_PATH=.env.prod python3 manage.py collectstatic --noinput \
    && echo "Static file collection is completed." \
    && ENV_PATH=.env.prod python3 manage.py makemigrations \
    && ENV_PATH=.env.prod python3 manage.py migrate \
    && echo "MySQL data migration is completed." \
    && ENV_PATH=.env.prod gunicorn -c gunicorn.conf.py
