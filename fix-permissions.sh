#!/bin/bash

# Fix permissions script for production deployment
# This script fixes the logs permission issue

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# Remove existing containers and images
print_status "Cleaning up existing containers and images..."
docker-compose -f docker-compose.prod.yml down --rmi all --volumes --remove-orphans 2>/dev/null || true

# Create logs directory with proper permissions
print_status "Creating logs directory with proper permissions..."
mkdir -p logs
chmod 755 logs
chown -R 1000:1000 logs 2>/dev/null || chmod 777 logs

# Create other necessary directories
print_status "Creating necessary directories..."
mkdir -p static templates
chmod 755 static templates

# Rebuild and start containers
print_status "Rebuilding and starting containers..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for container to start
print_status "Waiting for container to start..."
sleep 10

# Check if container is running
print_status "Checking container status..."
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    print_success "Container started successfully!"
    
    # Check logs
    print_status "Checking application logs..."
    docker-compose -f docker-compose.prod.yml logs --tail=20
    
    # Test health endpoint
    print_status "Testing health endpoint..."
    if curl -f http://localhost:5005/health > /dev/null 2>&1; then
        print_success "Application is healthy!"
    else
        print_warning "Health check failed, but container is running"
    fi
else
    print_error "Container failed to start"
    print_status "Showing container logs:"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi

print_success "✅ Permission fix completed!"
print_success "Application should now be running without permission errors"
