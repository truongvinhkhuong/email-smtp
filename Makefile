# NAVER Vietnam AI Hackathon - Email Sender Makefile
# Make commands for easy Docker management

.PHONY: help build up down restart logs status clean deploy deploy-prod

# Default target
help:
	@echo "NAVER Vietnam AI Hackathon - Email Sender"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make build        - Build Docker image"
	@echo "  make up           - Start containers (development)"
	@echo "  make up-prod      - Start containers (production)"
	@echo "  make down         - Stop containers"
	@echo "  make restart      - Restart containers"
	@echo "  make logs         - Show application logs"
	@echo "  make status       - Show container status"
	@echo "  make clean        - Remove containers and images"
	@echo "  make deploy       - Deploy application (development)"
	@echo "  make deploy-prod  - Deploy application (production)"
	@echo "  make shell        - Open shell in container"
	@echo "  make health       - Check application health"
	@echo ""

# Build Docker image
build:
	@echo "Building Docker image..."
	docker-compose build

# Start containers (development)
up:
	@echo "Starting containers in development mode..."
	docker-compose up -d
	@echo "Application is running on http://localhost:5005"

# Start containers (production)
up-prod:
	@echo "Starting containers in production mode..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Application is running on http://localhost:5005"

# Stop containers
down:
	@echo "Stopping containers..."
	docker-compose down

# Restart containers
restart:
	@echo "Restarting containers..."
	docker-compose restart

# Show logs
logs:
	@echo "Showing application logs..."
	docker-compose logs -f email-sender

# Show status
status:
	@echo "Container status:"
	docker-compose ps
	@echo ""
	@echo "Resource usage:"
	docker stats --no-stream

# Clean up
clean:
	@echo "Cleaning up containers and images..."
	docker-compose down --rmi all --volumes --remove-orphans
	@echo "Cleanup completed"

# Deploy (development)
deploy: build up
	@echo "Deployment completed!"

# Deploy (production)
deploy-prod:
	@echo "Deploying in production mode..."
	docker-compose -f docker-compose.prod.yml up --build -d
	@echo "Production deployment completed!"

# Open shell in container
shell:
	@echo "Opening shell in container..."
	docker-compose exec email-sender /bin/bash

# Health check
health:
	@echo "Checking application health..."
	@curl -f http://localhost:5005/health && echo "✅ Application is healthy" || echo "❌ Application is not responding"

# Install dependencies (for development)
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

# Run tests
test:
	@echo "Running tests..."
	python -m pytest test_*.py -v

# Format code
format:
	@echo "Formatting code..."
	black *.py
	isort *.py

# Lint code
lint:
	@echo "Linting code..."
	flake8 *.py
	pylint *.py
