#!/usr/bin/env python3
"""
Test script để kiểm tra cấu hình email trước khi gửi hàng loạt
"""

import os
import sys
from send_emails import EmailSender

def test_email_configuration():
    """Test cấu hình email cơ bản"""
    print("Testing email configuration...")
    
    # Kiểm tra environment variables
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not sender_email:
        print("ERROR: SENDER_EMAIL environment variable not set")
        print("   Please run: export SENDER_EMAIL='your-email@gmail.com'")
        return False
        
    if not sender_password:
        print("ERROR: SENDER_PASSWORD environment variable not set")
        print("   Please run: export SENDER_PASSWORD='your-app-password'")
        return False
        
    print(f"SENDER_EMAIL: {sender_email}")
    print(f"SENDER_PASSWORD: {'*' * len(sender_password)}")
    
    # Test SMTP connection
    try:
        sender = EmailSender()
        print("EmailSender initialized successfully")
        
        # Test SMTP connection
        if sender._connect_smtp():
            print("SMTP connection successful")
            sender._disconnect_smtp()
            return True
        else:
            print("SMTP connection failed")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_csv_loading():
    """Test loading CSV file"""
    print("\nTesting CSV file loading...")
    
    try:
        sender = EmailSender()
        participants = sender._load_participants()
        
        print(f"Loaded {len(participants)} participants from CSV")
        
        # Show first few participants
        print("First 3 participants:")
        for i, p in enumerate(participants[:3]):
            print(f"   {i+1}. {p['email']} - {p['name']}")
            
        return True
        
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return False

def test_email_creation():
    """Test email message creation"""
    print("\nTesting email message creation...")
    
    try:
        sender = EmailSender()
        
        # Test HTML and text content creation
        html_content, text_content = sender._create_email_content("Test User")
        
        print("Email content created successfully")
        print(f"   HTML length: {len(html_content)} characters")
        print(f"   Text length: {len(text_content)} characters")
        
        # Test email message creation
        msg = sender._create_email_message("test@example.com", "Test User")
        
        print("Email message created successfully")
        print(f"   Subject: {msg['Subject']}")
        print(f"   From: {msg['From']}")
        print(f"   To: {msg['To']}")
        
        return True
        
    except Exception as e:
        print(f"Error creating email: {e}")
        return False

def main():
    """Main test function"""
    print("NAVER Vietnam AI Hackathon - Email Configuration Test")
    print("=" * 60)
    
    tests = [
        ("Email Configuration", test_email_configuration),
        ("CSV Loading", test_csv_loading),
        ("Email Creation", test_email_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        if test_func():
            passed += 1
            print(f"{test_name}: PASSED")
        else:
            print(f"{test_name}: FAILED")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! You're ready to send emails.")
        print("\nNext steps:")
        print("1. Update participants.csv with real data")
        print("2. Run: python send_emails.py --test")
        print("3. If test successful, run: python send_emails.py")
    else:
        print("Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
