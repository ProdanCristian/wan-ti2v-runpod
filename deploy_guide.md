# Deployment Guide for Wan2.2-TI2V-5B on RunPod

## Step-by-Step Deployment Instructions

### 1. Upload to GitHub

1. **Create a new GitHub repository**:
   - Go to [GitHub](https://github.com) and create a new repository
   - Name it something like `wan-ti2v-runpod`
   - Make it public (or private if you have RunPod Pro)

2. **Upload these files**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Wan2.2-TI2V-5B RunPod deployment"
   git branch -M main
   git remote add origin https://github.com/yourusername/wan-ti2v-runpod.git
   git push -u origin main
   ```

### 2. Deploy on RunPod

1. **Go to RunPod Serverless**:
   - Visit [RunPod Serverless](https://www.runpod.io/serverless)
   - Click "Create Endpoint"

2. **Choose "GitHub Repo"**:
   - Select the GitHub Repository option

3. **Configure Deployment**:
   ```
   Repository URL: https://github.com/yourusername/wan-ti2v-runpod
   Entry Point File: handler.py
   Entry Point Function: handler
   Python Version: 3.10+
   ```

4. **Choose Hardware**:
   - **GPU**: RTX 4090, A10G, or A100 (minimum 12GB VRAM)
   - **CPU**: 8+ cores
   - **RAM**: 16GB+ (24GB+ recommended)
   - **Storage**: 50GB+ (for model weights)

5. **Advanced Settings**:
   - **Cold Start Timeout**: 600 seconds (10 minutes for model loading)
   - **Active Timeout**: 300 seconds (5 minutes per request)
   - **Max Workers**: 1-3 (depending on your budget)

### 3. Environment Variables (Optional)

If the model requires authentication:
```
HF_TOKEN=your_hugging_face_token
```

### 4. Test Deployment

Once deployed, you'll get an endpoint URL like:
```
https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run
```

Use the `example_usage.py` script to test your deployment.

## Estimated Costs

- **A10G (24GB)**: ~$0.50-0.80 per hour
- **RTX 4090 (24GB)**: ~$0.40-0.60 per hour  
- **A100 (40GB)**: ~$1.50-2.00 per hour

Each video generation takes ~30-60 seconds, so budget accordingly.

## Troubleshooting

### Common Issues:

1. **"CUDA out of memory"**:
   - Reduce `num_frames` in your requests
   - Use smaller input images (resize to 512x512)
   - Choose GPU with more VRAM

2. **"Model loading timeout"**:
   - Increase cold start timeout to 900 seconds
   - The model is ~10GB and takes time to download

3. **"Handler function not found"**:
   - Ensure `handler.py` is in the root of your repo
   - Check that the function is named exactly `handler`

4. **Import errors**:
   - Verify all packages in `requirements.txt` are correct
   - Some packages may need specific versions

### Performance Tips:

- Keep at least 1 worker active to avoid cold starts
- Use smaller frame counts (8-16) for faster generation
- Resize input images to 512x512 for optimal performance