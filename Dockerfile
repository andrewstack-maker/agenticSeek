# Use official Python 3.11 image as the base
FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    libportaudio2 \
    portaudio19-dev \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip cache purge

COPY . .

RUN BLIS_ARCH=generic pip install --no-cache-dir -r requirements.txt