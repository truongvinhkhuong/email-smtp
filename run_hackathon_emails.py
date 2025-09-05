#!/usr/bin/env python3
"""
Script chính để chạy toàn bộ quy trình gửi email cho NAVER Vietnam AI Hackathon
Bao gồm: test cấu hình, tạo dữ liệu test, và gửi email
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """Chạy command và trả về True nếu thành công"""
    print(f"\n {description}...")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"{description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def check_environment():
    """Kiểm tra environment variables"""
    print("Checking environment variables...")
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not sender_email:
        print("SENDER_EMAIL not set")
        print("   Please run: export SENDER_EMAIL='your-email@gmail.com'")
        return False
        
    if not sender_password:
        print("SENDER_PASSWORD not set")
        print("   Please run: export SENDER_PASSWORD='your-app-password'")
        return False
        
    print(f"SENDER_EMAIL: {sender_email}")
    print(f"SENDER_PASSWORD: {'*' * len(sender_password)}")
    return True

def check_files():
    """Kiểm tra các file cần thiết"""
    print("\nChecking required files...")
    
    required_files = [
        'send_emails.py',
        'config.py',
        'participants.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"{file}")
    
    if missing_files:
        print(f"Missing files: {', '.join(missing_files)}")
        return False
        
    return True

def main():
    """Main function"""
    print("NAVER Vietnam AI Hackathon - Email Sender")
    print("=" * 60)
    
    # Kiểm tra environment
    if not check_environment():
        print("\nEnvironment setup incomplete. Please fix the issues above.")
        sys.exit(1)
    
    # Kiểm tra files
    if not check_files():
        print("\nRequired files missing. Please check the project structure.")
        sys.exit(1)
    
    # Menu chính
    while True:
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("1. Test email configuration")
        print("2. Generate test data (2000 participants)")
        print("3. Send test emails (5 emails only)")
        print("4. Send all emails (production)")
        print("5. Reset checkpoint and start over")
        print("6. View current statistics")
        print("7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            # Test configuration
            if run_command("python test_email.py", "Testing email configuration"):
                print("Configuration test passed!")
            else:
                print("Configuration test failed. Please check your settings.")
                
        elif choice == '2':
            # Generate test data
            if run_command("python generate_test_data.py", "Generating test data"):
                print("Test data generated successfully!")
            else:
                print("Failed to generate test data.")
                
        elif choice == '3':
            # Send test emails
            confirm = input("This will send 5 test emails. Continue? (y/N): ").strip().lower()
            if confirm == 'y':
                if run_command("python send_emails.py --test", "Sending test emails"):
                    print("Test emails sent successfully!")
                else:
                    print("Failed to send test emails.")
            else:
                print("Test email sending cancelled.")
                
        elif choice == '4':
            # Send all emails
            print("WARNING: This will send emails to ALL participants!")
            print("   Make sure you have:")
            print("   - Tested with option 3 first")
            print("   - Updated participants.csv with real data")
            print("   - Verified your email configuration")
            
            confirm = input("\nProceed with sending ALL emails? (y/N): ").strip().lower()
            if confirm == 'y':
                if run_command("python send_emails.py", "Sending all emails"):
                    print("All emails sent successfully!")
                else:
                    print("Some emails failed. Check log files for details.")
            else:
                print("Email sending cancelled.")
                
        elif choice == '5':
            # Reset checkpoint
            confirm = input("This will reset progress and start over. Continue? (y/N): ").strip().lower()
            if confirm == 'y':
                if run_command("python send_emails.py --reset", "Resetting checkpoint"):
                    print("Checkpoint reset successfully!")
                else:
                    print("Failed to reset checkpoint.")
            else:
                print("Checkpoint reset cancelled.")
                
        elif choice == '6':
            # View statistics
            print("\nCurrent Statistics:")
            print("-" * 40)
            
            # Check if checkpoint exists
            if Path('checkpoint.txt').exists():
                try:
                    import json
                    with open('checkpoint.txt', 'r') as f:
                        checkpoint = json.load(f)
                    
                    print(f"Total sent: {checkpoint.get('total_sent', 0)}")
                    print(f"Total failed: {checkpoint.get('total_failed', 0)}")
                    print(f"Last sent index: {checkpoint.get('last_sent_index', -1)}")
                    
                    if checkpoint.get('start_time'):
                        print(f"Started at: {checkpoint['start_time']}")
                        
                except Exception as e:
                    print(f"Error reading checkpoint: {e}")
            else:
                print("No checkpoint found. No emails sent yet.")
                
        elif choice == '7':
            # Exit
            print("\nGoodbye! Good luck with the hackathon!")
            break
            
        else:
            print("Invalid option. Please select 1-7.")

if __name__ == '__main__':
    main()
