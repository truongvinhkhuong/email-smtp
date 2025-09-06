# Production Deployment Guide
## Domain: https://smtp.truongvinhkhuong.io.vn/

### 🚀 Quick Deploy

```bash
# 1. Clone repository
git clone <your-repo-url>
cd mail-test

# 2. Run production deployment script
sudo ./deploy-production.sh

# 3. Verify deployment
curl https://smtp.truongvinhkhuong.io.vn/health
```

### 📋 Prerequisites

- Ubuntu 20.04+ or CentOS 8+
- Root access
- Domain `smtp.truongvinhkhuong.io.vn` pointing to server IP
- Ports 80, 443, 22 open

### 🔧 Manual Setup

#### 1. Install Dependencies
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl enable docker
sudo systemctl start docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
sudo apt-get install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

#### 2. Configure Environment
```bash
# Copy production environment
cp production.env .env

# Edit credentials
nano .env
```

#### 3. Deploy Application
```bash
# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up --build -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

#### 4. Configure Nginx
```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/smtp.truongvinhkhuong.io.vn

# Enable site
sudo ln -s /etc/nginx/sites-available/smtp.truongvinhkhuong.io.vn /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

#### 5. Setup SSL Certificate
```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d smtp.truongvinhkhuong.io.vn
```

### 🔍 Verification

#### Health Check
```bash
# Application health
curl https://smtp.truongvinhkhuong.io.vn/health

# Expected response: "healthy"
```

#### Service Status
```bash
# Docker containers
docker-compose -f docker-compose.prod.yml ps

# Nginx status
sudo systemctl status nginx

# Application logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 📊 Monitoring

#### Application Logs
```bash
# Real-time logs
docker-compose -f docker-compose.prod.yml logs -f

# Nginx logs
sudo tail -f /var/log/nginx/smtp.truongvinhkhuong.io.vn.access.log
sudo tail -f /var/log/nginx/smtp.truongvinhkhuong.io.vn.error.log
```

#### System Monitoring
```bash
# Resource usage
docker stats

# Disk usage
df -h

# Memory usage
free -h
```

### 🔧 Management Commands

```bash
# Restart application
sudo systemctl restart naver-email-sender.service

# Stop application
sudo systemctl stop naver-email-sender.service

# View status
sudo systemctl status naver-email-sender.service

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 🛡️ Security Configuration

#### Firewall Setup
```bash
# Allow necessary ports
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# Enable firewall
sudo ufw enable
```

#### SSL Configuration
- TLS 1.2+ only
- Strong cipher suites
- HSTS enabled
- Security headers configured

#### Rate Limiting
- API endpoints: 10 requests/minute
- File upload: 5 requests/minute
- Burst protection enabled

### 🔄 Updates and Maintenance

#### Update Application
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up --build -d
```

#### Backup
```bash
# Backup application data
tar -czf backup-$(date +%Y%m%d).tar.gz logs/ static/ templates/

# Backup nginx config
sudo cp /etc/nginx/sites-available/smtp.truongvinhkhuong.io.vn backup-nginx.conf
```

#### Log Rotation
```bash
# Setup logrotate for nginx
sudo nano /etc/logrotate.d/nginx-smtp
```

### 🚨 Troubleshooting

#### Application Not Starting
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check environment
docker-compose -f docker-compose.prod.yml config

# Restart
docker-compose -f docker-compose.prod.yml restart
```

#### Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Restart nginx
sudo systemctl restart nginx
```

#### SSL Issues
```bash
# Check certificate
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Test SSL
openssl s_client -connect smtp.truongvinhkhuong.io.vn:443
```

### 📞 Support

#### Health Check URLs
- Application: `https://smtp.truongvinhkhuong.io.vn/health`
- Nginx: `https://smtp.truongvinhkhuong.io.vn/`

#### Log Locations
- Application: `logs/app.log`
- Nginx Access: `/var/log/nginx/smtp.truongvinhkhuong.io.vn.access.log`
- Nginx Error: `/var/log/nginx/smtp.truongvinhkhuong.io.vn.error.log`

#### Contact
- Technical issues: Check logs first
- Domain issues: Verify DNS settings
- SSL issues: Check certificate validity
