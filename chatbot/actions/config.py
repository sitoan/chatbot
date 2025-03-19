import os
from typing import Dict, TypedDict, Union
from dotenv import load_dotenv


load_dotenv()

class Config:
    AI_SERVER = os.getenv('AI_SERVER')  
    BE_SERVER = os.getenv('BE_SERVER') 
    DATE_FORMAT = "%d-%m-%Y"  
class NumberMapping(TypedDict):
    vietnamese: Dict[str, str]  
    budget_multipliers: Dict[str, int]  

NUMBERS: NumberMapping = {
    "vietnamese": {
        'một': '1', 'hai': '2', 'ba': '3', 'bốn': '4', 'năm': '5',
        'sáu': '6', 'bảy': '7', 'tám': '8', 'chín': '9', 'mười': '10'
    },

    "budget_multipliers": {
        'k': 1000,  # nghìn
        'm': 1000000,  # triệu
        'triệu': 1000000,
        'tr': 1000000,
        'tỷ': 1000000000
    }
}

class ValidationPatterns:

    PHONE = r"[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
    PEOPLE = r"""(?ix)\b(?:(?:\d+(?:\.\d+)?|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:người|khách))\b"""
    BUDGET = r"""(?ix)\b(?:\d+(?:\.\d+)?|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|mươi|trăm|nghìn|triệu|tỷ)\s*(?:k|triệu|tr|tỷ|nghìn|đ|vnđ|usd|vnd|đồng|dollars?)?\b"""
    DATE = r"""(?ix)\b((ngày\s([1-9]|[12][0-9]|3[01])(?:[/-][1-9]|1[0-2])?(?:[/-]\d{4})?)|(tháng\s([1-9]|1[0-2])(?:[/-]\d{4})?)|([0-3]?[0-9][/-][0-1]?[0-9](?:[/-]\d{4})?))\b"""
    DURATION = r"""(?ix)\b(?:(?:(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*ngày\s*(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*đêm)|(?:(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:ngày|tuần|tháng|năm)))\b"""