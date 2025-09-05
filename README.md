# 🚀 NAVER Vietnam AI Hackathon - Email Sender

## 📋 Overview
A comprehensive web application for sending bulk emails to hackathon participants with a modern UI and production-ready deployment configuration.

## ✨ Features
- **Modern Web UI** - Beautiful, responsive interface with real-time status updates
- **CSV Upload** - Easy file upload with validation
- **Bulk Email Sending** - Send personalized emails to hundreds of participants
- **Real-time Monitoring** - Live progress tracking and logging
- **Gmail Integration** - Pre-configured with Gmail SMTP
- **Production Ready** - Nginx configuration and systemd service
- **Security** - Rate limiting, SSL/TLS, and secure headers
- **Resume Functionality** - Continue interrupted email campaigns

## 🛠️ Quick Start

### Development Mode
```bash
# Make scripts executable
chmod +x start_development.sh start_production.sh

# Start development server
./start_development.sh
```

### Production Deployment
```bash
# Deploy to production
./start_production.sh
```

## 📁 Project Structure
```
├── app.py                    # Main Flask application
├── config.py                 # Email and SMTP configuration
├── templates/
│   └── index.html           # Web UI template
├── requirements.txt          # Python dependencies
├── nginx.conf               # Nginx configuration
├── email-sender.service     # Systemd service file
├── gunicorn.conf.py         # Gunicorn configuration
├── start_development.sh     # Development startup script
├── start_production.sh      # Production deployment script
├── test_app.py              # Application testing script
├── production.env           # Production environment variables
└── DEPLOYMENT.md            # Detailed deployment guide
```

## 🌐 Web Interface

### Main Features
- **File Upload**: Drag & drop CSV file upload
- **Real-time Status**: Live progress tracking
- **Email Control**: Start/stop email sending
- **Logs Viewer**: Real-time log monitoring
- **Responsive Design**: Works on desktop and mobile

### URL Endpoints
- `/` - Main application interface
- `/upload` - CSV file upload
- `/start_sending` - Start email campaign
- `/stop_sending` - Stop email campaign
- `/status` - Get sending status (JSON)
- `/logs` - Get recent logs (JSON)
- `/health` - Health check endpoint

## 📧 Email Configuration

### Gmail Setup
The application is pre-configured with:
- **Email**: khuonggg2924@gmail.com
- **Password**: oboxhjcfxkzqnpug (App Password)

### CSV Format
Create a CSV file with participant data:
```csv
identifier,name
email1@example.com,John Doe
email2@example.com,Jane Smith
```

## 🚀 Production Deployment

### Prerequisites
- Ubuntu/Debian server
- Python 3.6+
- Nginx
- SSL certificate for your domain

### Domain Configuration
- **Domain**: smtp.truongvinhkhuong.io.vn
- **SSL**: Automatic Let's Encrypt setup
- **Security**: Rate limiting and secure headers

### Deployment Steps
1. **Upload files** to your server
2. **Run deployment script**: `./start_production.sh`
3. **Configure SSL**: Automatic with Let's Encrypt
4. **Access application**: https://smtp.truongvinhkhuong.io.vn

## 🔧 Configuration

### Environment Variables
```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key

# Email Configuration
SENDER_EMAIL=khuonggg2924@gmail.com
SENDER_PASSWORD=oboxhjcfxkzqnpug

# Email Sending Settings
BATCH_SIZE=100
DELAY_BETWEEN_BATCHES=300
DELAY_BETWEEN_EMAILS=1
```

### Customization
Edit `config.py` to modify:
- Email templates
- SMTP settings
- Batch processing parameters
- UI theme colors

## 📊 Monitoring & Logs

### Real-time Monitoring
- Live progress bar
- Email count tracking
- Error monitoring
- Batch progress

### Log Files
- `app.log` - Application logs
- `logs/access.log` - Web access logs
- `logs/error.log` - Error logs

### Health Checks
```bash
# Check application health
curl https://smtp.truongvinhkhuong.io.vn/health

# Check service status
sudo systemctl status email-sender
```

## 🧪 Testing

### Run Tests
```bash
# Test all functionality
python3 test_app.py

# Test with custom URL
python3 test_app.py https://smtp.truongvinhkhuong.io.vn
```

### Test Coverage
- Health check endpoint
- Gmail SMTP connection
- CSV upload functionality
- Status and logs endpoints
- Email sending process

## 🛡️ Security Features

### Application Security
- Rate limiting on API endpoints
- File upload validation
- Input sanitization
- Secure session configuration

### Server Security
- SSL/TLS encryption
- Security headers
- Firewall configuration
- Process isolation

### Email Security
- App password authentication
- SMTP over TLS
- Email validation
- Batch processing limits

## 🔄 Maintenance

### Updates
```bash
# Stop service
sudo systemctl stop email-sender

# Update code
git pull origin main

# Restart service
sudo systemctl start email-sender
```

### Backup
```bash
# Automatic daily backups
/usr/local/bin/backup-email-sender.sh
```

### Monitoring
```bash
# View logs
sudo journalctl -u email-sender -f

# Check nginx logs
sudo tail -f /var/log/nginx/smtp.truongvinhkhuong.io.vn.access.log
```

## 🐛 Troubleshooting

### Common Issues
1. **Service won't start**
   ```bash
   sudo journalctl -u email-sender -n 50
   ```

2. **Nginx 502 error**
   ```bash
   sudo systemctl status email-sender
   sudo tail -f /var/log/nginx/error.log
   ```

3. **Email sending fails**
   ```bash
   tail -f app.log
   python3 test_app.py
   ```

4. **SSL certificate issues**
   ```bash
   sudo certbot certificates
   sudo certbot renew
   ```

## 📞 Support

### Getting Help
1. Check the logs first
2. Run the test script
3. Review this documentation
4. Check the deployment guide

### Useful Commands
```bash
# Service management
sudo systemctl start|stop|restart|status email-sender

# Log viewing
sudo journalctl -u email-sender -f
tail -f app.log

# Health checks
curl https://smtp.truongvinhkhuong.io.vn/health
python3 test_app.py
```

## 🎯 Key URLs

- **Application**: https://smtp.truongvinhkhuong.io.vn
- **Health Check**: https://smtp.truongvinhkhuong.io.vn/health
- **Status API**: https://smtp.truongvinhkhuong.io.vn/status
- **Logs API**: https://smtp.truongvinhkhuong.io.vn/logs

---

**🎉 Ready to send emails to your hackathon participants!**