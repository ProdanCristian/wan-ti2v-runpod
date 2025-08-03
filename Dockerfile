# Use NVIDIA CUDA base image with Python 3.10
FROM nvidia/cuda:12.1-devel-ubuntu22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    git \
    wget \
    curl \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links for python
RUN ln -s /usr/bin/python3.10 /usr/bin/python && \
    ln -s /usr/bin/python3.10 /usr/bin/python3

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Create directories for model cache and temporary files
RUN mkdir -p /app/cache /app/tmp

# Set environment variables for model caching
ENV HF_HOME=/app/cache
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_DATASETS_CACHE=/app/cache

# Expose port (if needed)
EXPOSE 8080

# Set the entry point
CMD ["python", "handler.py"]