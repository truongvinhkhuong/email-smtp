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
import re
from io import StringIO

from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config import (
    SMTP_CONFIG, EMAIL_CONFIG, EMAIL_TEMPLATES, 
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
    
    def __init__(self, template_type='web'):
        self.smtp_config = SMTP_CONFIG['naver']
        self.email_config = EMAIL_CONFIG.copy()
        self.email_config['sender_email'] = 'devgrowth@naver.com'
        self.email_config['sender_password'] = '5N6WJ2B3596R'
        self.template_type = template_type
        
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        # Strip whitespace before validation
        email = email.strip()
        return re.match(EMAIL_REGEX, email) is not None
    
    def create_email_message(self, recipient_name: str, recipient_email: str) -> MIMEMultipart:
        """Tạo email message"""
        # Get template based on type
        template = EMAIL_TEMPLATES.get(self.template_type, EMAIL_TEMPLATES['web'])
        
        # Create HTML content
        html_content = template['html_template']
        
        # Create text content (fallback)
        text_content = template['text_template']
        
        # Create multipart message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.email_config['sender_name']} <{self.email_config['sender_email']}>"
        msg['To'] = recipient_email
        msg['Subject'] = template['subject']
        
        # Add both text and HTML parts
        text_part = MIMEText(text_content, 'plain', 'utf-8')
        html_part = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
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
            if self.smtp_config['use_ssl']:
                # Use SSL connection for Naver
                with smtplib.SMTP_SSL(self.smtp_config['server'], self.smtp_config['port']) as server:
                    server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                    
                    # Send email
                    server.send_message(msg)
                    logger.info(f"Email sent successfully to {recipient_name} ({recipient_email})")
                    return True
            else:
                # Use TLS connection for other providers
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

def send_emails_batch(participants_data: List[Dict[str, str]], template_type: str = 'web'):
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
        
        # Log start information
        email_status['logs'].append({
            'timestamp': datetime.now().isoformat(),
            'type': 'info',
            'message': f"Starting email sending process with {template_type} template"
        })
        email_status['logs'].append({
            'timestamp': datetime.now().isoformat(),
            'type': 'info',
            'message': f"Total emails: {len(participants_data)}, Batches: {email_status['total_batches']}, Batch size: {batch_size}"
        })
        
        sender = EmailSender(template_type)
        
        # Process in batches
        for batch_idx in range(email_status['total_batches']):
            if not email_status['is_running']:  # Check if stopped
                email_status['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'warning',
                    'message': f"Email sending stopped by user at batch {batch_idx + 1}/{email_status['total_batches']}"
                })
                break
                
            email_status['current_batch'] = batch_idx + 1
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(participants_data))
            batch_data = participants_data[start_idx:end_idx]
            
            # Log batch start
            email_status['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'type': 'info',
                'message': f"Processing batch {batch_idx + 1}/{email_status['total_batches']} (emails {start_idx + 1}-{end_idx})"
            })
            
            # Send emails in current batch
            for email_idx, participant in enumerate(batch_data):
                if not email_status['is_running']:  # Check if stopped
                    current_email_idx = start_idx + email_idx + 1
                    email_status['logs'].append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'warning',
                        'message': f"Email sending stopped by user at email {current_email_idx}/{len(participants_data)} in batch {batch_idx + 1}"
                    })
                    break
                    
                email = participant.get('identifier', '').strip()
                # Extract name from email (part before @)
                name = email.split('@')[0] if '@' in email else email
                current_email_idx = start_idx + email_idx + 1
                
                # Log current email being processed
                email_status['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'info',
                    'message': f"Processing email {current_email_idx}/{len(participants_data)}: {name} ({email})"
                })
                
                if sender.send_email(name, email):
                    email_status['sent_emails'] += 1
                    email_status['logs'].append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'success',
                        'message': f"✅ Email sent successfully to {name} ({email}) - {email_status['sent_emails']}/{len(participants_data)} completed"
                    })
                else:
                    email_status['failed_emails'] += 1
                    email_status['errors'].append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'error',
                        'message': f"❌ Failed to send email to {name} ({email}) - {email_status['failed_emails']} failed so far"
                    })
                
                # Delay between emails
                time.sleep(float(EMAIL_CONFIG.get('delay_between_emails', 1)))
            
            # Log batch completion
            if email_status['is_running']:
                email_status['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'info',
                    'message': f"✅ Batch {batch_idx + 1}/{email_status['total_batches']} completed. Progress: {email_status['sent_emails']} sent, {email_status['failed_emails']} failed"
                })
            
            # Delay between batches
            if batch_idx < email_status['total_batches'] - 1 and email_status['is_running']:
                delay_seconds = float(EMAIL_CONFIG.get('delay_between_batches', 300))
                email_status['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'info',
                    'message': f"Waiting {delay_seconds} seconds before next batch..."
                })
                time.sleep(delay_seconds)
        
        if email_status['is_running']:
            email_status['end_time'] = datetime.now().isoformat()
            email_status['is_running'] = False
            email_status['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'type': 'success',
                'message': f"🎉 Email sending completed! Total: {email_status['sent_emails']} sent, {email_status['failed_emails']} failed"
            })
        else:
            email_status['end_time'] = datetime.now().isoformat()
            email_status['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'type': 'warning',
                'message': f"⏹️ Email sending stopped by user. Final stats: {email_status['sent_emails']} sent, {email_status['failed_emails']} failed"
            })
        
    except Exception as e:
        logger.error(f"Error in email sending process: {str(e)}")
        email_status['errors'].append({
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'message': f"💥 Email sending process error: {str(e)}"
        })
        email_status['is_running'] = False
        email_status['end_time'] = datetime.now().isoformat()
        email_status['logs'].append({
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'message': f"💥 Process stopped due to error. Final stats: {email_status['sent_emails']} sent, {email_status['failed_emails']} failed"
        })


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
            participants_data = []
            
            # Process each row and strip whitespace
            for row in csv_reader:
                # Strip whitespace from all values
                cleaned_row = {key: value.strip() if value else value for key, value in row.items()}
                participants_data.append(cleaned_row)
            
            # Validate required columns
            required_columns = ['identifier']
            if not participants_data:
                return jsonify({'success': False, 'message': 'CSV file is empty'})
            
            if not all(col in participants_data[0].keys() for col in required_columns):
                return jsonify({'success': False, 'message': f'CSV must contain column: {", ".join(required_columns)}'})
            
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
        
        # Get template type from request
        data = request.get_json() or {}
        template_type = data.get('template', 'web')
        
        # Validate template type
        if template_type not in EMAIL_TEMPLATES:
            return jsonify({'success': False, 'message': 'Invalid template type'})
        
        # Start email sending in background thread
        email_thread = threading.Thread(target=send_emails_batch, args=(participants_data, template_type))
        email_thread.daemon = True
        email_thread.start()
        
        return jsonify({'success': True, 'message': f'Email sending started with {template_type} template for {len(participants_data)} participants'})
        
    except Exception as e:
        logger.error(f"Error starting email sending: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/stop_sending', methods=['POST'])
def stop_sending():
    """Dừng gửi email"""
    global email_status
    
    try:
        if email_status['is_running']:
            email_status['is_running'] = False
            email_status['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'type': 'warning',
                'message': f"🛑 Stop request received. Current progress: {email_status['sent_emails']} sent, {email_status['failed_emails']} failed"
            })
            return jsonify({'success': True, 'message': f'Email sending stop requested. Current progress: {email_status["sent_emails"]} sent, {email_status["failed_emails"]} failed'})
        else:
            return jsonify({'success': False, 'message': 'Email sending is not currently running'})
        
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
