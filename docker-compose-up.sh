#!/bin/sh
./env-inject.sh
docker-compose --env-file ./.env up -d