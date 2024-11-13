$originalLocation = Get-Location

try {
    ./env-inject.ps1
    
    Set-Location -Path "django"
    
    ./entrypoint.ps1
}
finally {
    Set-Location -Path $originalLocation
    Write-Host "Restored location to: $originalLocation"
}