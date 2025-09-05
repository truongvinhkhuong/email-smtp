#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for NAVER Vietnam AI Hackathon Email Sender
"""

import requests
import json
import time
import sys

def test_health_check(base_url):
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_upload_csv(base_url):
    """Test CSV upload functionality"""
    print("🔍 Testing CSV upload...")
    try:
        # Create test CSV content
        csv_content = "identifier,name\ntest@example.com,Test User"
        
        files = {
            'csv_file': ('test.csv', csv_content, 'text/csv')
        }
        
        response = requests.post(f"{base_url}/upload", files=files, timeout=30)
        if response.status_code == 200:  # JSON response after successful upload
            data = response.json()
            if data.get('success'):
                print("✅ CSV upload test passed")
                return True
            else:
                print(f"❌ CSV upload failed: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ CSV upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ CSV upload error: {e}")
        return False

def test_status_endpoint(base_url):
    """Test status endpoint"""
    print("🔍 Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Status endpoint working")
            print(f"   Total emails: {data.get('total_emails', 0)}")
            print(f"   Sent emails: {data.get('sent_emails', 0)}")
            print(f"   Is running: {data.get('is_running', False)}")
            return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
        return False

def test_logs_endpoint(base_url):
    """Test logs endpoint"""
    print("🔍 Testing logs endpoint...")
    try:
        response = requests.get(f"{base_url}/logs", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Logs endpoint working")
            print(f"   Logs count: {len(data.get('logs', []))}")
            print(f"   Errors count: {len(data.get('errors', []))}")
            return True
        else:
            print(f"❌ Logs endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Logs endpoint error: {e}")
        return False

def test_gmail_connection():
    """Test Gmail SMTP connection"""
    print("🔍 Testing Gmail SMTP connection...")
    try:
        import smtplib
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('khuonggg2924@gmail.com', 'oboxhjcfxkzqnpug')
        print("✅ Gmail SMTP connection successful")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Gmail SMTP connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Email Sender Application Tests")
    print("=" * 50)
    
    # Test configuration
    base_url = "http://localhost:5001"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing against: {base_url}")
    print()
    
    # Run tests
    tests = [
        ("Health Check", lambda: test_health_check(base_url)),
        ("Gmail SMTP", test_gmail_connection),
        ("Status Endpoint", lambda: test_status_endpoint(base_url)),
        ("Logs Endpoint", lambda: test_logs_endpoint(base_url)),
        ("CSV Upload", lambda: test_upload_csv(base_url)),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready for production.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
