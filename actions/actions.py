from typing import Dict, Text, List, Any
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
import requests
import json 
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime,timedelta
from actions import DatabaseConnection
import re
from dateutil.relativedelta import relativedelta  

ai_server = os.getenv('AI_SERVER')

class ValidateInformationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_information_form"
    
    def validate_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"Ghi nhận tên là {slot_value}")
        return {"name": slot_value}

    def validate_phonenumb(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"Ghi nhận sđt là {slot_value}")
        return {"phonenumb": slot_value}
    
    def validate_starpos(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"Ghi nhận điểm khỏi hành là {slot_value}")
        return {"starpos": slot_value}

class ActionAskTours(Action):

    def name(self):
        return "action_ask_tours"

    def run(self, dispatcher : CollectingDispatcher, tracker, domain) -> list:
        db = DatabaseConnection()
        tours = db.execute_query("SELECT DepartureLocation, StartDate, EndDate, PRICE, AvailableSlots FROM Tour")
        prompt = '''
        Dựa vào mảng trên, hãy nói bằng tiếng việt chứ không phải dữ liệu, ví dụ như :
        - Tour Thành phố Hồ Chí Minh:
    * Điểm đến là Thành phố Hồ Chí Minh.
    * Khởi hành lúc 8 giờ sáng ngày 1 tháng 11 năm 2024.
    * Kết thúc lúc 8 giờ tối ngày 6 tháng 11 năm 2024.
    * Giá tour là 2200.0 (chưa rõ đơn vị tiền tệ).
    * Chuyến đi kéo dài 5 ngày. 
        '''
        data = {
            "data": str(tours),
            "prompt": prompt
        }
        res = requests.post(f"{ai_server}/post", json=data)
        print(res.content.decode('utf-8'))
        dispatcher.utter_message(text=f"{res.content.decode('utf-8')}")
        return [] 
    
class ActionSessionStart(Action):
    def name(self) -> str:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        dispatcher.utter_message(text="Xin chào! Chào mừng bạn đến với dịch vụ tour du lịch của chúng tôi. Bạn muốn tìm hiểu tour nào?")

        return []
    
class ActionSaveAvailableDate(Action):
    def name(self) -> str:
        return "action_save_available_date"

    def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        message = tracker.latest_message['text']
        today = datetime.now()

        date_pattern = r'(\d{1,2})\s+tháng\s+(\d{1,2})(?:\s+năm\s+(\d{4}))?'
        match = re.search(date_pattern, message)

        day, month, year = None, None, None

        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3)) if match.group(3) else today.year
        else:
            month_pattern = r'tháng\s+(\d{1,2})'
            month_match = re.search(month_pattern, message)
            if month_match:
                month = int(month_match.group(1))
                day = today.day + 1  # Ngày hiện tại cộng thêm 1
                year = today.year  # Năm hiện tại

            day_pattern = r'(\d{1,2})'
            day_match = re.search(day_pattern, message)
            if day_match and month is None:
                day = int(day_match.group(1))
                month = today.month  # Tháng hiện tại
                year = today.year    # Năm hiện tại

        if day is None and month is None:
            dispatcher.utter_message(text="Xin lỗi, bạn cần cung cấp ngày hoặc tháng.")
            return [SlotSet("valid_date", "false")]

        if month is not None and day is None:
            day = today.day + 1  

        try:
            available_date = datetime(year, month, day)
            if available_date < today:
                dispatcher.utter_message(text="Ngày bạn chọn phải lớn hơn ngày hiện tại.")
                return [SlotSet("valid_date", "false")]

            available_date_str = f"{year}-{month:02d}-{day:02d}"
            print(f"Available Date: {available_date_str}")
            return [SlotSet("available_date", available_date_str), SlotSet("valid_date", "true")]
        except ValueError:
            dispatcher.utter_message(text="Ngày bạn nhập không hợp lệ.")
            return [SlotSet("valid_date", "false")]

class ActionConfirmDate(Action):
    def name(self) -> str:
        return "action_confirm_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        if tracker.get_slot("valid_date") == "false":
            dispatcher.utter_message(text="Vui lòng nhập một ngày hợp lệ trước khi xác nhận.")
            return [] 

        available_date = tracker.get_slot("available_date")
        print(f"Ngày khởi hành bạn đã chọn là: {available_date}.")
        dispatcher.utter_message(text=f"Ngày khởi hành bạn đã chọn là: {available_date}.")
        
        return []

