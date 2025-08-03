FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler file
COPY handler.py .

# Create cache directories
RUN mkdir -p /tmp/torch_cache /tmp/hf_cache

# Set environment variables for caching
ENV TORCH_HOME=/tmp/torch_cache
ENV HF_HOME=/tmp/hf_cache

# Start the container
CMD ["python3", "-u", "handler.py"]