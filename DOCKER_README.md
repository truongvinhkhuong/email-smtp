# Docker Deployment Guide - NAVER Vietnam AI Hackathon Email Sender

## Tổng quan

Dự án này đã được containerized để deploy dễ dàng hơn với Docker Compose. Không cần cài đặt Python hay dependencies trên server.

## Yêu cầu hệ thống

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- 2GB RAM tối thiểu
- 1GB disk space

## Cài đặt nhanh

### 1. Clone repository
```bash
git clone <your-repo-url>
cd mail-test
```

### 2. Cấu hình environment
```bash
# Copy file cấu hình mẫu
cp env.example .env

# Chỉnh sửa file .env với thông tin thực tế
nano .env
```

**Các biến môi trường cần thiết:**
```env
SENDER_EMAIL=your-email@naver.com
SENDER_PASSWORD=your-app-password
```

### 3. Deploy ứng dụng
```bash
# Cách 1: Sử dụng script tự động
./docker-deploy.sh

# Cách 2: Sử dụng Docker Compose trực tiếp
docker-compose up --build -d
```

### 4. Kiểm tra ứng dụng
```bash
# Xem trạng thái containers
docker-compose ps

# Xem logs
docker-compose logs -f email-sender

# Kiểm tra health
curl http://localhost:5005/health
```

## Quản lý ứng dụng

### Scripts có sẵn
```bash
# Deploy ứng dụng
./docker-deploy.sh deploy

# Dừng ứng dụng
./docker-deploy.sh stop

# Khởi động lại
./docker-deploy.sh restart

# Xem logs
./docker-deploy.sh logs

# Xem trạng thái
./docker-deploy.sh status

# Dọn dẹp (xóa containers và images)
./docker-deploy.sh cleanup
```

### Docker Compose commands
```bash
# Khởi động
docker-compose up -d

# Dừng
docker-compose down

# Xem logs
docker-compose logs -f

# Rebuild và khởi động
docker-compose up --build -d

# Restart service
docker-compose restart email-sender
```

## Cấu trúc Docker

### Dockerfile
- Base image: Python 3.11-slim
- Non-root user cho security
- Health check tự động
- Optimized cho production

### Docker Compose
- Service: `email-sender`
- Port: 5005
- Volume mounts cho logs và static files
- Environment variables từ .env file
- Health check configuration

## Monitoring và Logs

### Logs
```bash
# Xem logs real-time
docker-compose logs -f email-sender

# Xem logs của tất cả services
docker-compose logs

# Xem logs với timestamp
docker-compose logs -t email-sender
```

### Health Check
- URL: `http://localhost:5005/health`
- Interval: 30s
- Timeout: 10s
- Retries: 3

### Monitoring
```bash
# Xem resource usage
docker stats

# Xem container details
docker inspect naver-email-sender

# Xem processes trong container
docker exec naver-email-sender ps aux
```

## Troubleshooting

### Container không start
```bash
# Xem logs chi tiết
docker-compose logs email-sender

# Check environment variables
docker-compose config

# Rebuild từ đầu
docker-compose down
docker-compose up --build -d
```

### Lỗi kết nối email
1. Kiểm tra credentials trong .env
2. Kiểm tra network connectivity
3. Xem logs để debug SMTP errors

### Performance issues
```bash
# Xem resource usage
docker stats naver-email-sender

# Scale workers (nếu cần)
# Chỉnh sửa gunicorn.conf.py
```

## Production Deployment

### 1. Cấu hình Nginx (tùy chọn)
Vì server đã có Nginx, bạn có thể cấu hình reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. SSL/HTTPS
Cấu hình SSL certificate trong Nginx để bảo mật ứng dụng.

### 3. Firewall
```bash
# Mở port 5005 (nếu cần)
sudo ufw allow 5005
```

### 4. Auto-start
```bash
# Tạo systemd service
sudo nano /etc/systemd/system/naver-email-sender.service
```

## Backup và Recovery

### Backup
```bash
# Backup volumes
docker run --rm -v naver-email-sender_logs:/data -v $(pwd):/backup alpine tar czf /backup/logs-backup.tar.gz -C /data .
```

### Recovery
```bash
# Restore từ backup
docker run --rm -v naver-email-sender_logs:/data -v $(pwd):/backup alpine tar xzf /backup/logs-backup.tar.gz -C /data
```

## Security Notes

1. **Credentials**: Luôn sử dụng environment variables, không hardcode
2. **Non-root user**: Container chạy với user `app` (non-root)
3. **Network**: Chỉ expose port cần thiết
4. **Updates**: Thường xuyên update base images
5. **Logs**: Monitor logs để phát hiện issues

## Support

Nếu gặp vấn đề, hãy:
1. Check logs: `docker-compose logs email-sender`
2. Check status: `docker-compose ps`
3. Verify config: `docker-compose config`
4. Contact team support
