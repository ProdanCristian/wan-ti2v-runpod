# Docker Deployment Guide for RunPod

## Option 1: Build and Push Docker Image

### 1. Build the Docker Image Locally

```bash
# Build the image
docker build -t wan-ti2v-runpod:latest .

# Tag for your registry (replace with your Docker Hub username)
docker tag wan-ti2v-runpod:latest prodancristian/wan-ti2v-runpod:latest
```

### 2. Push to Docker Registry

```bash
# Login to Docker Hub
docker login

# Push the image
docker push prodancristian/wan-ti2v-runpod:latest
```

### 3. Deploy on RunPod

1. Go to [RunPod Serverless](https://www.runpod.io/serverless)
2. Click **"Create Endpoint"**
3. Choose **"Docker Image"**
4. Configure:
   ```
   Image Name: prodancristian/wan-ti2v-runpod:latest
   Entry Point: ["python", "handler.py"]
   ```

## Option 2: Use GitHub Repo with Dockerfile (Recommended)

### RunPod Configuration Settings

When using **"GitHub Repo"** option with Dockerfile:

```
Repository URL: https://github.com/ProdanCristian/wan-ti2v-runpod
Branch: main
Dockerfile Path: Dockerfile
Build Context: .
```

### Build Context Explanation

- **Branch**: `main` (your default branch)
- **Dockerfile Path**: `Dockerfile` (relative to repository root)
- **Build Context**: `.` (entire repository root directory)

This tells RunPod:
- Use the `main` branch of your repository
- Find the `Dockerfile` in the root directory
- Use the entire repository (`.`) as the build context

### Hardware Requirements

- **GPU**: RTX 4090, A10G, or A100 (minimum 12GB VRAM)
- **CPU**: 8+ cores
- **RAM**: 16GB+ (24GB+ recommended)
- **Storage**: 50GB+ (for model weights and Docker layers)

### Build Time Considerations

- Docker build will take ~10-15 minutes
- Model downloading happens at runtime (first request)
- Set cold start timeout to 900 seconds (15 minutes)

### Environment Variables (Optional)

```
HF_TOKEN=your_hugging_face_token
HF_HOME=/app/cache
TRANSFORMERS_CACHE=/app/cache
```

## Testing Your Docker Image Locally

```bash
# Test the Docker image locally (requires NVIDIA Docker)
docker run --gpus all -p 8080:8080 wan-ti2v-runpod:latest
```

## Dockerfile Features

✅ **CUDA 12.1 support** for GPU acceleration  
✅ **Python 3.10** with all dependencies  
✅ **FFmpeg** for video processing  
✅ **Optimized caching** with .dockerignore  
✅ **Model caching** in /app/cache directory  
✅ **Minimal size** by excluding unnecessary files  

## Troubleshooting

### Build Issues
- Ensure Docker has enough memory (8GB+)
- Check that all files are committed to Git
- Verify Dockerfile syntax

### Runtime Issues
- GPU not available: Check CUDA installation
- Out of memory: Reduce num_frames or image size
- Model download fails: Check internet connection and HF_TOKEN

### RunPod Specific
- Build timeout: Increase build timeout in settings
- Cold start timeout: Set to 900+ seconds
- Check RunPod logs for specific error messages