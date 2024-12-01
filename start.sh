#!/bin/bash

sudo apt-get update

sudo apt-get install pipx -y

pipx install poetry
pipx ensurepath
export PATH="/home/ubuntu/.local/bin:$PATH"

cd world-scraper

poetry shell
poetry install
poetry run python3 src/main.py