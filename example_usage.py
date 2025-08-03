#!/usr/bin/env python3
"""
Example usage script for the Wan2.2-TI2V-5B RunPod serverless endpoint
"""

import requests
import base64
import json
import time
from PIL import Image
import io

def image_to_base64(image_path):
    """Convert image file to base64 string"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def create_test_image():
    """Create a simple test image and return as base64"""
    # Create a simple 512x512 test image
    img = Image.new('RGB', (512, 512), color='skyblue')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    
    return base64.b64encode(img_bytes).decode('utf-8')

def test_runpod_endpoint():
    """Test the RunPod serverless endpoint"""
    
    # Your RunPod endpoint details
    ENDPOINT_ID = "YOUR_ENDPOINT_ID"  # Replace with your actual endpoint ID
    API_KEY = "YOUR_API_KEY"          # Replace with your actual API key
    
    # RunPod API URLs
    run_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    status_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Create test input
    test_image_b64 = create_test_image()
    
    payload = {
        "input": {
            "image": test_image_b64,
            "prompt": "A magical transformation with sparkling effects and smooth motion",
            "num_frames": 24,
            "fps": 24
        }
    }
    
    print("🚀 Sending request to RunPod endpoint...")
    print(f"Prompt: {payload['input']['prompt']}")
    print(f"Frames: {payload['input']['num_frames']}")
    
    # Send the request
    try:
        response = requests.post(run_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        job_id = result.get('id')
        
        print(f"✅ Job submitted successfully! Job ID: {job_id}")
        
        # Poll for results
        print("⏳ Waiting for video generation...")
        
        while True:
            status_response = requests.get(f"{status_url}{job_id}", headers=headers)
            status_result = status_response.json()
            
            status = status_result.get('status')
            print(f"Status: {status}")
            
            if status == 'COMPLETED':
                output = status_result.get('output', {})
                if 'video' in output:
                    print("🎬 Video generated successfully!")
                    
                    # Save the video
                    video_b64 = output['video']
                    video_bytes = base64.b64decode(video_b64)
                    
                    with open('generated_video.mp4', 'wb') as f:
                        f.write(video_bytes)
                    
                    print("💾 Video saved as 'generated_video.mp4'")
                    print(f"📊 Execution time: {status_result.get('executionTime', 'N/A')}ms")
                    break
                else:
                    print("❌ No video in output:", output)
                    break
                    
            elif status == 'FAILED':
                print("❌ Job failed:", status_result.get('error', 'Unknown error'))
                break
                
            elif status in ['IN_QUEUE', 'IN_PROGRESS']:
                time.sleep(10)  # Wait 10 seconds before checking again
                continue
            else:
                print(f"🤔 Unknown status: {status}")
                time.sleep(5)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_local_handler():
    """Test the handler locally (requires dependencies installed)"""
    print("🧪 Testing handler locally...")
    
    try:
        from handler import handler
        
        test_image_b64 = create_test_image()
        
        event = {
            'input': {
                'image': test_image_b64,
                'prompt': 'A beautiful cinematic scene with gentle movement',
                'num_frames': 8,  # Smaller for faster local testing
                'fps': 8
            }
        }
        
        result = handler(event)
        
        if 'error' in result:
            print(f"❌ Handler error: {result['error']}")
        else:
            print("✅ Handler executed successfully!")
            print(f"📊 Response keys: {list(result.keys())}")
            
    except ImportError as e:
        print(f"❌ Cannot import handler: {e}")
    except Exception as e:
        print(f"❌ Local test failed: {e}")

if __name__ == "__main__":
    print("Wan2.2-TI2V-5B RunPod Test Script")
    print("=" * 40)
    
    choice = input("Test (1) Local handler or (2) RunPod endpoint? [1/2]: ").strip()
    
    if choice == "1":
        test_local_handler()
    elif choice == "2":
        print("\n⚠️  Make sure to update ENDPOINT_ID and API_KEY in the script!")
        confirm = input("Continue with RunPod test? [y/N]: ").strip().lower()
        if confirm == 'y':
            test_runpod_endpoint()
        else:
            print("Test cancelled.")
    else:
        print("Invalid choice. Please run again and select 1 or 2.")