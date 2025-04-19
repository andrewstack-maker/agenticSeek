#!/bin/bash

echo "Starting installation for macOS..."

set -e

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
# update pip
python3 -m pip install --upgrade pip
# upgrade setuptools and wheel
pip3 install --upgrade setuptools wheel
# Install Selenium
pip3 install selenium
# Install Python dependencies from requirements.txt
pip3 install -r requirements.txt --no-cache-dir

echo "Installation complete for macOS!"