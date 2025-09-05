#!/usr/bin/env python3
"""
Script helper để setup Outlook configuration
"""

import os
import getpass

def setup_outlook_config():
    """Setup Outlook configuration interactively"""
    
    print("=" * 60)
    print("🔧 OUTLOOK CONFIGURATION SETUP")
    print("=" * 60)
    
    print("\n📧 Nhập thông tin Outlook của bạn:")
    
    # Lấy email
    email = input("Email address: ").strip()
    if not email:
        print("❌ Email không được để trống!")
        return False
    
    # Lấy password
    print("\n🔐 Nhập App Password (16 ký tự):")
    print("   (Nếu chưa có, hãy tạo tại: outlook.com → Security → App passwords)")
    password = getpass.getpass("App Password: ").strip()
    
    if not password:
        print("❌ App Password không được để trống!")
        return False
    
    if len(password) != 16:
        print("⚠️  App Password phải có đúng 16 ký tự!")
        print("   Hãy kiểm tra lại App Password tại outlook.com")
        return False
    
    # Tạo file .env
    env_content = f"""# Outlook Configuration
SENDER_EMAIL={email}
SENDER_PASSWORD={password}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ Đã lưu cấu hình vào file .env")
        print(f"📧 Email: {email}")
        print(f"🔐 Password: {'*' * len(password)}")
        
        # Hướng dẫn load environment
        print("\n📋 Để sử dụng cấu hình này:")
        print("1. Load environment variables:")
        print("   source .env")
        print("2. Hoặc chạy trực tiếp:")
        print("   python3 test_outlook.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu file .env: {e}")
        return False

def load_env_file():
    """Load environment variables from .env file"""
    try:
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
            return True
    except Exception as e:
        print(f"⚠️  Không thể load file .env: {e}")
    return False

def main():
    """Main function"""
    print("Chọn một trong các tùy chọn:")
    print("1. Setup cấu hình mới")
    print("2. Test cấu hình hiện tại")
    print("3. Load từ file .env và test")
    
    choice = input("\nNhập lựa chọn (1-3): ").strip()
    
    if choice == '1':
        setup_outlook_config()
    elif choice == '2':
        # Test với environment variables hiện tại
        os.system('python3 test_outlook.py')
    elif choice == '3':
        # Load từ .env và test
        if load_env_file():
            print("✅ Đã load cấu hình từ .env")
            os.system('python3 test_outlook.py')
        else:
            print("❌ Không tìm thấy file .env")
    else:
        print("❌ Lựa chọn không hợp lệ!")

if __name__ == '__main__':
    main()
