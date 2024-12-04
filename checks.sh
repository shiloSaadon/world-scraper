#!/bin/bash

# Function to throw an exception (exit with an error message)
throw_exception() {
    echo "Error: $1" >&2
    exit 1
}

# Check if an argument is provided
if [[ $# -eq 0 ]]; then
    throw_exception "No hexagon count provided. Usage: $0 <number>"
fi

# Validate that the argument is a positive integer
if ! [[ "$1" =~ ^[1-9][0-9]*$ ]]; then
    throw_exception "Invalid hexagon count. Please provide a positive integer."
fi

# Check if .env file exists
if [[ ! -f ".env" ]]; then
    throw_exception ".env file does not exist"
fi

# Array of required variables
required_vars=(
    "SUPABASE_PROJECT_URL"
    "SUPABASE_PROJECT_KEY"
    "HOST_SERVER_URL"
    "HOST_SERVER_AUTH_KEY"
)

# Check each required variable
for var in "${required_vars[@]}"; do
    if ! grep -q "^${var}=" .env; then
        throw_exception "Missing required variable: ${var}"
    fi
done

# Update or add HEXAGON_COUNT with the provided argument
if grep -q "^HEXAGON_COUNT=" .env; then
    sed -i "s/^HEXAGON_COUNT=.*$/HEXAGON_COUNT=$1/" .env
else
    echo "HEXAGON_COUNT=$1" >> .env
fi

echo "Environment checks passed. HEXAGON_COUNT set to $1."