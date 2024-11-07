#!/bin/sh
docker-compose --env-file .env -f docker-compose-build.yml up -d
# ./env-inject.sh docker-compose -f docker-compose-build.yml up -d