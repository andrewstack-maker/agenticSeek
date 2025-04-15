#!/bin/bash

# entrypoint for docker searxng service

SECRET_KEY=$(openssl rand -hex 32)

sed -i "s/ultrasecretkey/$SECRET_KEY/g" /etc/searxng/settings.yml

exec /usr/local/searxng/dockerfiles/docker-entrypoint.sh "$@"