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
from datetime import datetime
from actions import DatabaseConnection
import re

ai_server = os.getenv('AI_SERVER')


class ValidateCustomerForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_customer_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate name 
        dispatcher.utter_message(text="Xác nhận tên của bạn là " + slot_value)
        return {"name": slot_value}
    
    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate phone number format
        if not slot_value.isdigit() or len(slot_value) != 10:
            dispatcher.utter_message(text="Số điện thoại không hợp lệ. Vui lòng nhập 10 chữ số.")
            return {"phone_number": None}
        dispatcher.utter_message(text="Xác nhận số điện thoại " + slot_value)
        return {"phone_number": slot_value}
    
    def validate_departure_point(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate departure point format
        dispatcher.utter_message(text= " Xác nhận điểm xuất phát " + slot_value)
        return {"departure_point": slot_value}
    
    def validate_departure_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate departure time format
        dispatcher.utter_message(text= " Xác nhận giờ xuất phát " + slot_value)
        return {"departure_time": slot_value}

class ActionShowTours(Action):

    def name(self):
        return "action_show_tours"

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

class ValidateTourForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_tour_form"

    def validate_destination(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # validate destination
        dispatcher.utter_message(text="Xác nhận điểm đến " + slot_value)
        return {"destination": slot_value}

    def validate_tour_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # validate tour type
        tour_type = tracker.get_slot("tour_type")
        valid_tour_types = ["individual", "family", "group"]
        if tour_type not in valid_tour_types:
            dispatcher.utter_message(text=f"Giá trị '{tour_type}' không hợp lệ. Vui lòng chọn giữa 'cá nhân', 'nhóm' hoặc 'gia đình'.")
            return {"tour_type": None} 
        else:
            dispatcher.utter_message(text=f"Bạn đã chọn tour loại '{tour_type}'.")
        return {"tour_type": slot_value}

    def validate_number_of_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate number of people
        total_people = tracker.get_slot("number_of_people") or 0
        if total_people == 0:
            number_of_adult = tracker.get_slot("number_of_adult") or 0
            number_of_children = tracker.get_slot("number_of_children") or 0

        # Tính tổng số người
            total_people = number_of_adult + number_of_children

        dispatcher.utter_message(text="Xác nhận số người tham gia " + total_people)
        # Cập nhật slot
        return {"number_of_people": total_people}
    
    def validate_budget(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate budget
        dispatcher.utter_message(text="Xác nhận ngân sách " + slot_value)
        return {"budget": slot_value}
    
    def validate_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate duration
        dispatcher.utter_message(text="Xác nhận thời gian tour này " + slot_value)
        return {"duration": slot_value}