FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Add build arguments for logging
ARG BUILDKIT_PROGRESS=plain

# Enable verbose logging
ENV PYTHONUNBUFFERED=1
ENV PIP_PROGRESS_BAR=on

# Install system dependencies with logging
RUN echo "🔧 Installing system dependencies..." && \
    apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    htop \
    && echo "✅ System dependencies installed" \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN echo "📋 Requirements file copied"

# Install Python dependencies with verbose logging
RUN echo "🐍 Starting Python dependencies installation..." && \
    echo "📦 Installing RunPod SDK..." && \
    pip install --no-cache-dir --verbose runpod && \
    echo "🔥 Installing PyTorch..." && \
    pip install --no-cache-dir --verbose torch==2.1.0 && \
    echo "🤗 Installing Transformers and Diffusers..." && \
    pip install --no-cache-dir --verbose transformers diffusers && \
    echo "⚡ Installing additional dependencies..." && \
    pip install --no-cache-dir --verbose accelerate safetensors Pillow torchvision && \
    echo "✅ All Python dependencies installed successfully!"

# Copy handler file
COPY handler.py .
RUN echo "📄 Handler file copied"

# Create cache directories with logging
RUN echo "📁 Creating cache directories..." && \
    mkdir -p /tmp/torch_cache /tmp/hf_cache && \
    echo "✅ Cache directories created"

# Set environment variables for caching and logging
ENV TORCH_HOME=/tmp/torch_cache
ENV HF_HOME=/tmp/hf_cache
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0

# Add health check
RUN echo "🔍 Verifying installation..." && \
    python3 -c "import torch; print(f'PyTorch version: {torch.__version__}')" && \
    python3 -c "import diffusers; print(f'Diffusers version: {diffusers.__version__}')" && \
    python3 -c "import runpod; print('RunPod SDK imported successfully')" && \
    echo "✅ All imports verified successfully!"

RUN echo "🚀 Build completed! Ready for deployment."

# Start the container
CMD ["python3", "-u", "handler.py"]