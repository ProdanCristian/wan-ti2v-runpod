#!/usr/bin/env python3
"""
Test script for the Wan2.2-TI2V-5B handler
Run this locally to test your handler before deploying to RunPod
"""

import base64
import json
from PIL import Image
import io

def create_test_image():
    """Create a simple test image and encode it as base64"""
    # Create a simple test image (red square)
    img = Image.new('RGB', (512, 512), color='red')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_b64

def test_handler():
    """Test the handler function locally"""
    try:
        # Import handler
        from handler import handler
        
        # Create test event
        test_image = create_test_image()
        event = {
            "image": test_image,
            "prompt": "A red square transforming into a spinning cube",
            "num_frames": 8,  # Smaller for testing
            "fps": 4
        }
        
        print("Testing handler with test image...")
        print(f"Input: {json.dumps({k: v if k != 'image' else f'{v[:50]}...' for k, v in event.items()}, indent=2)}")
        
        # Run handler
        result = handler(event)
        
        # Check result
        if result.get("status") == "success":
            print("✅ Handler test successful!")
            print(f"Generated video with {result.get('num_frames')} frames at {result.get('fps')} fps")
            
            # Optionally save the video for inspection
            video_b64 = result.get("video")
            if video_b64:
                video_bytes = base64.b64decode(video_b64)
                with open("test_output.mp4", "wb") as f:
                    f.write(video_bytes)
                print("📹 Test video saved as 'test_output.mp4'")
        else:
            print("❌ Handler test failed!")
            print(f"Error: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_handler()