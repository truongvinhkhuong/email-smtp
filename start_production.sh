#!/bin/bash

# NAVER Vietnam AI Hackathon - Email Sender Production Startup Script
# Domain: smtp.truongvinhkhuong.io.vn

set -e

echo "🚀 Starting NAVER Vietnam AI Hackathon Email Sender..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/Users/khuong/Khuong-D/mail-test"
SERVICE_NAME="email-sender"
NGINX_CONFIG="/etc/nginx/sites-available/smtp.truongvinhkhuong.io.vn"
NGINX_ENABLED="/etc/nginx/sites-enabled/smtp.truongvinhkhuong.io.vn"

# Function to print colored output
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

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Check if virtual environment exists
if [ ! -d "$APP_DIR/env" ]; then
    print_error "Virtual environment not found at $APP_DIR/env"
    print_status "Please run: python3 -m venv env && source env/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source "$APP_DIR/env/bin/activate"

# Install/update dependencies
print_status "Installing/updating dependencies..."
pip install -r requirements.txt

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p "$APP_DIR/logs"
mkdir -p "$APP_DIR/uploads"
mkdir -p "$APP_DIR/static"

# Set proper permissions
print_status "Setting permissions..."
chmod 755 "$APP_DIR"
chmod 644 "$APP_DIR"/*.py
chmod 644 "$APP_DIR"/*.txt
chmod 644 "$APP_DIR"/*.conf
chmod 755 "$APP_DIR/start_production.sh"

# Copy nginx configuration
print_status "Configuring Nginx..."
if [ -f "$APP_DIR/nginx.conf" ]; then
    sudo cp "$APP_DIR/nginx.conf" "$NGINX_CONFIG"
    sudo ln -sf "$NGINX_CONFIG" "$NGINX_ENABLED"
    print_success "Nginx configuration copied"
else
    print_warning "Nginx configuration file not found"
fi

# Test nginx configuration
print_status "Testing Nginx configuration..."
if sudo nginx -t; then
    print_success "Nginx configuration is valid"
else
    print_error "Nginx configuration test failed"
    exit 1
fi

# Copy systemd service file
print_status "Configuring systemd service..."
if [ -f "$APP_DIR/$SERVICE_NAME.service" ]; then
    sudo cp "$APP_DIR/$SERVICE_NAME.service" "/etc/systemd/system/"
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    print_success "Systemd service configured"
else
    print_warning "Systemd service file not found"
fi

# Start services
print_status "Starting services..."

# Start the application service
if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
    print_status "Restarting $SERVICE_NAME service..."
    sudo systemctl restart "$SERVICE_NAME"
else
    print_status "Starting $SERVICE_NAME service..."
    sudo systemctl start "$SERVICE_NAME"
fi

# Start nginx
if sudo systemctl is-active --quiet nginx; then
    print_status "Reloading Nginx..."
    sudo systemctl reload nginx
else
    print_status "Starting Nginx..."
    sudo systemctl start nginx
fi

# Check service status
print_status "Checking service status..."
if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
    print_success "Email sender service is running"
else
    print_error "Email sender service failed to start"
    sudo systemctl status "$SERVICE_NAME"
    exit 1
fi

if sudo systemctl is-active --quiet nginx; then
    print_success "Nginx is running"
else
    print_error "Nginx failed to start"
    sudo systemctl status nginx
    exit 1
fi

# Show service information
print_success "🎉 Email Sender is now running!"
echo ""
echo "📋 Service Information:"
echo "   • Application URL: https://smtp.truongvinhkhuong.io.vn"
echo "   • Service Status: $(sudo systemctl is-active $SERVICE_NAME)"
echo "   • Nginx Status: $(sudo systemctl is-active nginx)"
echo ""
echo "🔧 Management Commands:"
echo "   • View logs: sudo journalctl -u $SERVICE_NAME -f"
echo "   • Restart service: sudo systemctl restart $SERVICE_NAME"
echo "   • Stop service: sudo systemctl stop $SERVICE_NAME"
echo "   • Check status: sudo systemctl status $SERVICE_NAME"
echo ""
echo "📊 Monitoring:"
echo "   • Health check: curl https://smtp.truongvinhkhuong.io.vn/health"
echo "   • Application logs: tail -f $APP_DIR/app.log"
echo ""

# Test the application
print_status "Testing application..."
if curl -s -o /dev/null -w "%{http_code}" https://smtp.truongvinhkhuong.io.vn/health | grep -q "200"; then
    print_success "Application is responding correctly"
else
    print_warning "Application health check failed - please check logs"
fi

print_success "Setup completed successfully! 🚀"
