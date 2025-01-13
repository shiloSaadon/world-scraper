#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

sudo -E apt-get update
sudo -E apt-get install -y \
    python3-poetry \
    nodejs \
    npm \
    -o Dpkg::Options::="--force-confnew"

export PATH="/home/ubuntu/.local/bin:$PATH"

node -v
npm -v
npx -v

sudo npx --yes playwright install-deps

cd /tmp/world-scraper

sudo chmod +x ./src/go-scraper/google_maps_scraper_linux

sudo poetry install
sudo poetry run python3 src/main.py