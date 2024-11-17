#!/bin/sh
./env-inject.sh
docker-compose --env-file ./.env -f docker-compose-build.yml up -d