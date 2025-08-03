import runpod
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import base64
import io
import tempfile
import os
import logging

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
        pipe = DiffusionPipeline.from_pretrained(
            "Wan-AI/Wan2.2-TI2V-5B",
            torch_dtype=torch.float16,
            variant="fp16"
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
        
        # Run inference
        logger.info("Running inference...")
        if prompt:
            # If prompt is provided, use text + image
            result = pipe(
                prompt=prompt,
                image=image,
                num_frames=num_frames,
                guidance_scale=7.5,
                num_inference_steps=25
            )
        else:
            # Image-to-video only
            result = pipe(
                image=image,
                num_frames=num_frames,
                guidance_scale=7.5,
                num_inference_steps=25
            )
        
        # Get video frames
        video_frames = result.frames[0]  # Get first batch
        
        # Convert frames to video and encode as base64
        logger.info("Converting frames to video...")
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            video_path = tmp_file.name
            
            # Use imageio to create video from frames
            import imageio
            with imageio.get_writer(video_path, fps=fps) as writer:
                for frame in video_frames:
                    writer.append_data(frame)
            
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