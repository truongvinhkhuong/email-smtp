#!/usr/bin/env python3
"""
Hệ thống gửi email hàng loạt cho NAVER Vietnam AI Hackathon
Sử dụng Python built-in libraries: smtplib, email, csv, json, time, logging
"""

import smtplib
import csv
import json
import time
import logging
import re
import os
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Tuple, Optional
from config import (
    SMTP_CONFIG, EMAIL_CONFIG, EMAIL_HTML_TEMPLATE, 
    EMAIL_TEXT_TEMPLATE, EMAIL_REGEX, TEST_MODE
)


class EmailSender:
    """Class chính để gửi email hàng loạt"""
    
    def __init__(self, smtp_provider: str = 'gmail'):
        """
        Khởi tạo EmailSender
        
        Args:
            smtp_provider: 'gmail', 'outlook', hoặc 'yahoo'
        """
        self.smtp_config = SMTP_CONFIG.get(smtp_provider, SMTP_CONFIG['gmail'])
        self.email_config = EMAIL_CONFIG
        self.smtp_server = None
        self.session = None
        
        # Thiết lập logging
        self._setup_logging()
        
        # Validate cấu hình
        self._validate_config()
        
        # Load checkpoint nếu có
        self.checkpoint = self._load_checkpoint()
        
    def _setup_logging(self):
        """Thiết lập logging system"""
        # Tạo logger chính
        self.logger = logging.getLogger('email_sender')
        self.logger.setLevel(logging.INFO)
        
        # Xóa handlers cũ nếu có
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler cho log chính
        file_handler = logging.FileHandler(
            self.email_config['log_file'], 
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
        
        # File handler cho error log
        error_handler = logging.FileHandler(
            self.email_config['error_log_file'], 
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_format)
        self.logger.addHandler(error_handler)
        
    def _validate_config(self):
        """Validate cấu hình email"""
        if not self.email_config['sender_email']:
            raise ValueError("SENDER_EMAIL environment variable is required")
        if not self.email_config['sender_password']:
            raise ValueError("SENDER_PASSWORD environment variable is required")
            
        # Validate email format
        if not re.match(EMAIL_REGEX, self.email_config['sender_email']):
            raise ValueError("Invalid sender email format")
            
    def _load_checkpoint(self) -> Dict:
        """Load checkpoint từ file"""
        checkpoint_file = self.email_config['checkpoint_file']
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load checkpoint: {e}")
        return {
            'last_sent_index': -1,
            'total_sent': 0,
            'total_failed': 0,
            'start_time': None
        }
        
    def _save_checkpoint(self):
        """Lưu checkpoint vào file"""
        checkpoint_file = self.email_config['checkpoint_file']
        try:
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(self.checkpoint, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save checkpoint: {e}")
            
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        # Strip whitespace before validation
        email = email.strip()
        return bool(re.match(EMAIL_REGEX, email))
        
    def _create_email_content(self, name: str = '') -> Tuple[str, str]:
        """
        Tạo nội dung email HTML và text
        
        Args:
            name: Tên người nhận (optional)
            
        Returns:
            Tuple (html_content, text_content)
        """
        # Sử dụng tên hoặc "Participant" nếu không có tên
        display_name = name.strip() if name and name.strip() else 'Participant'
        
        # Template variables
        template_vars = {
            'name': display_name,
            'deadline': self.email_config['deadline'],
            'github_classroom_link': self.email_config['github_classroom_link'],
            'support_email': self.email_config['support_email'],
            'discord_link': self.email_config['discord_link']
        }
        
        # Tạo HTML content
        html_content = EMAIL_HTML_TEMPLATE.format(**template_vars)
        
        # Tạo text content
        text_content = EMAIL_TEXT_TEMPLATE.format(**template_vars)
        
        return html_content, text_content
        
    def _create_email_message(self, to_email: str, name: str = '') -> MIMEMultipart:
        """
        Tạo email message
        
        Args:
            to_email: Email người nhận
            name: Tên người nhận
            
        Returns:
            MIMEMultipart message
        """
        # Tạo message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.email_config['sender_name']} <{self.email_config['sender_email']}>"
        msg['To'] = to_email
        msg['Subject'] = self.email_config['subject']
        
        # Tạo nội dung email
        html_content, text_content = self._create_email_content(name)
        
        # Attach text và HTML
        text_part = MIMEText(text_content, 'plain', 'utf-8')
        html_part = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        return msg
        
    def _connect_smtp(self) -> bool:
        """
        Kết nối đến SMTP server
        
        Returns:
            True nếu kết nối thành công
        """
        try:
            self.smtp_server = smtplib.SMTP(
                self.smtp_config['server'], 
                self.smtp_config['port']
            )
            
            # Enable debug mode (optional)
            # self.smtp_server.set_debuglevel(1)
            
            # Start TLS if required
            if self.smtp_config['use_tls']:
                self.smtp_server.starttls()
                
            # Login
            self.smtp_server.login(
                self.email_config['sender_email'],
                self.email_config['sender_password']
            )
            
            self.logger.info("Successfully connected to SMTP server")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to SMTP server: {e}")
            return False
            
    def _disconnect_smtp(self):
        """Ngắt kết nối SMTP"""
        if self.smtp_server:
            try:
                self.smtp_server.quit()
                self.logger.info("Disconnected from SMTP server")
            except Exception as e:
                self.logger.warning(f"Error disconnecting from SMTP: {e}")
            finally:
                self.smtp_server = None
                
    def _send_single_email(self, to_email: str, name: str = '') -> bool:
        """
        Gửi một email
        
        Args:
            to_email: Email người nhận
            name: Tên người nhận
            
        Returns:
            True nếu gửi thành công
        """
        try:
            # Strip whitespace from email and name
            to_email = to_email.strip()
            name = name.strip()
            
            # Validate email
            if not self._validate_email(to_email):
                self.logger.error(f"Invalid email format: {to_email}")
                return False
                
            # Tạo message
            msg = self._create_email_message(to_email, name)
            
            # Gửi email
            self.smtp_server.send_message(msg)
            
            self.logger.info(f"Email sent successfully to: {to_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {to_email}: {e}")
            return False
            
    def _load_participants(self) -> List[Dict[str, str]]:
        """
        Load danh sách participants từ CSV file
        
        Returns:
            List of participant dictionaries
        """
        participants = []
        csv_file = self.email_config['participants_file']
        
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Participants file not found: {csv_file}")
            
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Strip whitespace from all fields
                    cleaned_row = {key: value.strip() if value else value for key, value in row.items()}
                    
                    # Validate required fields
                    if 'identifier' not in cleaned_row or not cleaned_row['identifier']:
                        self.logger.warning(f"Invalid row (missing identifier): {cleaned_row}")
                        continue
                        
                    participants.append({
                        'email': cleaned_row['identifier'],
                        'name': cleaned_row.get('name', '')
                    })
                    
            self.logger.info(f"Loaded {len(participants)} participants from CSV")
            return participants
            
        except Exception as e:
            self.logger.error(f"Error loading participants: {e}")
            raise
            
    def send_emails(self, test_mode: bool = False) -> Dict[str, int]:
        """
        Gửi email hàng loạt
        
        Args:
            test_mode: Nếu True, chỉ gửi 5 email đầu tiên
            
        Returns:
            Dictionary với thống kê gửi email
        """
        # Load participants
        try:
            participants = self._load_participants()
        except Exception as e:
            self.logger.error(f"Cannot load participants: {e}")
            return {'sent': 0, 'failed': 0, 'total': 0}
            
        # Test mode: chỉ gửi 5 email đầu tiên
        if test_mode or TEST_MODE['enabled']:
            participants = participants[:TEST_MODE['test_emails_count']]
            self.logger.info(f"TEST MODE: Sending to first {len(participants)} participants only")
            
        total_participants = len(participants)
        batch_size = self.email_config['batch_size']
        delay_between_batches = self.email_config['delay_between_batches']
        delay_between_emails = self.email_config['delay_between_emails']
        
        # Resume từ checkpoint nếu có
        start_index = self.checkpoint['last_sent_index'] + 1
        if start_index > 0:
            self.logger.info(f"Resuming from index {start_index}")
            
        # Khởi tạo thống kê
        stats = {
            'sent': self.checkpoint['total_sent'],
            'failed': self.checkpoint['total_failed'],
            'total': total_participants
        }
        
        # Bắt đầu gửi email
        self.checkpoint['start_time'] = datetime.now().isoformat()
        self.logger.info(f"Starting to send emails to {total_participants} participants")
        self.logger.info(f"Batch size: {batch_size}, Delay between batches: {delay_between_batches}s")
        
        try:
            # Kết nối SMTP
            if not self._connect_smtp():
                self.logger.error("Cannot connect to SMTP server. Aborting.")
                return stats
                
            # Gửi email theo batch
            for batch_start in range(start_index, total_participants, batch_size):
                batch_end = min(batch_start + batch_size, total_participants)
                batch_participants = participants[batch_start:batch_end]
                
                self.logger.info(f"Processing batch {batch_start//batch_size + 1}: "
                               f"emails {batch_start + 1}-{batch_end}")
                
                # Gửi email trong batch
                for i, participant in enumerate(batch_participants):
                    email = participant['email']
                    name = participant['name']
                    current_index = batch_start + i
                    
                    # Gửi email
                    success = self._send_single_email(email, name)
                    
                    if success:
                        stats['sent'] += 1
                        self.checkpoint['total_sent'] += 1
                    else:
                        stats['failed'] += 1
                        self.checkpoint['total_failed'] += 1
                        
                    # Cập nhật checkpoint
                    self.checkpoint['last_sent_index'] = current_index
                    self._save_checkpoint()
                    
                    # Delay giữa các email trong batch
                    if i < len(batch_participants) - 1:
                        time.sleep(delay_between_emails)
                        
                # Delay giữa các batch (trừ batch cuối)
                if batch_end < total_participants:
                    self.logger.info(f"Waiting {delay_between_batches} seconds before next batch...")
                    time.sleep(delay_between_batches)
                    
        except KeyboardInterrupt:
            self.logger.info("Email sending interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error during email sending: {e}")
        finally:
            # Ngắt kết nối SMTP
            self._disconnect_smtp()
            
        # Log kết quả cuối cùng
        self.logger.info(f"Email sending completed!")
        self.logger.info(f"Total sent: {stats['sent']}")
        self.logger.info(f"Total failed: {stats['failed']}")
        self.logger.info(f"Success rate: {stats['sent']/(stats['sent']+stats['failed'])*100:.1f}%")
        
        return stats


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Send bulk emails for NAVER Vietnam AI Hackathon')
    parser.add_argument('--provider', choices=['gmail', 'outlook', 'yahoo'], 
                       default='gmail', help='SMTP provider to use')
    parser.add_argument('--test', action='store_true', 
                       help='Test mode: send to first 5 participants only')
    parser.add_argument('--reset', action='store_true', 
                       help='Reset checkpoint and start from beginning')
    
    args = parser.parse_args()
    
    # Reset checkpoint nếu được yêu cầu
    if args.reset:
        checkpoint_file = EMAIL_CONFIG['checkpoint_file']
        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)
            print("Checkpoint reset successfully")
    
    # Kiểm tra environment variables
    if not os.getenv('SENDER_EMAIL'):
        print("ERROR: SENDER_EMAIL environment variable is required")
        print("Please set it with: export SENDER_EMAIL='your-email@gmail.com'")
        sys.exit(1)
        
    if not os.getenv('SENDER_PASSWORD'):
        print("ERROR: SENDER_PASSWORD environment variable is required")
        print("Please set it with: export SENDER_PASSWORD='your-app-password'")
        sys.exit(1)
    
    # Tạo và chạy EmailSender
    try:
        sender = EmailSender(smtp_provider=args.provider)
        stats = sender.send_emails(test_mode=args.test)
        
        print(f"\n=== FINAL STATISTICS ===")
        print(f"Total participants: {stats['total']}")
        print(f"Emails sent successfully: {stats['sent']}")
        print(f"Emails failed: {stats['failed']}")
        print(f"Success rate: {stats['sent']/(stats['sent']+stats['failed'])*100:.1f}%")
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
