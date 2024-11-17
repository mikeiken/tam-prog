#!/bin/bash

# Function to load .env file and set environment variables
load_dotenv() {
    local env_file="${1:-.env}"

    if [ -f "$env_file" ]; then
        while IFS= read -r line || [ -n "$line" ]; do
            # Skip comments and empty lines
            if [[ $line =~ ^[[:space:]]*#.*$ ]] || [[ -z $line ]]; then
                continue
            fi

            # Extract variable name and value
            if [[ $line =~ ^[[:space:]]*([^#][^=]*)[[:space:]]*=[[:space:]]*(.*)[[:space:]]*$ ]]; then
                local name="${BASH_REMATCH[1]}"
                local value="${BASH_REMATCH[2]}"
                export "$name=$value"
            fi
        done < "$env_file"
    else
        echo "[ENV-INJECT] The .env file does not exist at path: $env_file" >&2
        exit 1
    fi
}

# Load the .env file
load_dotenv

# Check if a command is provided as arguments
if [ $# -eq 0 ]; then
    echo "[ENV-INJECT] No command provided. Ran as standalone script."
else
    # Execute the command with all arguments
    eval "$@"
fi