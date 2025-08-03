# handler.py
import runpod
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import base64
import io
import tempfile
import os
from torchvision.io import write_video

# Load model once on cold start
print("Loading Wan2.2-TI2V-5B model...")
pipe = DiffusionPipeline.from_pretrained(
    "Wan-AI/Wan2.2-TI2V-5B",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")
print("Model loaded successfully!")

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
