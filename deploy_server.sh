#!/bin/bash

echo "Checking the MySQL service."
while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL service to be deployed."
    sleep 3
done
echo "MySQL service has been deployed."

ENV_PATH=.env.prod python3 manage.py collectstatic --noinput \
    && echo "Static file collection is completed." \
    && ENV_PATH=.env.prod python3 manage.py makemigrations \
    && ENV_PATH=.env.prod python3 manage.py migrate \
    && echo "MySQL data migration is completed." \
    && ENV_PATH=.env.prod gunicorn -c gunicorn.conf.py
