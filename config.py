
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
[NAVER Vietnam AI Hackathon 2025] Preliminary Assignment Released

Dear Paticipant,

Welcome to the Preliminary Round of the NAVER Vietnam AI Hackathon 2025! 🎉
You are now invited to complete your Preliminary Assignment:
👉 Build a To-Do App (React / React Native).

What you need to submit (by Sep 15, 18:00 Vietnam time):
- A GitHub repository (automatically created through GitHub Classroom from our template) containing your code.
- Executable demo: Deployment link or local execution guide
- Project documentation: An updated README.md file, completed with all required content.

📖 Assignment Platform: https://classroom.github.com/a/mImcFdiB
You can view the full details and instructions in Platform.

⚠️ Please note:
- This is an individual assignment.
- Late submissions will not be accepted.
- Deadline: Sep 15, 2025 - 18:00 (strict cutoff)

If you have any issue, please submit this form: https://forms.gle/BQwvwmitbh37ZvCF8

We wish you the best of luck and are excited to see your creativity in action 🚀.

Best regards,
The Organizing Committee NAVER Vietnam AI Hackathon 2025
        """
    },
    'mobile': {
        'subject': '[NAVER Vietnam AI Hackathon 2025] Preliminary Assignment Released',
        'text_template': """
[NAVER Vietnam AI Hackathon 2025] Preliminary Assignment Released

Dear Paticipant,

Welcome to the Preliminary Round of the NAVER Vietnam AI Hackathon 2025! 🎉
You are now invited to complete your Preliminary Assignment:
👉 Build a To-Do App (Kotlin / Java).

What you need to submit (by Sep 15, 18:00 Vietnam time):
- A GitHub repository (automatically created through GitHub Classroom from our template) containing your code.
- Executable demo: APK file
- Project documentation: An updated README.md file, completed with all required content.

📖 Assignment Platform: https://classroom.github.com/a/U6KLaMSq
You can view the full details and instructions in Platform.

⚠️ Please note:
- This is an individual assignment.
- Late submissions will not be accepted.
- Deadline: Sep 15, 2025 - 18:00 (strict cutoff)

If you have any issue, please submit this form: https://forms.gle/BQwvwmitbh37ZvCF8

We wish you the best of luck and are excited to see your creativity in action 🚀.

Best regards,
The Organizing Committee NAVER Vietnam AI Hackathon 2025
        """
    },
    'web_mobile': {
        'subject': '[NAVER Vietnam] Your Hackathon Registrations is Confirmed: Preliminary Assignment Inside',
        'text_template': """
[NAVER Vietnam] Your Hackathon Registrations is Confirmed: Preliminary Assignment Inside

Let's Get Started
Hi, Paticipant,
Thank you for registering for the NAVER Vietnam AI Hackathon 2025 - your application has been successfully received!

What's Next
You are now invited to complete your Preliminary Assignment: Build a To-Do App 

📖 Assignment Platform
Web: https://classroom.github.com/a/mImcFdiB
Mobile Android: https://classroom.github.com/a/U6KLaMSq
Applicants must select a track when applying, track changes are not allowed after submission.

What you need to submit (by Sep 15, 18:00 Vietnam time):
- A GitHub repository (automatically created through GitHub Classroom from our template) containing your code.
- Executable demo: Web - Deployment link or local execution guide, Mobile App - APK file
- Project documentation: An updated README.md file, completed with all required content.

You can view the full details and instructions in the Assignment Platform.

⚠️ Please note:
- This is an individual assignment.
- Late submissions will not be accepted.
- Deadline: Sep 15, 2025 – 18:00 (strict cutoff)

If you have any issue, please submit this form: https://forms.gle/BQwvwmitbh37ZvCF8

Join Our Official Discord - It's Where Everything Happens!
To make the most out of your hackathon journey, we strongly recommend joining our Discord Community:
📌 Discord Invitation Code: KbhfW5tnmQ

Here's what you'll find inside:
- Real-time announcements & Reminders
- Free mini-courses & Tech tips from mentors
- A chance to connect with fellow participants and form study or project groups
- Ask questions, share ideas, and get help quickly

Joining Discord early will help you stay ahead and feel connected throughout the event.

We wish you the best of luck and are excited to see your creativity in action 🚀.

Best Regards,
The Organizing Committee
NAVER Vietnam AI Hackathon 2025
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
