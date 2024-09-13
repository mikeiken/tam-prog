#!/bin/sh

# Usually this is the version (latest, ...)
tag="latest"

# Name of the image
# in format "<dockerhub-account-name>/<image-name>"
# or "ghcr.io/<github-account-name>/<image-name>" 
# (if you want to push to GitHub Container Registry
# instead of Docker Hub)
name="tamprog/nginx"

# Build as tagged image
echo "Starting build for $name ..."
if docker build -t ${name} -t ${name}:${tag} . -o ./build-container; then
  echo "Script finished for $name."
else
  echo "Build error." >&2
fi