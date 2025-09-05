#!/usr/bin/env python3
"""
Script để tạo dữ liệu test cho NAVER Vietnam AI Hackathon
Tạo file participants.csv với 2000+ email test
"""

import csv
import random
from typing import List

# Danh sách tên Việt Nam phổ biến
VIETNAMESE_FIRST_NAMES = [
    "An", "Bình", "Cường", "Dung", "Em", "Phương", "Giang", "Hoa", "Inh", "Kim",
    "Long", "Mai", "Nam", "Oanh", "Phúc", "Quỳnh", "Rạng", "Sinh", "Tài", "Uyên",
    "Vinh", "Xuân", "Yên", "Zara", "Anh", "Bảo", "Cường", "Dung", "Em", "Phương",
    "Giang", "Hoa", "Inh", "Kim", "Long", "Mai", "Nam", "Oanh", "Phúc", "Quỳnh"
]

VIETNAMESE_LAST_NAMES = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đặng", "Bùi", "Ngô", "Dương",
    "Phan", "Trịnh", "Đinh", "Lý", "Chu", "Tôn", "Võ", "Đỗ", "Hồ", "Vũ"
]

# Danh sách domain email phổ biến
EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "naver.com",
    "example.com", "test.com", "demo.com", "sample.com", "hackathon.com"
]

def generate_vietnamese_name() -> str:
    """Tạo tên Việt Nam ngẫu nhiên"""
    last_name = random.choice(VIETNAMESE_LAST_NAMES)
    first_name = random.choice(VIETNAMESE_FIRST_NAMES)
    return f"{last_name} {first_name}"

def generate_email(name: str, index: int) -> str:
    """Tạo email từ tên và index"""
    # Tạo username từ tên
    name_parts = name.lower().split()
    if len(name_parts) >= 2:
        username = f"{name_parts[0]}.{name_parts[1]}{index}"
    else:
        username = f"{name_parts[0]}{index}"
    
    # Chọn domain ngẫu nhiên
    domain = random.choice(EMAIL_DOMAINS)
    
    return f"{username}@{domain}"

def generate_participants(count: int) -> List[dict]:
    """Tạo danh sách participants"""
    participants = []
    
    for i in range(1, count + 1):
        name = generate_vietnamese_name()
        email = generate_email(name, i)
        
        participants.append({
            'identifier': email,
            'name': name
        })
    
    return participants

def save_to_csv(participants: List[dict], filename: str = 'participants.csv'):
    """Lưu participants vào file CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['identifier', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for participant in participants:
            writer.writerow(participant)
    
    print(f"Saved {len(participants)} participants to {filename}")

def main():
    """Main function"""
    print("NAVER Vietnam AI Hackathon - Test Data Generator")
    print("=" * 60)
    
    # Tạo 2000 participants
    count = 2000
    print(f"Generating {count} test participants...")
    
    participants = generate_participants(count)
    
    # Lưu vào file CSV
    save_to_csv(participants)
    
    # Hiển thị thống kê
    print(f"\nStatistics:")
    print(f"   Total participants: {len(participants)}")
    
    # Thống kê domain
    domains = {}
    for p in participants:
        domain = p['identifier'].split('@')[1]
        domains[domain] = domains.get(domain, 0) + 1
    
    print(f"   Email domains:")
    for domain, count in sorted(domains.items()):
        print(f"     {domain}: {count}")
    
    # Hiển thị 5 participants đầu tiên
    print(f"\nFirst 5 participants:")
    for i, p in enumerate(participants[:5]):
        print(f"   {i+1}. {p['name']} - {p['identifier']}")
    
    print(f"\nTest data generation completed!")
    print(f"   File: participants.csv")
    print(f"   Ready for email sending test!")

if __name__ == '__main__':
    main()
