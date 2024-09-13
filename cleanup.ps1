# delete build folders
Write-Host "Deleting nginx build-container folder..."
Remove-Item -Path .\nginx\build-container -Recurse -Force

Write-Host "Deleting psql build-container folder..."
Remove-Item -Path .\psql\build-container -Recurse -Force