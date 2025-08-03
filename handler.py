import runpod
import torch
from diffusers import WanPipeline, AutoencoderKLWan
from diffusers.utils import export_to_video
from PIL import Image
import base64
import io
import tempfile
import os
import logging
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the pipeline
pipe = None

def load_model():
    """Load the Wan2.2-TI2V-5B model once on cold start"""
    global pipe
    try:
        logger.info("Loading Wan2.2-TI2V-5B model...")
        
        # Use the Diffusers-compatible version
        model_id = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
        
        # Load VAE separately with float32 for stability
        vae = AutoencoderKLWan.from_pretrained(
            model_id, 
            subfolder="vae", 
            torch_dtype=torch.float32
        )
        
        # Load the main pipeline
        pipe = WanPipeline.from_pretrained(
            model_id,
            vae=vae,
            torch_dtype=torch.bfloat16
        ).to("cuda")
        
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise e

def handler(event):
    """
    RunPod serverless handler function
    
    Expected input:
    {
        "image": "<base64-encoded-image>",
        "prompt": "<optional-text-prompt>",
        "num_frames": 16,  # optional
        "fps": 8  # optional
    }
    
    Returns:
    {
        "video": "<base64-encoded-video>",
        "status": "success"
    }
    """
    global pipe
    
    # Load model if not already loaded
    if pipe is None:
        load_model()
    
    try:
        # Get input parameters
        image_b64 = event.get("image")
        prompt = event.get("prompt", "")
        num_frames = event.get("num_frames", 16)
        fps = event.get("fps", 8)
        
        if not image_b64:
            return {"error": "No image provided", "status": "error"}
        
        # Decode base64 image
        logger.info("Decoding input image...")
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Set video parameters for 720P generation
        height = 704
        width = 1280
        num_frames = min(num_frames, 121)  # Max supported frames
        num_inference_steps = 50
        guidance_scale = 5.0
        
        # Negative prompt for better quality
        negative_prompt = "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走"
        
        # Run inference
        logger.info("Running inference...")
        if prompt:
            # Text + Image to Video
            result = pipe(
                prompt=prompt,
                image=image,
                negative_prompt=negative_prompt,
                height=height,
                width=width,
                num_frames=num_frames,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps
            )
        else:
            # Image-to-video only (still need a prompt for this model)
            default_prompt = "high quality, detailed, smooth motion"
            result = pipe(
                prompt=default_prompt,
                image=image,
                negative_prompt=negative_prompt,
                height=height,
                width=width,
                num_frames=num_frames,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps
            )
        
        # Get video frames
        video_frames = result.frames[0]  # Get first batch
        
        # Convert frames to video and encode as base64
        logger.info("Converting frames to video...")
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            video_path = tmp_file.name
            
            # Use diffusers export_to_video function
            export_to_video(video_frames, video_path, fps=fps)
            
            # Read video file and encode as base64
            with open(video_path, "rb") as f:
                video_b64 = base64.b64encode(f.read()).decode("utf-8")
            
            # Clean up temporary file
            os.remove(video_path)
        
        logger.info("Inference completed successfully!")
        return {
            "video": video_b64,
            "status": "success",
            "num_frames": len(video_frames),
            "fps": fps
        }
        
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}")
        return {"error": str(e), "status": "error"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})