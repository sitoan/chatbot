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

from actions import DatabaseConnection

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