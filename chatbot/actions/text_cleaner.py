import re
from datetime import datetime
from typing import Optional

from .config import Config, NUMBERS

class TextCleaner:
    
    @staticmethod
    def clean_vietnamese_numbers(text: str) -> str:
        """Convert Vietnamese number words to digits."""
        result = text.lower()
        for vn_num, num in NUMBERS["vietnamese"].items():
            result = result.replace(vn_num, num)
        print(f"Cleaned text: {result}")
        return result

    @staticmethod
    def clean_date(date_text: str) -> Optional[str]:
        date_text = date_text.lower()
        print(f"Original date: {date_text}")
        date_text = date_text.replace('tháng', '/').replace('ngày', '').replace(' ', '')
        print(f"Cleaned date 1: {date_text}")
        
        parts = re.split(r'[/-]', date_text)
        print(f"Parts: {parts}")
        current_date = datetime.now()
        
        try:
            day = int(parts[0]) if parts[0] != '' else 1
            month = int(parts[1]) if len(parts) > 1 else current_date.month
            year = int(parts[2]) if len(parts) > 2 else current_date.year + 1

            print(f"Cleaned date 2: {datetime(year, month, day).strftime(Config.DATE_FORMAT)}")
            return datetime(year, month, day).strftime(Config.DATE_FORMAT)
        except (ValueError, IndexError):
            return None

    @staticmethod
    def clean_people_count(people_text: str or int) -> Optional[int]:
        if not people_text:
            return None

        if isinstance(people_text, int):
            return people_text    
        
        cleaned_text = TextCleaner.clean_vietnamese_numbers(people_text)
        match = re.search(r'\d+', cleaned_text)
        print(f"Cleaned people count: {int(match.group()) if match else None}")
        return int(match.group()) if match else None

    @staticmethod
    def clean_budget(budget_text: str or float) -> Optional[float]:
        if not budget_text:
            return None

        if isinstance(budget_text, float):
            return budget_text

        budget_text = budget_text.lower()
        amount_match = re.search(r'\d+(\.\d+)?', budget_text)
        if not amount_match:
            return None
            
        amount = float(amount_match.group().replace(',',''))
        
        for unit, multiplier in NUMBERS["budget_multipliers"].items():
            if unit in budget_text:
                amount *= multiplier
                print(f"Cleaned budget 1: {amount}")
                return amount
        
        print(f"Cleaned budget 2: {amount}")
        return amount


    @staticmethod
    def clean_duration(duration_text: str or int) -> Optional[int]:
        if not duration_text:
            return None

        if isinstance(duration_text, int):
            return duration_text

        duration = TextCleaner.clean_vietnamese_numbers(duration_text.lower()) 
        
        patterns = {
            r'(\d+)\s*ngày\s*(\d+)\s*đêm': lambda x: int(x.group(1)),
            r'(\d+)\s*ngày(?!\s*\d+\s*đêm)': lambda x: int(x.group(1)),
            r'(\d+)\s*tuần': lambda x: int(x.group(1)) * 7,
            r'(\d+)\s*tháng': lambda x: int(x.group(1)) * 30
        }
        
        for pattern, converter in patterns.items():
            match = re.search(pattern, duration)
            if match:
                print(f"Cleaned duration: {converter(match)}")
                return converter(match)
        return None
    
    