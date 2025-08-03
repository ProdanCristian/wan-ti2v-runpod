# Deployment Guide for Wan2.2-TI2V-5B on RunPod

## 🐍 **Python Deployment (Recommended)**

Your repository is now correctly configured for **Wan2.2-TI2V-5B** using the proper **WanPipeline**.

### **Key Fixes Applied:**
✅ **Correct Pipeline**: Using `WanPipeline` instead of `DiffusionPipeline`  
✅ **Right Model**: Using `Wan-AI/Wan2.2-TI2V-5B-Diffusers`  
✅ **Updated Dependencies**: Latest versions for WanPipeline support  
✅ **720P Support**: Native 1280x704 resolution at 24fps  
✅ **Proper VAE**: Using `AutoencoderKLWan` for high compression  

---

## 🚀 **RunPod Deployment Instructions**

### **1. Go to RunPod Serverless**
- Visit [RunPod Serverless](https://www.runpod.io/serverless)
- Click **"Create Endpoint"**

### **2. Choose "GitHub Repo"**
- Select the GitHub Repository option

### **3. Configuration Settings:**
```
Repository URL: https://github.com/ProdanCristian/wan-ti2v-runpod
Entry Point File: handler.py
Entry Point Function: handler
Python Version: 3.10+
```

**Leave these fields EMPTY:**
- Branch *(optional: can use "main")*
- Dockerfile Path *(leave empty)*
- Build Context *(leave empty)*

### **4. Hardware Configuration:**
```
GPU: RTX 4090, A10G, or A100 (minimum 24GB VRAM)
CPU: 8+ cores
RAM: 24GB+ (32GB recommended)
Storage: 50GB+ (model is ~70GB)
```

### **5. Worker Configuration:**
```
Max Workers: 1-2
Active Workers: 0 (testing) → 1 (production)
GPU Count: 1
Idle Timeout: 60 seconds
Execution Timeout: 900 seconds (15 minutes)
```

### **6. Timeout Settings:**
```
Cold Start Timeout: 900 seconds (15 minutes for model loading)
Active Timeout: 600 seconds (10 minutes per request)
```

---

## 📊 **Model Specifications**

| Feature | Value |
|---------|-------|
| **Resolution** | 1280x704 (720P) |
| **Max Frames** | 121 (5 seconds at 24fps) |
| **Model Size** | ~70GB |
| **VRAM Required** | 24GB+ |
| **Generation Time** | ~5-9 minutes per video |

---

## 🧪 **API Usage**

### **Input Format:**
```json
{
    "image": "<base64-encoded-image>",
    "prompt": "A beautiful sunset with moving clouds",
    "num_frames": 24,
    "fps": 24
}
```

### **Response Format:**
```json
{
    "video": "<base64-encoded-mp4>",
    "status": "success",
    "num_frames": 24,
    "fps": 24
}
```

### **Example cURL:**
```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "image": "<base64-image>",
    "prompt": "Cinematic style, magical transformation with sparkles",
    "num_frames": 48,
    "fps": 24
  }'
```

---

## 💰 **Cost Estimation**

| GPU Type | Cost/Hour | Video Generation |
|----------|-----------|------------------|
| **RTX 4090** | $0.40-0.60 | ~$0.05-0.10 per video |
| **A10G** | $0.50-0.80 | ~$0.06-0.12 per video |
| **A100** | $1.50-2.00 | ~$0.15-0.30 per video |

*Based on 5-9 minute generation time per video*

---

## 🛠️ **Troubleshooting**

### **Build Issues:**
- ❌ **"WanPipeline not found"**: Update to diffusers>=0.32.0
- ❌ **"Model not found"**: Ensure using `Wan-AI/Wan2.2-TI2V-5B-Diffusers`
- ❌ **Dependency conflicts**: Use exact versions from requirements.txt

### **Runtime Issues:**
- ❌ **CUDA OOM**: Use smaller num_frames (16-48)
- ❌ **Model loading timeout**: Increase cold start to 900s
- ❌ **Poor quality**: Add better prompts and use guidance_scale=5.0

### **Performance Tips:**
- 🎯 **Keep 1 active worker** to avoid cold starts
- 🎯 **Use num_frames=24-48** for best speed/quality balance
- 🎯 **Resize input images** to 512x512 before encoding
- 🎯 **Use descriptive prompts** for better video quality

---

## 🔧 **Advanced Configuration**

### **Environment Variables (Optional):**
```
HF_TOKEN=your_hugging_face_token
TORCH_HOME=/tmp/torch_cache
HF_HOME=/tmp/hf_cache
```

### **Model Parameters:**
- **Height**: 704 (fixed for 720P)
- **Width**: 1280 (fixed for 720P)
- **Max Frames**: 121 (5 seconds max)
- **Inference Steps**: 50 (quality vs speed)
- **Guidance Scale**: 5.0 (prompt adherence)

---

## ✅ **Deployment Checklist**

- [ ] Repository updated with correct WanPipeline implementation
- [ ] RunPod endpoint created with GitHub Repo option
- [ ] Hardware: 24GB+ VRAM GPU selected
- [ ] Timeouts: Cold start 900s, execution 600s
- [ ] Test with example_usage.py script
- [ ] Monitor costs and performance

Your **Wan2.2-TI2V-5B** deployment is now ready for **720P video generation**! 🎬