#!/bin/bash

echo "🔄 Deploying persistent status feature..."

# Stop container
echo "Stopping container..."
sudo docker-compose -f docker-compose.prod.yml down

# Rebuild and start
echo "Rebuilding and starting container with persistent status..."
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
    echo "🌐 Open https://smtp.truongvinhkhuong.io.vn/ to see the persistent status"
    echo ""
    echo "📋 New status features:"
    echo "  - Status persists and doesn't disappear on refresh"
    echo "  - Only updates when there are actual changes"
    echo "  - Smooth progress bar animation"
    echo "  - Better status states with colors and animations"
    echo "  - Reset button to clear status when needed"
    echo "  - Formatted last processed info with icons"
    echo ""
    echo "🎯 Status improvements:"
    echo "  - Ready: Green"
    echo "  - Sending: Orange with pulse animation"
    echo "  - Completed: Green"
    echo "  - Completed with errors: Orange"
    echo "  - Smooth progress bar transitions"
    echo "  - Better time formatting"
    echo ""
    echo "🔧 Controls:"
    echo "  - Refresh: Update status manually"
    echo "  - Reset: Clear all status data"
    echo "  - Clear: Clear logs only"
else
    echo "❌ Health check failed"
    echo "Checking logs..."
    sudo docker logs naver-email-sender-prod --tail=20
fi

echo "✅ Persistent status deployment completed!"
