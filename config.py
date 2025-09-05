
import os
from typing import Dict, Any

# Cấu hình SMTP Server
SMTP_CONFIG: Dict[str, Any] = {
    # Gmail Configuration
    'gmail': {
        'server': 'smtp.gmail.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False
    },
    # Outlook Configuration
    'outlook': {
        'server': 'smtp-mail.outlook.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False
    },
    # Yahoo Configuration
    'yahoo': {
        'server': 'smtp.mail.yahoo.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False
    }
}

# Cấu hình email
EMAIL_CONFIG = {
    # Thông tin người gửi (sẽ được đọc từ environment variables)
    'sender_email': os.getenv('SENDER_EMAIL', ''),
    'sender_password': os.getenv('SENDER_PASSWORD', ''),
    'sender_name': 'NAVER Vietnam AI Hackathon Team',
    
    # Subject và nội dung email
    'subject': '[NAVER Vietnam AI Hackathon 2025] Preliminary Assignment Released',
    
    # URLs cho các tracks
    'mobile_track_url': 'https://hackathon.naver.com/mobile-track',
    'web_track_url': 'https://hackathon.naver.com/web-track',
    
    # Thông tin cuộc thi
    'deadline': 'Sep 15, 2025 – 23:59 ICT',
    'support_email': 'support@contest.com',
    'discord_link': 'https://discord.gg/naver-ai-hackathon',
    'github_classroom_link': 'https://classroom.github.com/a/your-assignment-link',
    
    # Cấu hình gửi email
    'batch_size': 100,  # Số email gửi mỗi batch
    'delay_between_batches': 300,  # 5 phút = 300 giây
    'delay_between_emails': 1,  # 1 giây giữa các email trong cùng batch
    
    # File paths
    'participants_file': 'participants.csv',
    'log_file': 'log.txt',
    'checkpoint_file': 'checkpoint.txt',
    'error_log_file': 'error_log.txt'
}

