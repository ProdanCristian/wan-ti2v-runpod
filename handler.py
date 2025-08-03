# handler.py
import runpod
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import base64
import io
import tempfile
import os
import time
import logging
from torchvision.io import write_video

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def log_system_info():
    """Log system information for debugging"""
    logger.info("🖥️  System Information:")
    logger.info(f"   Python version: {torch.__version__}")
    logger.info(f"   PyTorch version: {torch.__version__}")
    logger.info(f"   CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.info(f"   CUDA device count: {torch.cuda.device_count()}")
        logger.info(f"   CUDA device name: {torch.cuda.get_device_name(0)}")
        logger.info(f"   CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # Log memory usage
    try:
        import psutil
        memory = psutil.virtual_memory()
        logger.info(f"   System RAM: {memory.total / 1024**3:.1f} GB")
        logger.info(f"   Available RAM: {memory.available / 1024**3:.1f} GB")
    except ImportError:
        logger.info("   psutil not available for memory info")

# Log startup information
logger.info("🚀 Starting Wan2.2-TI2V-5B RunPod Handler")
log_system_info()

# Load model once on cold start
logger.info("📥 Starting model download and loading...")
start_time = time.time()

try:
    logger.info("   Downloading model from Hugging Face...")
    pipe = DiffusionPipeline.from_pretrained(
        "Wan-AI/Wan2.2-TI2V-5B",
        torch_dtype=torch.float16,
        variant="fp16"
    )
    
    logger.info("   Moving model to CUDA...")
    pipe = pipe.to("cuda")
    
    load_time = time.time() - start_time
    logger.info(f"✅ Model loaded successfully in {load_time:.1f} seconds!")
    
    # Log memory usage after model loading
    if torch.cuda.is_available():
        memory_allocated = torch.cuda.memory_allocated(0) / 1024**3
        memory_reserved = torch.cuda.memory_reserved(0) / 1024**3
        logger.info(f"   CUDA memory allocated: {memory_allocated:.1f} GB")
        logger.info(f"   CUDA memory reserved: {memory_reserved:.1f} GB")
        
except Exception as e:
    logger.error(f"❌ Failed to load model: {str(e)}")
    raise e

logger.info("🎬 Handler ready for video generation requests!")

def handler(event):
    """
    RunPod serverless handler for Wan2.2-TI2V-5B text-to-video generation
    
    Args:
        event (dict): Contains the input data and request metadata
        
    Expected input format:
    {
        "input": {
            "image": "<base64-encoded-image>",
            "prompt": "Description of the video",
            "num_frames": 24,
            "fps": 24
        }
    }
    
    Returns:
        dict: Response containing the generated video or error
    """
    try:
        print("Processing video generation request...")
        
        # Extract input data from RunPod event structure
        input_data = event.get('input', {})
        
        # Get required parameters
        image_b64 = input_data.get('image')
        prompt = input_data.get('prompt', '')
        num_frames = input_data.get('num_frames', 24)
        fps = input_data.get('fps', 24)
        
        if not image_b64:
            return {"error": "Missing required 'image' parameter"}
        
        print(f"Prompt: {prompt}")
        print(f"Frames: {num_frames}, FPS: {fps}")
        
        # Decode the base64 image
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        print(f"Image loaded: {image.size}")

        # Run inference
        print("Running model inference...")
        result = pipe(image, prompt=prompt, num_frames=num_frames)
        video_tensor = result["video"]
        print("Video generation completed!")

        # Convert to video file in-memory
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            video_path = tmp.name
            write_video(video_path, video_tensor, fps=fps)

            with open(video_path, "rb") as f:
                video_b64 = base64.b64encode(f.read()).decode("utf-8")

        # Clean up temporary file
        os.remove(video_path)
        
        return {
            "video": video_b64,
            "status": "success",
            "num_frames": num_frames,
            "fps": fps,
            "prompt": prompt
        }

    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return {"error": str(e)}

# Start the RunPod serverless function
if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
