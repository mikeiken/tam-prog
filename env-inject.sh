#!/bin/sh

# Load .env file and run a specified command

# Function to load .env file and set environment variables
load_dotenv() {
    env_file_path=".env"
    if [ -f "$env_file_path" ]; then
        while IFS='=' read -r name value; do
            if [ -n "$name" ] && [ "${name:0:1}" != "#" ]; then
                export "$name"="$value"
            fi
        done < "$env_file_path"
    else
        echo "The .env file does not exist at path: $env_file_path" >&2
        exit 1
    fi
}

# Load the .env file
load_dotenv

# Check if a command is provided as arguments
if [ "$#" -eq 0 ]; then
    echo "No command provided. Please provide a command to run." >&2
    exit 1
fi

# Join all arguments into a single command string
command="$*"
eval "$command"