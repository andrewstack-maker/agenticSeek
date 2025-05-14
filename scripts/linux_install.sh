#!/bin/bash

echo "Starting installation for Linux..."

set -e

if ! command -v python3.10 &> /dev/null; then
    echo "Error: Python 3.10 is not installed. Please install Python 3.10 and try again."
    echo "You can install it using: sudo apt-get install python3.10 python3.10-dev python3.10-venv"
    exit 1
fi

# Check if pip3.10 is available
if ! python3.10 -m pip --version &> /dev/null; then
    echo "Error: pip for Python 3.10 is not installed. Installing python3.10-pip..."
    sudo apt-get install -y python3.10-pip || { echo "Failed to install python3.10-pip"; exit 1; }
fi

# Update package list
sudo apt-get update || { echo "Failed to update package list"; exit 1; }
# make sure essential tool are installed
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

# Upgrade pip for Python 3.10
python3.10 -m pip install --upgrade pip || { echo "Failed to upgrade pip"; exit 1; }
# Install and upgrade setuptools and wheel
python3.10 -m pip install --upgrade setuptools wheel || { echo "Failed to install setuptools and wheel"; exit 1; }
# Install Selenium for chromedriver
python3.10 -m pip install selenium || { echo "Failed to install selenium"; exit 1; }
# Install Python dependencies from requirements.txt
python3.10 -m pip install -r requirements.txt --no-cache-dir || { echo "Failed to install requirements.txt"; exit 1; }
# install docker compose
sudo apt install -y docker-compose

echo "Installation complete for Linux!"