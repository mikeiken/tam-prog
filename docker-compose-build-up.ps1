# $command = $args -join " "
./env-inject.ps1
docker-compose --env-file ./.env -f docker-compose-build.yml up -d $args