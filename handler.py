# handler.py
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import base64
import io

# Load model once on cold start
pipe = DiffusionPipeline.from_pretrained(
    "Wan-AI/Wan2.2-TI2V-5B",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

def handler(event):
    try:
        image_b64 = event["image"]
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Inference (you might need to adjust depending on pipeline type)
        result = pipe(image)
        video_tensor = result["video"]

        # Convert to video file in-memory
        # You can also use ffmpeg or torchvision.io.write_video
        from torchvision.io import write_video
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            video_path = tmp.name
            write_video(video_path, video_tensor, fps=8)

            with open(video_path, "rb") as f:
                video_b64 = base64.b64encode(f.read()).decode("utf-8")

        os.remove(video_path)
        return {"video": video_b64}

    except Exception as e:
        return {"error": str(e)}
