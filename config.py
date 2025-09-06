
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
    # Naver Configuration
    'naver': {
        'server': 'smtp.naver.com',
        'port': 465,
        'use_tls': False,
        'use_ssl': True
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

# Email Templates Configuration
EMAIL_TEMPLATES = {
    'web': {
        'subject': '[NAVER Vietnam AI Hackathon 2025] Preliminary Assignment Released',
        'text_template': """
**NAVER Vietnam AI Hackathon 2025 - Preliminary Assignment Released**

Dear **Participant**,

Welcome to the **Preliminary Round** of the NAVER Vietnam AI Hackathon 2025! 🎉

You are now invited to complete your **Preliminary Assignment**:
👉 **Build a To-Do App (React / React Native)**

**What you need to submit** (by **Sep 15, 18:00 Vietnam time**):
• A **GitHub repository** (automatically created through GitHub Classroom from our template) containing your code
• **Executable demo**: Deployment link or local execution guide
• **Project documentation**: An updated README.md file, completed with all required content

📖 **Assignment Platform**: [https://classroom.github.com/a/mImcFdiB](https://classroom.github.com/a/mImcFdiB)
You can view the full details and instructions in the Platform.

⚠️ **Please note**:
• This is an **individual assignment**
• **Late submissions will not be accepted**
• **Deadline**: Sep 15, 2025 - 18:00 (strict cutoff)

If you have any issues, please submit this form: [https://forms.gle/BQwvwmitbh37ZvCF8](https://forms.gle/BQwvwmitbh37ZvCF8)

We wish you the best of luck and are excited to see your creativity in action 🚀

**Best regards,**
*The Organizing Committee*
**NAVER Vietnam AI Hackathon 2025**
        """,
        'html_template': """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAVER Vietnam AI Hackathon 2025</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #00aaaa 0%, #00cccc 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }}
        .content {{ background: #f9f9f9; padding: 20px; border-radius: 10px; }}
        .section {{ margin: 20px 0; }}
        .highlight {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; border-radius: 5px; margin: 15px 0; }}
        .warning {{ background: #f8d7da; padding: 15px; border-left: 4px solid #dc3545; border-radius: 5px; margin: 15px 0; }}
        .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #e9ecef; border-radius: 10px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 8px 0; }}
        a {{ color: #00aaaa; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
     
    <div class="content">
        <p>Dear <strong>Participant</strong>,</p>
        
        <p>Welcome to the <strong>Preliminary Round</strong> of the NAVER Vietnam AI Hackathon 2025! 🎉</p>
        
        <div class="section">
            <p>You are now invited to complete your <strong>Preliminary Assignment</strong>:</p>
            <p>👉 <strong>Build a To-Do App (React / React Native)</strong></p>
        </div>
        
        <div class="highlight">
            <h3><strong>What you need to submit</strong> (by <strong>Sep 15, 18:00 Vietnam time</strong>):</h3>
            <ul>
                <li>A <strong>GitHub repository</strong> (automatically created through GitHub Classroom from our template) containing your code</li>
                <li><strong>Executable demo</strong>: Deployment link or local execution guide</li>
                <li><strong>Project documentation</strong>: An updated README.md file, completed with all required content</li>
            </ul>
        </div>
        
        <div class="section">
            <p>📖 <strong>Assignment Platform</strong>: <a href="https://classroom.github.com/a/mImcFdiB">https://classroom.github.com/a/mImcFdiB</a></p>
            <p>You can view the full details and instructions in the Platform.</p>
        </div>
        
        <div class="warning">
            <h3>⚠️ <strong>Please note</strong>:</h3>
            <ul>
                <li>This is an <strong>individual assignment</strong></li>
                <li><strong>Late submissions will not be accepted</strong></li>
                <li><strong>Deadline</strong>: Sep 15, 2025 - 18:00 (strict cutoff)</li>
            </ul>
        </div>
        
        <p>If you have any issues, please submit this form: <a href="https://forms.gle/BQwvwmitbh37ZvCF8">https://forms.gle/BQwvwmitbh37ZvCF8</a></p>
        
        <p>We wish you the best of luck and are excited to see your creativity in action 🚀</p>
    </div>
    
    <div class="footer">
        <p><strong>Best regards,</strong></p>
        <p><em>The Organizing Committee</em></p>
        <p><strong>NAVER Vietnam AI Hackathon 2025</strong></p>
    </div>
</body>
</html>
        """
    },
    'mobile': {
        'subject': '[NAVER Vietnam AI Hackathon 2025] Preliminary Assignment Released',
        'text_template': """
**NAVER Vietnam AI Hackathon 2025 - Preliminary Assignment Released**

Dear **Participant**,

Welcome to the **Preliminary Round** of the NAVER Vietnam AI Hackathon 2025! 🎉

You are now invited to complete your **Preliminary Assignment**:
👉 **Build a To-Do App (Kotlin / Java)**

**What you need to submit** (by **Sep 15, 18:00 Vietnam time**):
• A **GitHub repository** (automatically created through GitHub Classroom from our template) containing your code
• **Executable demo**: APK file
• **Project documentation**: An updated README.md file, completed with all required content

📖 **Assignment Platform**: [https://classroom.github.com/a/U6KLaMSq](https://classroom.github.com/a/U6KLaMSq)
You can view the full details and instructions in the Platform.

⚠️ **Please note**:
• This is an **individual assignment**
• **Late submissions will not be accepted**
• **Deadline**: Sep 15, 2025 - 18:00 (strict cutoff)

If you have any issues, please submit this form: [https://forms.gle/BQwvwmitbh37ZvCF8](https://forms.gle/BQwvwmitbh37ZvCF8)

We wish you the best of luck and are excited to see your creativity in action 🚀

**Best regards,**
*The Organizing Committee*
**NAVER Vietnam AI Hackathon 2025**
        """,
        'html_template': """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAVER Vietnam AI Hackathon 2025</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #00aaaa 0%, #00cccc 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }}
        .content {{ background: #f9f9f9; padding: 20px; border-radius: 10px; }}
        .section {{ margin: 20px 0; }}
        .highlight {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; border-radius: 5px; margin: 15px 0; }}
        .warning {{ background: #f8d7da; padding: 15px; border-left: 4px solid #dc3545; border-radius: 5px; margin: 15px 0; }}
        .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #e9ecef; border-radius: 10px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 8px 0; }}
        a {{ color: #00aaaa; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
     
    <div class="content">
        <p>Dear <strong>Participant</strong>,</p>
        
        <p>Welcome to the <strong>Preliminary Round</strong> of the NAVER Vietnam AI Hackathon 2025! 🎉</p>
        
        <div class="section">
            <p>You are now invited to complete your <strong>Preliminary Assignment</strong>:</p>
            <p>👉 <strong>Build a To-Do App (Kotlin / Java)</strong></p>
        </div>
        
        <div class="highlight">
            <h3><strong>What you need to submit</strong> (by <strong>Sep 15, 18:00 Vietnam time</strong>):</h3>
            <ul>
                <li>A <strong>GitHub repository</strong> (automatically created through GitHub Classroom from our template) containing your code</li>
                <li><strong>Executable demo</strong>: APK file</li>
                <li><strong>Project documentation</strong>: An updated README.md file, completed with all required content</li>
            </ul>
        </div>
        
        <div class="section">
            <p>📖 <strong>Assignment Platform</strong>: <a href="https://classroom.github.com/a/U6KLaMSq">https://classroom.github.com/a/U6KLaMSq</a></p>
            <p>You can view the full details and instructions in the Platform.</p>
        </div>
        
        <div class="warning">
            <h3>⚠️ <strong>Please note</strong>:</h3>
            <ul>
                <li>This is an <strong>individual assignment</strong></li>
                <li><strong>Late submissions will not be accepted</strong></li>
                <li><strong>Deadline</strong>: Sep 15, 2025 - 18:00 (strict cutoff)</li>
            </ul>
        </div>
        
        <p>If you have any issues, please submit this form: <a href="https://forms.gle/BQwvwmitbh37ZvCF8">https://forms.gle/BQwvwmitbh37ZvCF8</a></p>
        
        <p>We wish you the best of luck and are excited to see your creativity in action 🚀</p>
    </div>
    
    <div class="footer">
        <p><strong>Best regards,</strong></p>
        <p><em>The Organizing Committee</em></p>
        <p><strong>NAVER Vietnam AI Hackathon 2025</strong></p>
    </div>
</body>
</html>
        """
    },
    'web_mobile': {
        'subject': '[NAVER Vietnam] Your Hackathon Registration is Confirmed: Preliminary Assignment Inside',
        'text_template': """
**NAVER Vietnam - Your Hackathon Registration is Confirmed: Preliminary Assignment Inside**

**Let's Get Started**
Hi **Participant**,

Thank you for registering for the **NAVER Vietnam AI Hackathon 2025** - your application has been successfully received!

**What's Next**
You are now invited to complete your **Preliminary Assignment**: **Build a To-Do App**

📖 **Assignment Platform**
• **Web**: [https://classroom.github.com/a/mImcFdiB](https://classroom.github.com/a/mImcFdiB)
• **Mobile Android**: [https://classroom.github.com/a/U6KLaMSq](https://classroom.github.com/a/U6KLaMSq)

*Applicants must select a track when applying, track changes are not allowed after submission.*

**What you need to submit** (by **Sep 15, 18:00 Vietnam time**):
• A **GitHub repository** (automatically created through GitHub Classroom from our template) containing your code
• **Executable demo**: 
  - *Web*: Deployment link or local execution guide
  - *Mobile App*: APK file
• **Project documentation**: An updated README.md file, completed with all required content

You can view the full details and instructions in the Assignment Platform.

⚠️ **Please note**:
• This is an **individual assignment**
• **Late submissions will not be accepted**
• **Deadline**: Sep 15, 2025 – 18:00 (strict cutoff)

If you have any issues, please submit this form: [https://forms.gle/BQwvwmitbh37ZvCF8](https://forms.gle/BQwvwmitbh37ZvCF8)

**Join Our Official Discord - It's Where Everything Happens!**
To make the most out of your hackathon journey, we strongly recommend joining our Discord Community:
📌 **Discord Invitation Code**: KbhfW5tnmQ

**Here's what you'll find inside**:
• *Real-time announcements & Reminders*
• *Free mini-courses & Tech tips from mentors*
• *A chance to connect with fellow participants and form study or project groups*
• *Ask questions, share ideas, and get help quickly*

*Joining Discord early will help you stay ahead and feel connected throughout the event.*

We wish you the best of luck and are excited to see your creativity in action 🚀

**Best Regards,**
*The Organizing Committee*
**NAVER Vietnam AI Hackathon 2025**
        """,
        'html_template': """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAVER Vietnam AI Hackathon 2025</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #00aaaa 0%, #00cccc 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
        .content { background: #f9f9f9; padding: 20px; border-radius: 10px; }
        .section { margin: 20px 0; }
        .highlight { background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; border-radius: 5px; margin: 15px 0; }
        .warning { background: #f8d7da; padding: 15px; border-left: 4px solid #dc3545; border-radius: 5px; margin: 15px 0; }
        .discord {{ background: #e3f2fd; padding: 20px; border-left: 4px solid #2196f3; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #e9ecef; border-radius: 10px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 8px 0; }}
        a {{ color: #00aaaa; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .track-info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
    </style>
</head>
<body> 
    <div class="content">
        <h3><strong>Let's Get Started</strong></h3>
        <p>Hi <strong>Participant</strong>,</p>
        
        <p>Thank you for registering for the <strong>NAVER Vietnam AI Hackathon 2025</strong> - your application has been successfully received!</p>
        
        <div class="section">
            <h3><strong>What's Next</strong></h3>
            <p>You are now invited to complete your <strong>Preliminary Assignment</strong>: <strong>Build a To-Do App</strong></p>
        </div>
        
        <div class="track-info">
            <h3>📖 <strong>Assignment Platform</strong></h3>
            <ul>
                <li><strong>Web</strong>: <a href="https://classroom.github.com/a/mImcFdiB">https://classroom.github.com/a/mImcFdiB</a></li>
                <li><strong>Mobile Android</strong>: <a href="https://classroom.github.com/a/U6KLaMSq">https://classroom.github.com/a/U6KLaMSq</a></li>
            </ul>
            <p><em>Applicants must select a track when applying, track changes are not allowed after submission.</em></p>
        </div>
        
        <div class="highlight">
            <h3><strong>What you need to submit</strong> (by <strong>Sep 15, 18:00 Vietnam time</strong>):</h3>
            <ul>
                <li>A <strong>GitHub repository</strong> (automatically created through GitHub Classroom from our template) containing your code</li>
                <li><strong>Executable demo</strong>: 
                    <ul>
                        <li><em>Web</em>: Deployment link or local execution guide</li>
                        <li><em>Mobile App</em>: APK file</li>
                    </ul>
                </li>
                <li><strong>Project documentation</strong>: An updated README.md file, completed with all required content</li>
            </ul>
        </div>
        
        <p>You can view the full details and instructions in the Assignment Platform.</p>
        
        <div class="warning">
            <h3>⚠️ <strong>Please note</strong>:</h3>
            <ul>
                <li>This is an <strong>individual assignment</strong></li>
                <li><strong>Late submissions will not be accepted</strong></li>
                <li><strong>Deadline</strong>: Sep 15, 2025 – 18:00 (strict cutoff)</li>
            </ul>
        </div>
        
        <p>If you have any issues, please submit this form: <a href="https://forms.gle/BQwvwmitbh37ZvCF8">https://forms.gle/BQwvwmitbh37ZvCF8</a></p>
        
        <div class="discord">
            <h3><strong>Join Our Official Discord - It's Where Everything Happens!</strong></h3>
            <p>To make the most out of your hackathon journey, we strongly recommend joining our Discord Community:</p>
            <p>📌 <strong>Discord Invitation Code</strong>: KbhfW5tnmQ</p>
            
            <h4><strong>Here's what you'll find inside</strong>:</h4>
            <ul>
                <li><em>Real-time announcements & Reminders</em></li>
                <li><em>Free mini-courses & Tech tips from mentors</em></li>
                <li><em>A chance to connect with fellow participants and form study or project groups</em></li>
                <li><em>Ask questions, share ideas, and get help quickly</em></li>
            </ul>
            
            <p><em>Joining Discord early will help you stay ahead and feel connected throughout the event.</em></p>
        </div>
        
        <p>We wish you the best of luck and are excited to see your creativity in action 🚀</p>
    </div>
    
    <div class="footer">
        <p><strong>Best Regards,</strong></p>
        <p><em>The Organizing Committee</em></p>
        <p><strong>NAVER Vietnam AI Hackathon 2025</strong></p>
    </div>
</body>
</html>
        """
    }
}

# Legacy template for backward compatibility
EMAIL_TEXT_TEMPLATE = EMAIL_TEMPLATES['web']['text_template']

# Regex để validate email
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Cấu hình test mode
TEST_MODE = {
    'enabled': False,  # Set to True để chỉ gửi 5 email đầu tiên
    'test_emails_count': 5
}
