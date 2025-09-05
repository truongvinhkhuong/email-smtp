#!/usr/bin/env python3
"""
Test script để kiểm tra kết nối Outlook
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_CONFIG

def test_outlook_connection():
    """Test kết nối đến Outlook SMTP server"""
    
    # Lấy thông tin từ environment variables
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not sender_email or not sender_password:
        print("ERROR: Cần set SENDER_EMAIL và SENDER_PASSWORD environment variables")
        print("Ví dụ:")
        print("export SENDER_EMAIL='your-email@outlook.com'")
        print("export SENDER_PASSWORD='your-app-password'")
        return False
    
    print(f"Testing Outlook connection...")
    print(f"Email: {sender_email}")
    print(f"Password: {'*' * len(sender_password)}")
    
    # Lấy cấu hình Outlook
    outlook_config = SMTP_CONFIG['outlook']
    
    try:
        # Kết nối đến SMTP server
        print(f"Connecting to {outlook_config['server']}:{outlook_config['port']}...")
        server = smtplib.SMTP(outlook_config['server'], outlook_config['port'])
        
        # Enable debug mode để xem chi tiết
        server.set_debuglevel(1)
        
        # Start TLS
        print("Starting TLS...")
        server.starttls()
        
        # Login
        print("Logging in...")
        server.login(sender_email, sender_password)
        
        print("SUCCESS: Kết nối Outlook thành công!")
        
        # Test gửi email đơn giản
        test_email = input("\nNhập email để test gửi (hoặc Enter để skip): ").strip()
        
        if test_email:
            print(f"Sending test email to {test_email}...")
            
            # Tạo message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = test_email
            msg['Subject'] = "Test Email từ Python Script"
            
            body = """
            Đây là email test từ Python script.
            
            Nếu bạn nhận được email này, có nghĩa là cấu hình Outlook đã hoạt động!
            
            Best regards,
            Python Email Script
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Gửi email
            server.send_message(msg)
            print("Test email sent successfully!")
        
        # Đóng kết nối
        server.quit()
        print("Disconnected from Outlook server")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"AUTHENTICATION ERROR: {e}")
        print("\n🔧 HƯỚNG DẪN KHẮC PHỤC:")
        print("1. Kiểm tra email có đúng không")
        print("2. Tạo App Password mới:")
        print("   - Đăng nhập outlook.com")
        print("   - Settings → Security → Advanced security options")
        print("   - Bật Two-step verification")
        print("   - Tạo App Password cho 'Mail'")
        print("   - Sử dụng App Password (16 ký tự) thay vì password thường")
        print("3. Cập nhật environment variables:")
        print("   export SENDER_EMAIL='your-email@outlook.com'")
        print("   export SENDER_PASSWORD='your-app-password'")
        print("4. Chạy lại script: python3 test_outlook.py")
        return False
        
    except smtplib.SMTPException as e:
        print(f"SMTP ERROR: {e}")
        return False
        
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        return False

def main():
    """Main function"""
    print("=" * 50)
    print("OUTLOOK CONNECTION TEST")
    print("=" * 50)
    
    success = test_outlook_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("TEST PASSED: Outlook đã sẵn sàng để gửi email!")
        print("Bây giờ bạn có thể chạy: python send_emails.py --provider outlook")
    else:
        print("TEST FAILED: Cần kiểm tra lại cấu hình")
    print("=" * 50)

if __name__ == '__main__':
    main()