# Template email HTML
EMAIL_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAVER Vietnam AI Hackathon</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.7;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .email-container {{
            max-width: 650px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 170, 170, 0.15);
            overflow: hidden;
            position: relative;
        }}
        
        .email-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #00aaaa 0%, #00cccc 50%, #00aaaa 100%);
        }}
        
        .header {{
            background: linear-gradient(135deg, #00aaaa 0%, #00cccc 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(180deg); }}
        }}
        
        .header h1 {{
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }}
        
        .header h2 {{
            font-size: 1.3em;
            font-weight: 400;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }}
        
        .content {{
            padding: 40px 30px;
            background: white;
        }}
        
        .greeting {{
            font-size: 1.1em;
            margin-bottom: 25px;
            color: #34495e;
        }}
        
        .welcome-text {{
            font-size: 1.1em;
            margin-bottom: 30px;
            color: #2c3e50;
            line-height: 1.8;
        }}
        
        .assignment-card {{
            background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 100%);
            border: 2px solid #00aaaa;
            border-radius: 15px;
            padding: 25px;
            margin: 25px 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .assignment-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00aaaa, #00cccc, #00aaaa);
        }}
        
        .assignment-card h3 {{
            color: #00aaaa;
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .requirements {{
            margin: 30px 0;
        }}
        
        .requirements h3 {{
            color: #2c3e50;
            font-size: 1.2em;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .requirements ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .requirements li {{
            background: #f8f9fa;
            margin: 10px 0;
            padding: 15px 20px;
            border-radius: 10px;
            border-left: 4px solid #00aaaa;
            position: relative;
            transition: all 0.3s ease;
        }}
        
        .requirements li::before {{
            content: '✓';
            color: #00aaaa;
            font-weight: bold;
            margin-right: 10px;
        }}
        
        .cta-section {{
            text-align: center;
            margin: 35px 0;
        }}
        
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, #00aaaa 0%, #00cccc 100%);
            color: white;
            padding: 16px 32px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1em;
            box-shadow: 0 8px 20px rgba(0, 170, 170, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }}
        
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(0, 170, 170, 0.4);
        }}
        
        .button:hover::before {{
            left: 100%;
        }}
        
        .warning-card {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border: 2px solid #f39c12;
            border-radius: 15px;
            padding: 25px;
            margin: 25px 0;
            position: relative;
        }}
        
        .warning-card h3 {{
            color: #e67e22;
            font-size: 1.2em;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .warning-card ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .warning-card li {{
            margin: 8px 0;
            padding: 8px 0;
            color: #8b4513;
        }}
        
        .warning-card li::before {{
            content: '⚠️';
            margin-right: 10px;
        }}
        
        .closing {{
            margin: 30px 0;
            font-size: 1.1em;
            color: #2c3e50;
        }}
        
        .signature {{
            margin: 25px 0;
            font-size: 1.1em;
            color: #34495e;
        }}
        
        .footer {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 30px;
            border-top: 1px solid #dee2e6;
        }}
        
        .footer h4 {{
            color: #00aaaa;
            font-size: 1.1em;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .footer p {{
            margin: 8px 0;
            color: #6c757d;
        }}
        
        .footer a {{
            color: #00aaaa;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        .disclaimer {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            font-size: 0.85em;
            color: #6c757d;
            text-align: center;
        }}
        
        @media (max-width: 600px) {{
            .email-container {{
                margin: 10px;
                border-radius: 15px;
            }}
            
            .header, .content, .footer {{
                padding: 25px 20px;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .button {{
                padding: 14px 28px;
                font-size: 1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>NAVER Vietnam AI Hackathon 2025</h1>
            <h2>Preliminary Assignment Released</h2>
        </div>
        
        <div class="content">
            <div class="greeting">
                <p>Dear <strong>{name}</strong>,</p>
            </div>
            
            <div class="welcome-text">
                <p>Welcome to the Preliminary Round of the <strong>NAVER Vietnam AI Hackathon 2025</strong>! 🎉</p>
                <p>You are now invited to complete your Preliminary Assignment:</p>
            </div>
            
            <div class="assignment-card">
                <h3>Build a To-Do App (React / React Native)</h3>
            </div>
            
            <div class="requirements">
                <h3>📋 What you need to submit (by {deadline}):</h3>
                <ul>
                    <li>A GitHub repository (automatically created through GitHub Classroom from our template) containing your code.</li>
                    <li>An updated README.md file, completed with all required content.</li>
                </ul>
            </div>
            
            <div class="cta-section">
                <a href="{github_classroom_link}" class="button">📖 View Full Assignment Details</a>
            </div>
            
            <div class="warning-card">
                <h3>⚠️ Important Notes</h3>
                <ul>
                    <li>This is an individual assignment.</li>
                    <li>Late submissions will not be accepted.</li>
                    <li><strong>Deadline: {deadline} (strict cutoff)</strong></li>
                </ul>
            </div>
            
            <div class="closing">
                <p>We wish you the best of luck and are excited to see your creativity in action! 🚀</p>
            </div>
            
            <div class="signature">
                <p>Best regards,<br>
                <strong>NAVER Vietnam AI Hackathon 2025 Team</strong></p>
            </div>
        </div>
        
        <div class="footer">
            <h4>📞 Support & Contact</h4>
            <p><strong>Email:</strong> {support_email}</p>
            <p><strong>Discord:</strong> <a href="{discord_link}">Join our Discord community</a></p>
            <p><strong>Website:</strong> <a href="https://hackathon.naver.com">hackathon.naver.com</a></p>
            
            <div class="disclaimer">
                <p>This is an automated email, please do not reply directly.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Template email plain text
EMAIL_TEXT_TEMPLATE = """
[NAVER Vietnam AI Hackathon 2025] Preliminary Assignment Released

Dear {name},

Welcome to the Preliminary Round of the NAVER Vietnam AI Hackathon 2025! 🎉

You are now invited to complete your Preliminary Assignment:
👉 Build a To-Do App (React / React Native).

What you need to submit (by {deadline}):
- A GitHub repository (automatically created through GitHub Classroom from our template) containing your code.
- An updated README.md file, completed with all required content.

📖 Full assignment details & instructions: {github_classroom_link}

⚠️ Please note:
- This is an individual assignment.
- Late submissions will not be accepted.
- Deadline: {deadline} (strict cutoff)

We wish you the best of luck and are excited to see your creativity in action 🚀.

Best regards,
NAVER Vietnam AI Hackathon 2025 Team

---
SUPPORT:
Email: {support_email}
Discord: {discord_link}
Website: https://hackathon.naver.com

This is an automated email, please do not reply directly.
"""

# Regex để validate email
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Cấu hình test mode
TEST_MODE = {
    'enabled': False,  # Set to True để chỉ gửi 5 email đầu tiên
    'test_emails_count': 5
}
