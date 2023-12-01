#!/bin/bash

# Read .env file and export variables
export $(cat .env | grep -v '^#' | xargs)

# Replace variables in nginx.conf
envsubst '$GUNICORN_SERVICE_NAME $GUNICORN_SERVICE_PORT $NGINX_CONTAINER_PORT' < nginx.conf.template > nginx.conf
