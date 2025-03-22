#!/bin/bash

echo "Starting installation for Linux..."

# Update package list
sudo apt-get update

pip install --upgrade pip

# install pyaudio
pip install pyaudio
# install port audio
sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio
# install wheel
pip install --upgrade pip setuptools wheel

# Install Python dependencies from requirements.txt
pip3 install -r requirements.txt

# Install Selenium for chromedriver
pip3 install selenium

# Install portaudio for pyAudio
sudo apt-get install -y portaudio19-dev python3-dev alsa-utils

echo "Installation complete for Linux!"