# Use a Python base image
FROM python:3.10-slim

# Install system dependencies for graphics and audio
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libasound2 \
    alsa-utils \
    x11-utils \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Default command to run the Pygame application
CMD ["python", "run.py"]

