#!/bin/bash

# NAVER Vietnam AI Hackathon - Docker Deployment Script
# This script helps you deploy the email sender application using Docker Compose

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if .env file exists
check_env() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from env.example..."
        if [ -f "env.example" ]; then
            cp env.example .env
            print_warning "Please edit .env file with your actual email credentials before running again."
            print_warning "Required variables: SENDER_EMAIL, SENDER_PASSWORD"
            exit 1
        else
            print_error "env.example file not found. Please create .env file manually."
            exit 1
        fi
    fi
    print_success ".env file found"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p logs
    mkdir -p static
    mkdir -p templates
    print_success "Directories created"
}

# Build and start containers
deploy() {
    local mode=${1:-dev}
    if [ "$mode" = "prod" ]; then
        print_status "Building and starting containers in PRODUCTION mode..."
        docker-compose -f docker-compose.prod.yml up --build -d
    else
        print_status "Building and starting containers in DEVELOPMENT mode..."
        docker-compose up --build -d
    fi
    print_success "Containers started successfully"
}

# Show status
show_status() {
    print_status "Container status:"
    docker-compose ps
    
    print_status "Application logs:"
    docker-compose logs --tail=20 email-sender
}

# Stop containers
stop() {
    print_status "Stopping containers..."
    docker-compose down
    print_success "Containers stopped"
}

# Show logs
logs() {
    docker-compose logs -f email-sender
}

# Restart containers
restart() {
    print_status "Restarting containers..."
    docker-compose restart
    print_success "Containers restarted"
}

# Clean up
cleanup() {
    print_status "Cleaning up containers and images..."
    docker-compose down --rmi all --volumes --remove-orphans
    print_success "Cleanup completed"
}

# Main script
case "${1:-deploy}" in
    "deploy")
        check_docker
        check_env
        create_directories
        deploy
        show_status
        print_success "Deployment completed! Application is running on http://localhost:5005"
        ;;
    "deploy-prod")
        check_docker
        check_env
        create_directories
        deploy prod
        show_status
        print_success "Production deployment completed! Application is running on http://localhost:5005"
        ;;
    "stop")
        stop
        ;;
    "restart")
        restart
        ;;
    "logs")
        logs
        ;;
    "status")
        show_status
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy       - Build and start containers in development mode (default)"
        echo "  deploy-prod  - Build and start containers in production mode"
        echo "  stop         - Stop containers"
        echo "  restart      - Restart containers"
        echo "  logs         - Show application logs"
        echo "  status       - Show container status"
        echo "  cleanup      - Remove containers and images"
        echo "  help         - Show this help message"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' to see available commands"
        exit 1
        ;;
esac
