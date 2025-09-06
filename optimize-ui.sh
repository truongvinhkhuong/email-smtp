#!/bin/bash

echo "🎨 Optimizing UI for stable logs display..."

# Stop container
echo "Stopping container..."
sudo docker-compose -f docker-compose.prod.yml down

# Rebuild and start
echo "Rebuilding and starting container with optimized UI..."
sudo docker-compose -f docker-compose.prod.yml up --build -d

# Wait for container to start
echo "Waiting for container to start..."
sleep 15

# Check status
echo "Checking container status..."
sudo docker-compose -f docker-compose.prod.yml ps

# Test health endpoint
echo "Testing health endpoint..."
if curl -f http://localhost:5005/health > /dev/null 2>&1; then
    echo "✅ Application is healthy!"
    echo "🌐 Open https://smtp.truongvinhkhuong.io.vn/ to see the optimized UI"
    echo ""
    echo "📋 Improvements made:"
    echo "  - Removed unnecessary icons and buttons"
    echo "  - Optimized polling frequency (2 seconds)"
    echo "  - Added smart update (only when new logs)"
    echo "  - Improved CSS for better readability"
    echo "  - Reduced console logging"
else
    echo "❌ Health check failed"
    echo "Checking logs..."
    sudo docker logs naver-email-sender-prod --tail=20
fi

echo "✅ UI optimization completed!"
