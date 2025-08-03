#!/bin/bash

# Build script for Wan2.2-TI2V-5B with verbose logging
# Usage: ./build.sh [your-dockerhub-username]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DOCKER_USERNAME=${1:-"your-username"}
IMAGE_NAME="wan-ti2v-runpod"
TAG="latest"

echo -e "${BLUE}🚀 Starting Wan2.2-TI2V-5B Docker Build${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Build Configuration:${NC}"
echo -e "   Docker Username: ${DOCKER_USERNAME}"
echo -e "   Image Name: ${IMAGE_NAME}"
echo -e "   Full Tag: ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"
echo ""

# Show disk space
echo -e "${YELLOW}💾 Available Disk Space:${NC}"
df -h . | tail -1 | awk '{print "   Available: " $4 " (" $5 " used)"}'
echo ""

# Build with verbose logging
echo -e "${GREEN}🔨 Building Docker image with verbose logging...${NC}"
echo -e "${YELLOW}⏱️  This may take 10-20 minutes depending on your internet connection${NC}"
echo ""

# Use BuildKit for better logging
export DOCKER_BUILDKIT=1

# Build the image
docker build \
    --progress=plain \
    --no-cache \
    --platform linux/amd64 \
    --tag "${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}" \
    --tag "${DOCKER_USERNAME}/${IMAGE_NAME}:latest" \
    . || {
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}✅ Build completed successfully!${NC}"

# Show image info
echo ""
echo -e "${YELLOW}📊 Image Information:${NC}"
docker images "${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}" --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

echo ""
echo -e "${BLUE}🚀 Next Steps:${NC}"
echo -e "   1. Test locally: ${YELLOW}docker run --rm ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}${NC}"
echo -e "   2. Push to registry: ${YELLOW}docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}${NC}"
echo -e "   3. Deploy on RunPod using: ${YELLOW}docker.io/${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}${NC}"
echo ""

# Ask if user wants to push
read -p "Do you want to push the image to Docker Hub now? [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}📤 Pushing to Docker Hub...${NC}"
    docker push "${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}" || {
        echo -e "${RED}❌ Push failed! Make sure you're logged in with 'docker login'${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ Image pushed successfully!${NC}"
    echo -e "${BLUE}🎬 Ready for RunPod deployment!${NC}"
else
    echo -e "${YELLOW}⏸️  Skipping push. Run 'docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}' when ready.${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Build process complete!${NC}"