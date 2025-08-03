# Wan2.2-TI2V-5B RunPod Serverless Deployment

This repository contains the serverless deployment code for the Wan2.2-TI2V-5B text/image-to-video model on RunPod.

## Model Information

- **Model**: [Wan-AI/Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)
- **Type**: Text/Image-to-Video Generation
- **Framework**: Diffusers (PyTorch)

## API Usage

### Input Format

```json
{
    "image": "<base64-encoded-image>",
    "prompt": "<optional-text-prompt>",
    "num_frames": 16,
    "fps": 8
}
```

### Response Format

```json
{
    "video": "<base64-encoded-mp4-video>",
    "status": "success",
    "num_frames": 16,
    "fps": 8
}
```

### Example Usage

```bash
curl -X POST https://your-runpod-endpoint.com/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "prompt": "A cat walking in a garden",
    "num_frames": 16,
    "fps": 8
  }'
```

## Deployment on RunPod

1. **Create Serverless Endpoint**:
   - Go to [RunPod Serverless](https://www.runpod.io/serverless)
   - Click "Create Endpoint"
   - Choose "GitHub Repo"

2. **Configuration**:
   - **Repository URL**: `https://github.com/yourusername/wan-ti2v-runpod`
   - **Entry Point File**: `handler.py`
   - **Entry Point Function**: `handler`
   - **Python Version**: 3.10+
   - **GPU**: A10G, RTX 4090, or A100 (recommended)
   - **Memory**: 16GB+ RAM
   - **Storage**: 50GB+ (for model weights)

3. **Environment Variables** (if needed):
   - `HF_TOKEN`: Your Hugging Face token (if model requires authentication)

## Hardware Requirements

- **GPU**: NVIDIA GPU with at least 12GB VRAM
- **RAM**: 16GB+ system RAM
- **Storage**: 50GB+ for model weights and temporary files

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Test locally (requires GPU)
python handler.py
```

## Notes

- Model loading takes ~2-3 minutes on first cold start
- Video generation takes ~30-60 seconds depending on parameters
- Output videos are in MP4 format, base64 encoded
- Maximum video length is limited by GPU memory

## Troubleshooting

### Common Issues

1. **CUDA out of memory**: Reduce `num_frames` or use smaller input images
2. **Model loading timeout**: Increase cold start timeout in RunPod settings
3. **Base64 encoding errors**: Ensure input image is properly encoded

### Support

For issues with the model itself, refer to the [official Hugging Face repository](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B).