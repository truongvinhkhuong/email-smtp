#!/bin/bash

echo "🔧 Fixing logs permission issue..."

# Stop container
echo "Stopping container..."
sudo docker-compose -f docker-compose.prod.yml down

# Remove old container
echo "Removing old container..."
sudo docker-compose -f docker-compose.prod.yml down --rmi all --volumes --remove-orphans

# Create logs directory with proper permissions
echo "Creating logs directory..."
mkdir -p logs
sudo chmod 777 logs

# Rebuild and start
echo "Rebuilding and starting container..."
sudo docker-compose -f docker-compose.prod.yml up --build -d

# Wait and check
echo "Waiting for container to start..."
sleep 15

echo "Checking status..."
sudo docker-compose -f docker-compose.prod.yml ps

echo "Checking logs..."
sudo docker logs naver-email-sender-prod --tail=10

echo "✅ Fix completed! Check the logs above for any remaining errors."
