# Wan Ti2v Runpod

[![Runpod](https://api.runpod.io/badge/ProdanCristian/wan-ti2v-runpod)](https://console.runpod.io/hub/ProdanCristian/wan-ti2v-runpod)

AI-powered text-to-video generation using the Wan2.2-TI2V-5B model. Convert images into dynamic videos with text prompts for enhanced storytelling and content creation.

## Features

- **Text-to-Video Generation**: Transform static images into dynamic videos using AI
- **Customizable Parameters**: Control video length (frames) and frame rate (FPS)
- **GPU Optimized**: Optimized for RunPod's serverless GPU infrastructure
- **Base64 I/O**: Easy integration with web applications using base64 encoding

## Usage

### Input Parameters

- `image` (required): Base64-encoded input image
- `prompt` (optional): Text description to guide video generation
- `num_frames` (optional): Number of frames to generate (default: 24)
- `fps` (optional): Video frame rate (default: 24)

### Example Input

```json
{
  "input": {
    "image": "<base64-encoded-image>",
    "prompt": "A person walking through a beautiful garden",
    "num_frames": 24,
    "fps": 24
  }
}
```

### Example Output

```json
{
  "video": "<base64-encoded-video>",
  "status": "success",
  "num_frames": 24,
  "fps": 24,
  "prompt": "A person walking through a beautiful garden",
  "processing_time": {
    "decode_time": 0.12,
    "inference_time": 15.3,
    "encode_time": 2.1,
    "total_time": 17.5
  }
}
```

## Model Information

This serverless function uses the **Wan2.2-TI2V-5B** model from Hugging Face, which specializes in text-conditioned image-to-video generation.

## Requirements

- GPU with CUDA support
- 20GB+ container disk space
- RunPod serverless environment

## Deployment

Deploy this function on RunPod Serverless by:

1. Creating a new serverless endpoint
2. Using the provided Docker image
3. Configuring environment variables as needed

## Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run handler
python handler.py
```

## License

This project is open source and available under the MIT License.