#!/bin/bash

# NAVER Vietnam AI Hackathon - Production Deployment Script
# Domain: https://smtp.truongvinhkhuong.io.vn/

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="smtp.truongvinhkhuong.io.vn"
APP_PORT="5005"
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
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "Please run as root (use sudo)"
        exit 1
    fi
}

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        systemctl enable docker
        systemctl start docker
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Installing Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    
    # Check Nginx
    if ! command -v nginx &> /dev/null; then
        print_error "Nginx is not installed. Installing Nginx..."
        apt-get update
        apt-get install -y nginx
        systemctl enable nginx
        systemctl start nginx
    fi
    
    print_success "All requirements satisfied"
}

# Setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Copy production environment file
    if [ ! -f ".env" ]; then
        if [ -f "production.env" ]; then
            cp production.env .env
            print_warning "Please edit .env file with your actual credentials"
        else
            print_error "production.env file not found"
            exit 1
        fi
    fi
    
    # Create necessary directories
    mkdir -p logs
    mkdir -p static
    mkdir -p templates
    mkdir -p /var/log/nginx
    
    print_success "Environment setup completed"
}

# Configure Nginx
configure_nginx() {
    print_status "Configuring Nginx for domain: $DOMAIN"
    
    # Copy nginx configuration
    cp nginx.conf "$NGINX_CONFIG"
    
    # Enable site
    ln -sf "$NGINX_CONFIG" "$NGINX_ENABLED"
    
    # Remove default site if exists
    if [ -f "/etc/nginx/sites-enabled/default" ]; then
        rm -f /etc/nginx/sites-enabled/default
    fi
    
    # Test nginx configuration
    nginx -t
    
    # Reload nginx
    systemctl reload nginx
    
    print_success "Nginx configured for $DOMAIN"
}

# Deploy application
deploy_app() {
    print_status "Deploying application..."
    
    # Stop existing containers
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    
    # Build and start containers
    docker-compose -f docker-compose.prod.yml up --build -d
    
    # Wait for application to start
    sleep 10
    
    # Check if application is running
    if curl -f http://localhost:$APP_PORT/health > /dev/null 2>&1; then
        print_success "Application deployed successfully"
    else
        print_error "Application failed to start"
        docker-compose -f docker-compose.prod.yml logs
        exit 1
    fi
}

# Setup SSL (Let's Encrypt)
setup_ssl() {
    print_status "Setting up SSL certificate..."
    
    # Check if certbot is installed
    if ! command -v certbot &> /dev/null; then
        print_status "Installing Certbot..."
        apt-get update
        apt-get install -y certbot python3-certbot-nginx
    fi
    
    # Get SSL certificate
    certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    
    print_success "SSL certificate configured"
}

# Setup firewall
setup_firewall() {
    print_status "Configuring firewall..."
    
    # Allow SSH, HTTP, HTTPS
    ufw allow ssh
    ufw allow 80
    ufw allow 443
    
    # Enable firewall
    ufw --force enable
    
    print_success "Firewall configured"
}

# Setup monitoring
setup_monitoring() {
    print_status "Setting up monitoring..."
    
    # Create systemd service for auto-start
    cat > /etc/systemd/system/naver-email-sender.service << EOF
[Unit]
Description=NAVER Vietnam AI Hackathon Email Sender
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$(pwd)
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF
    
    # Enable service
    systemctl daemon-reload
    systemctl enable naver-email-sender.service
    
    print_success "Monitoring setup completed"
}

# Main deployment function
deploy() {
    print_status "Starting production deployment for $DOMAIN"
    
    check_root
    check_requirements
    setup_environment
    configure_nginx
    deploy_app
    setup_ssl
    setup_firewall
    setup_monitoring
    
    print_success "🎉 Production deployment completed!"
    print_success "Application is available at: https://$DOMAIN"
    print_success "Health check: https://$DOMAIN/health"
    
    # Show status
    print_status "Application status:"
    docker-compose -f docker-compose.prod.yml ps
    
    print_status "Nginx status:"
    systemctl status nginx --no-pager
    
    print_status "Service status:"
    systemctl status naver-email-sender.service --no-pager
}

# Show logs
show_logs() {
    docker-compose -f docker-compose.prod.yml logs -f
}

# Restart application
restart() {
    print_status "Restarting application..."
    systemctl restart naver-email-sender.service
    print_success "Application restarted"
}

# Stop application
stop() {
    print_status "Stopping application..."
    systemctl stop naver-email-sender.service
    print_success "Application stopped"
}

# Show status
status() {
    print_status "Application status:"
    docker-compose -f docker-compose.prod.yml ps
    
    print_status "Service status:"
    systemctl status naver-email-sender.service --no-pager
    
    print_status "Nginx status:"
    systemctl status nginx --no-pager
    
    print_status "Health check:"
    curl -f https://$DOMAIN/health && echo "✅ Healthy" || echo "❌ Unhealthy"
}

# Main script
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "logs")
        show_logs
        ;;
    "restart")
        restart
        ;;
    "stop")
        stop
        ;;
    "status")
        status
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy   - Deploy application to production (default)"
        echo "  logs     - Show application logs"
        echo "  restart  - Restart application"
        echo "  stop     - Stop application"
        echo "  status   - Show application status"
        echo "  help     - Show this help message"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' to see available commands"
        exit 1
        ;;
esac
