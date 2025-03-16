#!/bin/bash

echo "Starting installation for Linux..."

# Update package list
sudo apt-get update

# Install Python dependencies from requirements.txt
pip3 install -r requirements.txt

# Install Selenium for chromedriver
pip3 install selenium

# Install portaudio for pyAudio
sudo apt-get install -y portaudio19-dev python3-dev alsa-utils

echo "Installation complete for Linux!"