import os
from typing import Dict, TypedDict, Union
from dotenv import load_dotenv

# Load environment variables từ file .env
# Điều này giúp:
# - Bảo mật thông tin nhạy cảm (API endpoints, credentials)
# - Dễ dàng thay đổi config theo môi trường (dev/staging/prod)
# - Không phải hard-code các giá trị configuration
load_dotenv()

class Config:
    # Lưu trữ các endpoint của services
    # Được load từ environment variables để dễ dàng thay đổi
    AI_SERVER = os.getenv('AI_SERVER')  # Endpoint của AI service xử lý NLP
    BE_SERVER = os.getenv('BE_SERVER')  # Endpoint của backend service
    DATE_FORMAT = "%d-%m-%Y"  # Format chuẩn cho dates trong hệ thống

# TypedDict giúp type checking chặt chẽ hơn cho dictionary
# Định nghĩa structure cho number mappings
class NumberMapping(TypedDict):
    vietnamese: Dict[str, str]  # Map số tiếng Việt sang số
    budget_multipliers: Dict[str, int]  # Map đơn vị tiền tệ sang multiplier

# Constants cho việc chuyển đổi số và đơn vị
# Hỗ trợ xử lý input tiếng Việt của user
NUMBERS: NumberMapping = {
    # Map số tiếng Việt sang số 
    "vietnamese": {
        'một': '1', 'hai': '2', 'ba': '3', 'bốn': '4', 'năm': '5',
        'sáu': '6', 'bảy': '7', 'tám': '8', 'chín': '9', 'mười': '10'
    },
    # Hệ số nhân cho các đơn vị tiền tệ
    # Ví dụ: "5k" -> 5000, "1tr" -> 1000000
    "budget_multipliers": {
        'k': 1000,  # nghìn
        'm': 1000000,  # triệu
        'triệu': 1000000,
        'tr': 1000000,
        'tỷ': 1000000000
    }
}

class ValidationPatterns:
    """
    Chứa các regex patterns để validate và extract thông tin từ user input
    Tất cả patterns đều có flag (?ix) để:
    - i: case insensitive
    - x: ignore whitespace và comments trong regex
    """
    
    # Pattern cho số điện thoại
    # Yêu cầu đúng 10 chữ số
    PHONE = r"[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
    
    # Pattern cho số người
    # Matches:
    # - Số + "người/khách" (ví dụ: "5 người", "10 khách")
    # - Số tiếng Việt + "người/khách" (ví dụ: "năm người", "mười khách")
    PEOPLE = r"""(?ix)\b(?:(?:\d+(?:\.\d+)?|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:người|khách))\b"""
    
    # Pattern cho ngân sách/budget
    # Matches các format:
    # - Số + đơn vị tiền (ví dụ: "5k", "1 triệu", "2tr")
    # - Số tiếng Việt + đơn vị (ví dụ: "năm triệu", "hai tỷ")
    # - Các đơn vị tiền tệ khác nhau (vnđ, usd, đồng)
    BUDGET = r"""(?ix)\b(?:\d+(?:\.\d+)?|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|mươi|trăm|nghìn|triệu|tỷ)\s*(?:k|triệu|tr|tỷ|nghìn|đ|vnđ|usd|vnd|đồng|dollars?)?\b"""
    
    # Pattern cho ngày tháng
    # Matches các format:
    # - "ngày DD/MM/YYYY" hoặc "ngày DD-MM-YYYY"
    # - "tháng MM/YYYY" hoặc "tháng MM-YYYY"
    # - DD/MM/YYYY hoặc DD-MM-YYYY
    DATE = r"""(?ix)\b((ngày\s([1-9]|[12][0-9]|3[01])(?:[/-][1-9]|1[0-2])?(?:[/-]\d{4})?)|(tháng\s([1-9]|1[0-2])(?:[/-]\d{4})?)|([0-3]?[0-9][/-][0-1]?[0-9](?:[/-]\d{4})?))\b"""
    
    # Pattern cho thời gian du lịch
    # Matches:
    # - X ngày Y đêm (ví dụ: "3 ngày 2 đêm", "năm ngày bốn đêm")
    # - X [đơn vị thời gian] (ví dụ: "2 tuần", "một tháng", "ba ngày")
    DURATION = r"""(?ix)\b(?:(?:(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*ngày\s*(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*đêm)|(?:(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:ngày|tuần|tháng|năm)))\b"""