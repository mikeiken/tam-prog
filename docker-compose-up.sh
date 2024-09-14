#!/bin/sh

# Load .env file and export environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found"
  exit 1
fi

# Run docker-compose up
docker-compose up