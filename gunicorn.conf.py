# Gunicorn configuration file for NAVER Vietnam AI Hackathon Email Sender

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5005"  # Changed to 0.0.0.0 for Docker
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 300
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'email-sender'

# Server mechanics
daemon = False
pidfile = 'logs/gunicorn.pid'
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Environment variables
raw_env = [
    'FLASK_APP=app.py',
    'FLASK_ENV=production',
]

# Preload app for better performance
preload_app = True

# Worker timeout for long-running requests
timeout = 300

# Graceful timeout
graceful_timeout = 30

# Forwarded allow ips (for nginx proxy)
forwarded_allow_ips = '*'  # Allow all IPs for Docker

# Secure headers
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-FOR': 'for',
}
