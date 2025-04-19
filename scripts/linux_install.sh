#!/bin/bash

echo "Starting installation for Linux..."

set -e
# Update package list
sudo apt-get update || { echo "Failed to update package list"; exit 1; }
# make sure essential tool are installed
# Install essential tools
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    python3-wheel \
    build-essential \
    alsa-utils \
    portaudio19-dev \
    python3-pyaudio \
    libgtk-3-dev \
    libnotify-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 || { echo "Failed to install packages"; exit 1; }

# upgrade pip
pip install --upgrade pip
# install wheel
pip install --upgrade pip setuptools wheel
# install docker compose
sudo apt install -y docker-compose
# Install Selenium for chromedriver
pip3 install selenium
# Install Python dependencies from requirements.txt
pip3 install -r requirements.txt --no-cache-dir

echo "Installation complete for Linux!"