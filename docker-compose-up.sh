#!/bin/sh
docker-compose --env-file .env up -d
# ./env-inject.sh docker-compose up -d