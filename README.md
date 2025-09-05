## Feature

- **Gửi email hàng loạt** với khả năng xử lý 2000+ người tham gia
- **Batch processing** - Chia nhỏ thành các batch 100 email/lần để tránh giới hạn server
- **Rate limiting** - Tự động chờ 5 phút giữa các batch
- **Checkpoint system** - Có thể resume từ email cuối cùng thành công
- **Test mode** - Chế độ test chỉ gửi 5 email đầu tiên
- **Logging đầy đủ** - Theo dõi tiến độ và lỗi chi tiết
- **Email template đẹp** - HTML + Text với thiết kế chuyên nghiệp
- **Bảo mật** - Sử dụng environment variables cho thông tin nhạy cảm

## Structure

```
mail-test/
├── send_emails.py      # File chính chứa logic gửi email
├── config.py           # Cấu hình SMTP, template email, và các hằng số
├── participants.csv    # Danh sách người tham gia (email + tên)
├── README.md          # Hướng dẫn sử dụng
├── requirements.txt   # Dependencies (chỉ Python built-in libraries)
├── log.txt            # Log chính (tự động tạo)
├── error_log.txt      # Log lỗi (tự động tạo)
└── checkpoint.txt     # Checkpoint để resume (tự động tạo)
```

### 2. Config Environment Variables

```bash

export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-16-char-app-password"


echo "SENDER_EMAIL=your-email@gmail.com" > .env
echo "SENDER_PASSWORD=your-16-char-app-password" >> .env
```

## Run

### Basic

```bash
# Gửi email thật (tất cả participants)
python send_emails.py

# Test mode (chỉ gửi 5 email đầu tiên)
python send_emails.py --test

# Sử dụng Outlook thay vì Gmail
python send_emails.py --provider outlook

# Reset checkpoint và bắt đầu lại từ đầu
python send_emails.py --reset
```

### Command line

```bash
python send_emails.py [OPTIONS]

Options:
  --provider {gmail,outlook,yahoo}  SMTP provider (default: gmail)
  --test                           Test mode: chỉ gửi 5 email đầu tiên
  --reset                          Reset checkpoint và bắt đầu lại
  -h, --help                       Hiển thị help
```

