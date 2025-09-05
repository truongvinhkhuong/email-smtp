# 🚀 NAVER Vietnam AI Hackathon - Email Sender Deployment Guide

## 📋 Overview

This guide will help you deploy the Email Sender application to production on your server with domain `smtp.truongvinhkhuong.io.vn`.

## 🛠️ Prerequisites

- Ubuntu/Debian server with root access
- Python 3.6+ installed
- Nginx installed and running
- SSL certificate for your domain
- Domain `smtp.truongvinhkhuong.io.vn` pointing to your server

## 📦 Installation Steps

### 1. Prepare the Server

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create application user
sudo useradd -m -s /bin/bash emailsender
sudo usermod -aG www-data emailsender
```

### 2. Deploy Application

```bash
# Clone or upload the application to the server
cd /home/emailsender
# Upload your application files here

# Set proper ownership
sudo chown -R emailsender:www-data /home/emailsender/mail-test
sudo chmod -R 755 /home/emailsender/mail-test
```

### 3. Setup Virtual Environment

```bash
cd /home/emailsender/mail-test

# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure SSL Certificate

```bash
# Get SSL certificate using Let's Encrypt
sudo certbot --nginx -d smtp.truongvinhkhuong.io.vn

# Test certificate renewal
sudo certbot renew --dry-run
```

### 5. Configure Nginx

```bash
# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/smtp.truongvinhkhuong.io.vn

# Enable the site
sudo ln -s /etc/nginx/sites-available/smtp.truongvinhkhuong.io.vn /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 6. Configure Systemd Service

```bash
# Copy service file
sudo cp email-sender.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable email-sender
sudo systemctl start email-sender

# Check status
sudo systemctl status email-sender
```

### 7. Setup Logging

```bash
# Create log directory
sudo mkdir -p /var/log/email-sender
sudo chown emailsender:www-data /var/log/email-sender

# Configure logrotate
sudo tee /etc/logrotate.d/email-sender << EOF
/var/log/email-sender/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 emailsender www-data
}
EOF
```

## 🔧 Configuration

### Environment Variables

Create a production environment file:

```bash
sudo nano /home/emailsender/mail-test/.env
```

Add the following content:

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key
SENDER_EMAIL=khuonggg2924@gmail.com
SENDER_PASSWORD=oboxhjcfxkzqnpug
```

### Gmail App Password

Make sure you're using an App Password for Gmail:

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password instead of your regular password

## 🚀 Starting the Application

### Quick Start

```bash
# Make the startup script executable
chmod +x start_production.sh

# Run the startup script
./start_production.sh
```

### Manual Start

```bash
# Start the service
sudo systemctl start email-sender

# Check status
sudo systemctl status email-sender

# View logs
sudo journalctl -u email-sender -f
```

## 📊 Monitoring

### Health Check

```bash
# Check if application is responding
curl https://smtp.truongvinhkhuong.io.vn/health

# Expected response: "healthy"
```

### Log Monitoring

```bash
# View application logs
tail -f /home/emailsender/mail-test/app.log

# View systemd logs
sudo journalctl -u email-sender -f

# View nginx logs
sudo tail -f /var/log/nginx/smtp.truongvinhkhuong.io.vn.access.log
sudo tail -f /var/log/nginx/smtp.truongvinhkhuong.io.vn.error.log
```

## 🔄 Maintenance

### Updating the Application

```bash
# Stop the service
sudo systemctl stop email-sender

# Update code (replace with your update method)
# git pull origin main

# Activate virtual environment
cd /home/emailsender/mail-test
source env/bin/activate

# Update dependencies
pip install -r requirements.txt

# Start the service
sudo systemctl start email-sender
```

### Backup

```bash
# Create backup script
sudo tee /usr/local/bin/backup-email-sender.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/email-sender"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup application files
tar -czf $BACKUP_DIR/email-sender_$DATE.tar.gz /home/emailsender/mail-test

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /var/log/email-sender

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

sudo chmod +x /usr/local/bin/backup-email-sender.sh

# Add to crontab for daily backups
echo "0 2 * * * /usr/local/bin/backup-email-sender.sh" | sudo crontab -
```

## 🛡️ Security

### Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### SSL/TLS Security

The nginx configuration includes:
- TLS 1.2 and 1.3 only
- Strong cipher suites
- HSTS headers
- Security headers

### Application Security

- Rate limiting on API endpoints
- File upload restrictions
- Input validation
- Secure session configuration

## 🐛 Troubleshooting

### Common Issues

1. **Service won't start**
   ```bash
   sudo journalctl -u email-sender -n 50
   ```

2. **Nginx 502 Bad Gateway**
   ```bash
   # Check if service is running
   sudo systemctl status email-sender
   
   # Check nginx error logs
   sudo tail -f /var/log/nginx/error.log
   ```

3. **SSL Certificate Issues**
   ```bash
   # Check certificate status
   sudo certbot certificates
   
   # Renew certificate
   sudo certbot renew
   ```

4. **Email Sending Issues**
   ```bash
   # Check application logs
   tail -f /home/emailsender/mail-test/app.log
   
   # Test Gmail connection
   python3 -c "
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('khuonggg2924@gmail.com', 'oboxhjcfxkzqnpug')
   print('Gmail connection successful')
   server.quit()
   "
   ```

## 📞 Support

For issues or questions:
- Check the logs first
- Review this documentation
- Contact the development team

## 🔗 URLs

- **Application**: https://smtp.truongvinhkhuong.io.vn
- **Health Check**: https://smtp.truongvinhkhuong.io.vn/health
- **Status API**: https://smtp.truongvinhkhuong.io.vn/status
