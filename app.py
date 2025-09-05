#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NAVER Vietnam AI Hackathon - Email Sender Web Application
Flask web application để gửi email hàng loạt với UI
"""

import os
import csv
import json
import time
import smtplib
import logging
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import re
from io import StringIO

from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config import (
    SMTP_CONFIG, EMAIL_CONFIG, EMAIL_HTML_TEMPLATE, 
    EMAIL_TEXT_TEMPLATE, EMAIL_REGEX, TEST_MODE
)

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global variables for email sending status
email_status = {
    'is_running': False,
    'total_emails': 0,
    'sent_emails': 0,
    'failed_emails': 0,
    'current_batch': 0,
    'total_batches': 0,
    'start_time': None,
    'end_time': None,
    'logs': [],
    'errors': []
}

# Email sending thread
email_thread = None


class EmailSender:
    """Class để gửi email hàng loạt"""
    
    def __init__(self):
        self.smtp_config = SMTP_CONFIG['gmail']
        self.email_config = EMAIL_CONFIG.copy()
        self.email_config['sender_email'] = 'khuonggg2924@gmail.com'
        self.email_config['sender_password'] = 'oboxhjcfxkzqnpug'
        
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        return re.match(EMAIL_REGEX, email) is not None
    
    def create_email_message(self, recipient_name: str, recipient_email: str) -> MIMEMultipart:
        """Tạo email message"""
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.email_config['sender_name']} <{self.email_config['sender_email']}>"
        msg['To'] = recipient_email
        msg['Subject'] = self.email_config['subject']
        
        # Create HTML and text versions
        html_content = EMAIL_HTML_TEMPLATE.format(
            name=recipient_name,
            deadline=self.email_config['deadline'],
            github_classroom_link=self.email_config['github_classroom_link'],
            support_email=self.email_config['support_email'],
            discord_link=self.email_config['discord_link']
        )
        
        text_content = EMAIL_TEXT_TEMPLATE.format(
            name=recipient_name,
            deadline=self.email_config['deadline'],
            github_classroom_link=self.email_config['github_classroom_link'],
            support_email=self.email_config['support_email'],
            discord_link=self.email_config['discord_link']
        )
        
        # Attach parts
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        return msg
    
    def send_email(self, recipient_name: str, recipient_email: str) -> bool:
        """Gửi email đến một người nhận"""
        try:
            # Validate email
            if not self.validate_email(recipient_email):
                logger.error(f"Invalid email format: {recipient_email}")
                return False
            
            # Create message
            msg = self.create_email_message(recipient_name, recipient_email)
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                
                # Send email
                server.send_message(msg)
                logger.info(f"Email sent successfully to {recipient_name} ({recipient_email})")
                return True
                
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_name} ({recipient_email}): {str(e)}")
            return False

def send_emails_batch(participants_data: List[Dict[str, str]]):
    """Gửi email hàng loạt trong background thread"""
    global email_status, email_thread
    
    try:
        email_status['is_running'] = True
        email_status['start_time'] = datetime.now().isoformat()
        email_status['total_emails'] = len(participants_data)
        email_status['sent_emails'] = 0
        email_status['failed_emails'] = 0
        email_status['logs'] = []
        email_status['errors'] = []
        
        # Calculate batches
        batch_size = int(EMAIL_CONFIG.get('batch_size', 100))
        email_status['total_batches'] = (len(participants_data) + batch_size - 1) // batch_size
        
        sender = EmailSender()
        
        # Process in batches
        for batch_idx in range(email_status['total_batches']):
            if not email_status['is_running']:  # Check if stopped
                break
                
            email_status['current_batch'] = batch_idx + 1
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(participants_data))
            batch_data = participants_data[start_idx:end_idx]
            
            # Send emails in current batch
            for participant in batch_data:
                if not email_status['is_running']:  # Check if stopped
                    break
                    
                name = participant.get('name', '')
                email = participant.get('identifier', '')
                
                if sender.send_email(name, email):
                    email_status['sent_emails'] += 1
                    email_status['logs'].append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'success',
                        'message': f"Email sent to {name} ({email})"
                    })
                else:
                    email_status['failed_emails'] += 1
                    email_status['errors'].append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'error',
                        'message': f"Failed to send email to {name} ({email})"
                    })
                
                # Delay between emails
                time.sleep(float(EMAIL_CONFIG.get('delay_between_emails', 1)))
            
            # Delay between batches
            if batch_idx < email_status['total_batches'] - 1:
                time.sleep(float(EMAIL_CONFIG.get('delay_between_batches', 300)))
        
        email_status['end_time'] = datetime.now().isoformat()
        email_status['is_running'] = False
        
    except Exception as e:
        logger.error(f"Error in email sending process: {str(e)}")
        email_status['errors'].append({
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'message': f"Email sending process error: {str(e)}"
        })
        email_status['is_running'] = False


@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html', 
                         email_status=email_status,
                         theme_color='#00aaaa')

@app.route('/upload', methods=['POST'])
def upload_csv():
    """Upload và xử lý file CSV"""
    try:
        if 'csv_file' not in request.files:
            return jsonify({'success': False, 'message': 'No file selected'})
        
        file = request.files['csv_file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file and file.filename.endswith('.csv'):
            # Read CSV content
            csv_content = file.read().decode('utf-8')
            csv_io = StringIO(csv_content)
            
            # Parse CSV using built-in csv module
            csv_reader = csv.DictReader(csv_io)
            participants_data = list(csv_reader)
            
            # Validate required columns
            required_columns = ['identifier', 'name']
            if not participants_data:
                return jsonify({'success': False, 'message': 'CSV file is empty'})
            
            if not all(col in participants_data[0].keys() for col in required_columns):
                return jsonify({'success': False, 'message': f'CSV must contain columns: {", ".join(required_columns)}'})
            
            # Store in session or global variable
            app.config['participants_data'] = participants_data
            
            return jsonify({'success': True, 'message': f'Successfully uploaded {len(participants_data)} participants'})
        else:
            return jsonify({'success': False, 'message': 'Please upload a CSV file'})
            
    except Exception as e:
        logger.error(f"Error uploading CSV: {str(e)}")
        return jsonify({'success': False, 'message': f'Error uploading file: {str(e)}'})

@app.route('/start_sending', methods=['POST'])
def start_sending():
    """Bắt đầu gửi email"""
    global email_thread
    
    try:
        if email_status['is_running']:
            return jsonify({'success': False, 'message': 'Email sending is already in progress'})
        
        participants_data = app.config.get('participants_data', [])
        if not participants_data:
            return jsonify({'success': False, 'message': 'No participants data found. Please upload CSV first.'})
        
        # Start email sending in background thread
        email_thread = threading.Thread(target=send_emails_batch, args=(participants_data,))
        email_thread.daemon = True
        email_thread.start()
        
        return jsonify({'success': True, 'message': 'Email sending started'})
        
    except Exception as e:
        logger.error(f"Error starting email sending: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/stop_sending', methods=['POST'])
def stop_sending():
    """Dừng gửi email"""
    global email_status
    
    try:
        email_status['is_running'] = False
        return jsonify({'success': True, 'message': 'Email sending stopped'})
        
    except Exception as e:
        logger.error(f"Error stopping email sending: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/status')
def get_status():
    """Lấy trạng thái gửi email"""
    return jsonify(email_status)

@app.route('/logs')
def get_logs():
    """Lấy logs"""
    return jsonify({
        'logs': email_status['logs'][-100:],  # Last 100 logs
        'errors': email_status['errors'][-50:]  # Last 50 errors
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return "healthy", 200

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5005)
