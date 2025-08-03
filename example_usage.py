#!/usr/bin/env python3
"""
Example usage script for the deployed Wan2.2-TI2V-5B API on RunPod
"""

import requests
import base64
import json
import time
from PIL import Image
import io

# Replace with your actual RunPod endpoint URL
RUNPOD_ENDPOINT = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run"
API_KEY = "YOUR_RUNPOD_API_KEY"  # Get this from RunPod dashboard

def image_to_base64(image_path):
    """Convert local image file to base64 string"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def base64_to_video(b64_string, output_path):
    """Convert base64 string back to video file"""
    video_data = base64.b64decode(b64_string)
    with open(output_path, "wb") as video_file:
        video_file.write(video_data)

def call_api(image_path, prompt="", num_frames=16, fps=24):
    """
    Call the RunPod API with an image and optional parameters
    
    Args:
        image_path (str): Path to input image
        prompt (str): Optional text prompt
        num_frames (int): Number of frames to generate (max 121)
        fps (int): Frames per second for output video
    
    Returns:
        dict: API response
    """
    
    # Convert image to base64
    print(f"Converting image: {image_path}")
    image_b64 = image_to_base64(image_path)
    
    # Prepare request payload
    payload = {
        "input": {
            "image": image_b64,
            "prompt": prompt,
            "num_frames": num_frames,
            "fps": fps
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print(f"Sending request to: {RUNPOD_ENDPOINT}")
    print(f"Parameters: prompt='{prompt}', frames={num_frames}, fps={fps}")
    
    # Send request
    response = requests.post(RUNPOD_ENDPOINT, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def main():
    """Example usage of the API"""
    
    # Example 1: Basic image-to-video with 720P output
    print("=== Example 1: Basic Image-to-Video (720P) ===")
    
    # You'll need to provide your own test image
    image_path = "test_image.jpg"  # Replace with your image path
    
    try:
        result = call_api(
            image_path=image_path,
            prompt="A beautiful sunset with moving clouds and gentle waves",
            num_frames=24,  # 1 second at 24fps
            fps=24
        )
        
        if result and result.get("status") == "success":
            print("✅ Video generation successful!")
            
            # Save the output video
            video_b64 = result.get("video")
            if video_b64:
                base64_to_video(video_b64, "output_video_720p.mp4")
                print("📹 Video saved as 'output_video_720p.mp4'")
            
            # Print stats
            print(f"📊 Generated {result.get('num_frames')} frames at {result.get('fps')} fps")
            print(f"🎬 Video resolution: 1280x704 (720P)")
            
        else:
            print("❌ Video generation failed!")
            if result:
                print(f"Error: {result.get('error')}")
                
    except FileNotFoundError:
        print(f"❌ Image file not found: {image_path}")
        print("Please provide a valid image file path")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Example 2: Longer video with different prompt
    print("\n=== Example 2: Longer Video (5 seconds) ===")
    
    try:
        result = call_api(
            image_path=image_path,
            prompt="Transform this into a magical scene with sparkles and ethereal light, cinematic style",
            num_frames=121,  # 5 seconds at 24fps (maximum)
            fps=24
        )
        
        if result and result.get("status") == "success":
            print("✅ Long video generation successful!")
            base64_to_video(result.get("video"), "output_video_5sec.mp4")
            print("📹 Video saved as 'output_video_5sec.mp4'")
            
    except Exception as e:
        print(f"❌ Error in second example: {str(e)}")

if __name__ == "__main__":
    # Check if endpoint URL and API key are set
    if "YOUR_ENDPOINT_ID" in RUNPOD_ENDPOINT or "YOUR_RUNPOD_API_KEY" in API_KEY:
        print("⚠️  Please update RUNPOD_ENDPOINT and API_KEY with your actual values!")
        print("Get these from your RunPod dashboard after deployment.")
    else:
        main()