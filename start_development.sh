#!/bin/bash

# NAVER Vietnam AI Hackathon - Email Sender Development Startup Script

set -e

echo "🚀 Starting NAVER Vietnam AI Hackathon Email Sender (Development Mode)..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/Users/khuong/Khuong-D/mail-test"
VENV_DIR="$APP_DIR/env"

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

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    print_error "Virtual environment not found at $VENV_DIR"
    print_status "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

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
chmod 755 "$APP_DIR/start_development.sh"
chmod 755 "$APP_DIR/start_production.sh"

# Test Gmail connection
print_status "Testing Gmail SMTP connection..."
python3 -c "
import smtplib
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('khuonggg2924@gmail.com', 'oboxhjcfxkzqnpug')
    print('✅ Gmail SMTP connection successful')
    server.quit()
except Exception as e:
    print(f'❌ Gmail SMTP connection failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    print_success "Gmail connection test passed"
else
    print_error "Gmail connection test failed"
    exit 1
fi

# Start the Flask development server
print_success "🎉 Starting Flask development server..."
echo ""
echo "📋 Application Information:"
echo "   • URL: http://localhost:5005"
echo "   • Environment: Development"
echo "   • Debug Mode: Enabled"
echo ""
echo "🔧 Available Commands:"
echo "   • Test application: python3 test_app.py"
echo "   • View logs: tail -f app.log"
echo "   • Stop server: Ctrl+C"
echo ""

# Start Flask app
cd "$APP_DIR"
python3 app.py
