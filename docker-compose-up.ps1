./env-inject.ps1
docker-compose --env-file ./.env up -d $args
# ./env-inject.ps1 docker-compose up -d