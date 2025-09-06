# Quick Start Guide - Docker Deployment

## 🚀 Deploy trong 3 bước

### 1. Cấu hình
```bash
# Copy file cấu hình
cp env.example .env

# Chỉnh sửa credentials
nano .env
```

**Chỉnh sửa file `.env`:**
```env
SENDER_EMAIL=your-email@naver.com
SENDER_PASSWORD=your-app-password
```

### 2. Deploy
```bash
# Cách 1: Sử dụng script
./docker-deploy.sh

# Cách 2: Sử dụng Make
make deploy

# Cách 3: Docker Compose trực tiếp
docker-compose up --build -d
```

### 3. Kiểm tra
```bash
# Mở trình duyệt
open http://localhost:5005

# Hoặc kiểm tra health
curl http://localhost:5005/health
```

## 📋 Commands hữu ích

```bash
# Xem logs
make logs
# hoặc
docker-compose logs -f

# Dừng ứng dụng
make down
# hoặc
docker-compose down

# Khởi động lại
make restart

# Xem trạng thái
make status

# Dọn dẹp
make clean
```

## 🔧 Production Deployment

```bash
# Deploy production mode
make deploy-prod
# hoặc
./docker-deploy.sh deploy-prod
```

## ❗ Troubleshooting

### Container không start
```bash
# Xem logs chi tiết
docker-compose logs email-sender

# Rebuild
docker-compose up --build -d
```

### Lỗi email
- Kiểm tra credentials trong `.env`
- Kiểm tra network connectivity
- Xem logs để debug

### Port đã được sử dụng
```bash
# Thay đổi port trong docker-compose.yml
ports:
  - "5006:5005"  # Sử dụng port 5006
```

## 📞 Support

Nếu gặp vấn đề, hãy check:
1. `docker-compose logs email-sender`
2. `docker-compose ps`
3. File `.env` có đúng không
4. Port 5005 có bị chiếm không
