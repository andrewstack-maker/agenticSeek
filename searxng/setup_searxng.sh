#!/bin/bash

# Generate a secret key and update settings
SECRET_KEY=$(openssl rand -hex 32)
if [ -f "searxng/settings.yml" ]; then
    if [ "$(uname)" = "Darwin" ]; then
        sed -i '' "s/ultrasecretkey/$SECRET_KEY/g" searxng/settings.yml || {
            echo "Warning: Failed to update settings.yml with secret key. Please check the file manually."
        }
    else
        sed -i "s/ultrasecretkey/$SECRET_KEY/g" searxng/settings.yml || {
            echo "Warning: Failed to update settings.yml with secret key. Please check the file manually."
        }
    fi
else
    echo "Error: settings.yml not found. Initial setup may have failed."
    docker-compose logs searxng
    exit 1
fi