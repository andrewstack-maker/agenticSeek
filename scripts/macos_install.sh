#!/bin/bash

echo "Starting installation for macOS..."

# Install Python dependencies from requirements.txt
pip3 install -r requirements.txt

# Install chromedriver using Homebrew
brew install --cask chromedriver

# Install portaudio for pyAudio using Homebrew
brew install portaudio

# Install Selenium
pip3 install selenium

echo "Installation complete for macOS!"