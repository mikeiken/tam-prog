# Load .env file and run docker-compose up

# Function to load .env file and set environment variables
function Load-DotEnv {
    param (
        [string]$envFilePath = ".env"
    )

    if (Test-Path $envFilePath) {
        Get-Content $envFilePath | ForEach-Object {
            if ($_ -match "^\s*([^#][^=]*)\s*=\s*(.*)\s*$") {
                $name = $matches[1]
                $value = $matches[2]
                [System.Environment]::SetEnvironmentVariable($name, $value)
            }
        }
    } else {
        Write-Error "The .env file does not exist at path: $envFilePath"
    }
}

# Load the .env file
Load-DotEnv

# Run docker-compose up
python ./django/tamprog/manage.py runserver