class ActionShowTourTimes(Action):
    def name(self) -> str:
        return "action_show_tour_times"

    def __init__(self):
        self.db = DatabaseConnection()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        available_date = tracker.get_slot("available_date")
        
        if available_date:
            available_date = datetime.strptime(available_date, "%Y-%m-%d")
            query = f"""
            SELECT * FROM Tour
            WHERE StartDate > '{available_date.strftime('%Y-%m-%d %H:%M:%S')}'
            """
            results = self.db.execute_query(query)
            if results:
                response = "Các tour có sẵn vào thời gian bạn yêu cầu:\n"
                for row in results:
                    response += (
                        f"🔹 **Điểm đến**: {row.DepartureLocation}\n"
                        f"🔹 **Thời gian**: {row.StartDate} - {row.EndDate}\n"
                        f"🔹 **Giá**: {row.PRICE:.2f} VND\n"
                        f"🔹 **Số lượng còn lại**: {row.AvailableSlots}\n"
                        f"-------------------------\n"  
                    )
                dispatcher.utter_message(text=response)  
            else:
                dispatcher.utter_message(text="Xin lỗi, không có tour nào có sẵn trong khoảng thời gian này.")
        else:
            dispatcher.utter_message(text="Xin lỗi, tôi không tìm thấy thông tin ngày bạn đã cung cấp.")
        
        return []
    
class ActionShowRecentTours(Action):
    def name(self) -> str:
        return "action_show_recent_tours"

    def __init__(self):
        self.db = DatabaseConnection()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        today = datetime.now()
        two_months_from_now = today + relativedelta(months=2)  # Lấy ngày hiện tại cộng thêm 2 tháng

        query = f"""
        SELECT * FROM Tour
        WHERE StartDate BETWEEN '{today.strftime('%Y-%m-%d %H:%M:%S')}' 
                             AND '{two_months_from_now.strftime('%Y-%m-%d %H:%M:%S')}'
        """
        results = self.db.execute_query(query)

        if results:
            response = "Các tour có sẵn trong 2 tháng tới:\n"
            for row in results:
                response += (
                    f"🔹 **Điểm đến**: {row.DepartureLocation}\n"
                    f"🔹 **Thời gian**: {row.StartDate.strftime('%Y-%m-%d %H:%M:%S')} - {row.EndDate.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🔹 **Giá**: {row.PRICE:.2f} VND\n"
                    f"🔹 **Số lượng còn lại**: {row.AvailableSlots}\n"
                    f"-------------------------\n"
                )
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Không có tour nào trong 2 tháng tới.")
        
        return []
    
class ActionShowToursBySpecificDate(Action):
    def name(self) -> str:
        return "action_show_tours_by_specific_date"

    def __init__(self):
        self.db = DatabaseConnection()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        # Lấy giá trị tháng từ slot và chuyển sang số nguyên
        month = tracker.get_slot("month")
        if month is None:
            dispatcher.utter_message(text="Xin lỗi, bạn cần cung cấp tháng.")
            return []
        
        try:
            month = int(month)  # Chuyển đổi tháng sang số nguyên
        except ValueError:
            dispatcher.utter_message(text="Tháng không hợp lệ.")
            return []

        year = datetime.now().year  # Lấy năm hiện tại
        
        # Xác định ngày bắt đầu và ngày kết thúc của tháng
        start_date = datetime(year, month, 1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        # Xây dựng query để tìm tour trong tháng
        query = f"""
        SELECT * FROM Tour
        WHERE StartDate BETWEEN '{start_date.strftime('%Y-%m-%d')}' 
                             AND '{end_date.strftime('%Y-%m-%d')}'
        """
        results = self.db.execute_query(query)

        if results:
            response = f"Các tour có sẵn trong tháng {month}:\n"
            for row in results:
                response += (
                    f"🔹 **Điểm đến**: {row.DepartureLocation}\n"
                    f"🔹 **Thời gian**: {row.StartDate.strftime('%Y-%m-%d %H:%M:%S')} - {row.EndDate.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🔹 **Giá**: {row.PRICE:.2f} VND\n"
                    f"🔹 **Số lượng còn lại**: {row.AvailableSlots}\n"
                    f"-------------------------\n"
                )
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f"Xin lỗi, không có tour nào có sẵn trong tháng {month}.")
        
        return []