# Usually this is the version (latest, ...)
$tag = "latest"

# Name of the image
# in format "<dockerhub-account-name>/<imange-name>"
# or "ghcr.io/<github-account-name>/<imange-name>" 
# (if you want to push to GitHub Container Registry
# instead of Docker Hub)
$name = "tamprog/nginx"

# Build as tagged image
(Write-Host "Starting build for $name ..." -ForegroundColor Cyan) `
&& (docker build -t ${name} -t ${name}:${tag} . -o ./build-container `
|| Write-Error 'Build error.') `
&& (Write-Host "Script finished for $name." -ForegroundColor Cyan)