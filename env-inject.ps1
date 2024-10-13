# Load .env file and run a specified command

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

# Check if a command is provided as arguments
if ($args.Count -eq 0) {
    Write-Error "No command provided. Please provide a command to run."
    exit 1
}

# Join all arguments into a single command string
$command = $args -join " "
Invoke-Expression $command