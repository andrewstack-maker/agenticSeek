#!/bin/bash

echo "Starting installation for macOS..."

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

# Check if homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# update
brew update
# make sure wget installed
brew install wget
# Install chromedriver using Homebrew
brew install --cask chromedriver
# Install portaudio for pyAudio using Homebrew
brew install portaudio

# Upgrade pip for Python 3.10
python3.10 -m pip install --upgrade pip || { echo "Failed to upgrade pip"; exit 1; }
# Install and upgrade setuptools and wheel
python3.10 -m pip install --upgrade setuptools wheel || { echo "Failed to install setuptools and wheel"; exit 1; }
# Install Selenium for chromedriver
python3.10 -m pip install selenium || { echo "Failed to install selenium"; exit 1; }
# Install Python dependencies from requirements.txt
python3.10 -m pip install -r requirements.txt --no-cache-dir || { echo "Failed to install requirements.txt"; exit 1; }

echo "Installation complete for macOS!"