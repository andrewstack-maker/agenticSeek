#!/bin/bash

echo "Starting installation for Linux..."

# Update package list
sudo apt-get update

pip install --upgrade pip

# install pyaudio
pip install pyaudio
# make sure essential tool are installed
sudo apt install python3-dev python3-pip python3-wheel build-essential
# install port audio
sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio
# install wheel
pip install --upgrade pip setuptools wheel
# install docker compose
sudo apt install docker-compose

# Install Python dependencies from requirements.txt
pip3 install -r requirements.txt

# Install Selenium for chromedriver
pip3 install selenium

# Install portaudio for pyAudio
sudo apt-get install -y portaudio19-dev python3-dev alsa-utils

echo "Installation complete for Linux!"