#!/bin/sh
# delete build folders
@echo "Deleting nginx build-container folder..."
rm -rf ./nginx/build-container

@echo "Deleting psql build-container folder..."
rm -rf ./psql/build-container