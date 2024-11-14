from dataclasses import dataclass
from typing import Dict, Optional, Text, List, Any, Union
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
import re

ai_server =os.getenv('AI_SERVER')
be_server =os.getenv('BE_SERVER')


VN_NUMBERS = {
        'một': '1', 'hai': '2', 'ba': '3', 'bốn': '4', 'năm': '5',
        'sáu': '6', 'bảy': '7', 'tám': '8', 'chín': '9', 'mười': '10'
    }
    
BUDGET_MULTIPLIERS = {
    'k': 1000,
    'm': 1000000,
    'triệu': 1000000,
    'tr': 1000000,
    'tỷ': 1000000000
}

def clean_vietnamese_numbers( text: str) -> str:
    """Convert Vietnamese number words to digits."""
    result = text.lower()
    for vn_num, num in VN_NUMBERS.items():
        result = result.replace(vn_num, num)
    return result

def clean_date(date_text: str) -> Optional[str]:
    """Clean and validate date string."""
    parts = re.split(r'[/-]', date_text)
    current_date = datetime.now()
    
    try:
        day = int(parts[0])
        month = int(parts[1]) if len(parts) > 1 else current_date.month
        year = int(parts[2]) if len(parts) > 2 else current_date.year
        
        formatted_date = datetime(year, month, day)
        print(f"{formatted_date} : {type(formatted_date)}")
        return formatted_date.strftime("%d-%m-%Y")
        
    except ValueError:
        return None

def clean_people_count(people_text: str) -> Optional[int]:
    """Clean and convert people count to integer."""
    if not people_text:
        return None
        
    cleaned_text = clean_vietnamese_numbers(people_text)
    match = re.search(r'\d+', cleaned_text)
    print(f"{match.group()} : {type(match.group())}")
    return int(match.group()) if match else None

def clean_budget(budget_text: str) -> Optional[float]:
    """Clean and normalize budget to VND."""
    if not budget_text:
        return None
        
    budget_text = budget_text.lower()
    amount_match = re.search(r'\d+(\.\d+)?', budget_text)
    if not amount_match:
        return None
        
    amount = float(amount_match.group())
    
    for unit, multiplier in BUDGET_MULTIPLIERS.items():
        if unit in budget_text:
            print(f"{amount * multiplier} : {type(amount * multiplier)}")
            return amount * multiplier

    print(f"{amount} : {type(amount)}")
    return amount

def clean_duration(duration_text: str) -> Optional[int]:
    """Clean and normalize duration to number of days."""
    if not duration_text:
        return None

    duration = duration_text.lower()
    # Remove prefix words
    prefixes = ['kéo dài', 'khoảng', 'trong']
    for prefix in prefixes:
        duration = duration.replace(prefix, '').strip()

    duration = clean_vietnamese_numbers(duration)
        
    # Convert different formats to days
    patterns = {
        r'(\d+)\s*ngày\s*(\d+)\s*đêm': lambda x: int(x.group(1)),
        r'(\d+)\s*ngày(?!\s*\d+\s*đêm)': lambda x: int(x.group(1)),
        r'(\d+)\s*tuần': lambda x: int(x.group(1)) * 7,
        r'(\d+)\s*tháng': lambda x: int(x.group(1)) * 30
    }
    
    for pattern, converter in patterns.items():
        match = re.search(pattern, duration)
        if match:
            print(f"{converter(match)} : {type(converter(match))}")
            return converter(match)

    return None

class ActionClearSlots(Action):
    def name(self) -> Text:
        return "action_clear_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        departure_point = tracker.get_slot("departure_point")
        destination = tracker.get_slot("destination")
        number_of_people = tracker.get_slot("number_of_people")
        departure_date = tracker.get_slot("departure_date")
        budget = tracker.get_slot("budget")
        duration = tracker.get_slot("duration")

        print(f"{departure_point} : {type(departure_point)}")
        print(f"{destination} : {type(destination)}")
        print(f"{number_of_people} : {type(number_of_people)}")
        print(f"{departure_date} : {type(departure_date)}")
        print(f"{budget} : {type(budget)}")
        print(f"{duration} : {type(duration)}")


        events = []

        if departure_point is not None:
            events.append(SlotSet("departure_point", None))
        if destination is not None:
            events.append(SlotSet("destination", None))
        if number_of_people is not None:
            events.append(SlotSet("number_of_people", None))
        if departure_date is not None:
            events.append(SlotSet("departure_date", None))
        if budget is not None:
            events.append(SlotSet("budget", None))
        if duration is not None:
            events.append(SlotSet("duration", None))

        return events
class ValidateCustomerForm(FormValidationAction):

    PHONE_PATTERN = r"(0|\+84)[-.]?(3|5|7|8|9)[-.]?[0-9]{3}[-.]?[0-9]{4}[-.]?[0-9]{3}"

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
        if not re.match(self.PHONE_PATTERN, slot_value):
            dispatcher.utter_message(
                text="Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại di động Việt Nam (VD: 0912345678)."
            )
            return {"phone_number": None}
        
        # Chuẩn hóa số điện thoại
        clean_phone = re.sub(r'[-.]', '', slot_value)
        if clean_phone.startswith('+84'):
            clean_phone = '0' + clean_phone[3:]
        
        dispatcher.utter_message(text="Xác nhận số điện thoại của bạn là " + clean_phone)
        return {"phone_number": clean_phone}

class ActionShowTours(Action):
    def name(self) -> Text:
        return "action_show_tours"

    @staticmethod
    def filter_tours(
        tours_data: Union[str, List[Dict[str, Any]]],
        departure: Optional[str] = None,
        destination: Optional[str] = None,
        start_date: Optional[str] = None,
        duration: Optional[Union[str, int]] = None,
        price: Optional[Union[str, float]] = None,
        available_slot: Optional[Union[str, int]] = None,
        intent: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        try:
            # Parse tours data from JSON string if needed
            if isinstance(tours_data, str):
                suitable_tours = json.loads(tours_data)
            else:
                suitable_tours = tours_data
            
            print(f"{departure} : {type(departure)}")
            print(f"{destination} : {type(destination)}")
            print(f"{start_date} : {type(start_date)}")
            print(f"{duration} : {type(duration)}")
            print(f"{price} : {type(price)}")
            print(f"{available_slot} : {type(available_slot)}")



            if intent == "find_tour":
                if isinstance(start_date, str):
                    start_date = clean_date(start_date)
                if isinstance(duration, str):
                    duration = clean_duration(duration)
                if isinstance(price, str):
                    price = clean_budget(price)
                if isinstance(available_slot, str):
                    available_slot = clean_people_count(available_slot)

            
            print(f"{departure} : {type(departure)}")
            print(f"{destination} : {type(destination)}")
            print(f"{start_date} : {type(start_date)}")
            print(f"{duration} : {type(duration)}")
            print(f"{price} : {type(price)}")
            print(f"{available_slot} : {type(available_slot)}")
            

            print(f"base: {suitable_tours}")

            # Filter by departure location if specified
            if departure and isinstance(departure, str):
                departure = departure.lower().strip()
                suitable_tours = [
                    tour for tour in suitable_tours 
                    if departure in tour["departureLocation"].lower().strip() 
                ]
            
            print(suitable_tours)
            print(f"filter departureLocation: {suitable_tours}")
            
            # Filter by destination (city or country) if specified
            if destination and isinstance(destination, str):
                destination = destination.lower().strip()
                suitable_tours = [
                    tour for tour in suitable_tours 
                    if destination in tour["city"].lower().strip() or 
                       destination in tour["country"].lower().strip()
                ]
            
            print(f"filter destination: {suitable_tours}")
            print(suitable_tours)

            # Filter by start date if specified
            if start_date:
                try:
                    start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
                    
                    suitable_tours = [
                        tour for tour in suitable_tours 
                        if datetime.strptime(tour["startDate"], "%d-%m-%y") >= start_date_obj
                    ]
                except ValueError as e:
                    print(f"Invalid date format: {start_date}. Error: {str(e)}")
            


            # Filter by duration if specified
            if duration:
                try:
                    duration = int(duration)
                    suitable_tours = [
                        tour for tour in suitable_tours 
                        if int(tour["days"]) <= duration
                    ]
                except ValueError as e:
                    print(f"Invalid duration format: {duration}. Error: {str(e)}")
            
            print(f"filter duration: {suitable_tours}")

            # Filter by price if specified
            if price:
                try:
                    suitable_tours = [
                        tour for tour in suitable_tours 
                        if float(tour["price"]) <= price
                    ]
                except ValueError as e:
                    print(f"Invalid price format: {price}. Error: {str(e)}")

            print(f"filter price: {suitable_tours}")

            # Filter by available slots if specified
            if available_slot:
                try:
                    available_slot = int(available_slot)
                    suitable_tours = [
                        tour for tour in suitable_tours 
                        if int(tour["availableSlots"]) >= available_slot
                    ]
                except ValueError as e:
                    print(f"Invalid available slots format: {available_slot}. Error: {str(e)}")
        
            print(f"filter slots: {suitable_tours}")

            # Sort results by start date and price
            suitable_tours.sort(key=lambda x: (
                datetime.strptime(x["startDate"], "%d-%m-%y"),
                float(x["price"])
            ))

            print(f"filter result: {suitable_tours}")

            return suitable_tours

        except json.JSONDecodeError as e:
            print(f"Invalid JSON data format. Error: {str(e)}")
            return []
        except Exception as e:
            print(f"Error filtering tours: {str(e)}")
            return []

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            # Get tour data from backend server
            response = requests.get(f"{be_server}/getallforai")
            response.raise_for_status()
            tours_data = response.content.decode('utf-8')

            slots = {
                "departure": tracker.get_slot("departure_point"),
                "destination": tracker.get_slot("destination"),
                "start_date": tracker.get_slot("departure_date"),
                "duration": tracker.get_slot("duration"),
                "price": tracker.get_slot("budget"),
                "available_slot": tracker.get_slot("number_of_people")
            }

            intent = tracker.latest_message.get("intent").get("name")

            # Remove None values from slots                    
            slots = {k: v for k, v in slots.items() if v is not None}
            print(slots)
            # Filter tours based on criteria
            suitable_tours = self.filter_tours(
                tours_data=tours_data, 
                departure=slots.get("departure"),
                destination=slots.get("destination"),
                start_date=slots.get("start_date"),
                duration=slots.get("duration"),
                price=slots.get("price"),
                available_slot=slots.get("available_slot"), 
                intent=intent
                )
            
            print(type(suitable_tours), suitable_tours)

            if not suitable_tours:
                dispatcher.utter_message(text="Xin lỗi, không tìm thấy tour phù hợp với yêu cầu của bạn.")
                return []

            dispatcher.utter_message(text=f"một số tour gợi ý dựa theo yêu cầu của bạn {', '.join(str(v) for v in slots.values())}:")

            for tour in suitable_tours:
                dispatcher.utter_message(text=
f'''
Tour {tour['id']} - {tour['city']}:
* Điểm khởi hành: {tour['departureLocation']}
* Điểm đến: {tour['city']}, {tour['country']}
* Thời gian: {tour['startDate']} - {tour['endDate']} ({tour['duration']} ngày)
* Giá tour: {tour['price']:,.0f} VND
* Số chổ còn trống: {tour['availableSlots']}
''')
                dispatcher.utter_message(text=f"{tour['id']}")

            return []
        
        except requests.RequestException as e:
            error_message = f"Lỗi kết nối với server: {str(e)}"
            print(error_message)
            dispatcher.utter_message(text="Xin lỗi, không thể lấy thông tin tour lúc này. Vui lòng thử lại sau.")
            return []
        
        except Exception as e:
            error_message = f"Lỗi không xác định: {str(e)}"
            print(error_message)
            dispatcher.utter_message(text="Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn.")
            return []

@dataclass
class ValidationPatterns:
    """Constants for validation patterns."""
    PEOPLE = r"""(?ix)\b(?:(?:[0-9]|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:người|khách))\b"""
    BUDGET = r"""(?ix)
        \b
        (?:
            \d+(?:\.\d+)?     # Number part
            \s*               # Optional space
            (?:              # Units
                k|triệu|tr|tỷ|nghìn|đ|vnđ|usd|vnd
                |
                (?:đồng|dollars?)?  # Optional currency words
            )?
        )
        \b
    """
    DATE = r"""(?ix)(?:(?:tháng\s+(?:1[0-2]|[1-9]))|(?:(?:[0-2]?[0-9]|3[01])[/-](?:1[0-2]|[1-9])(?:[/-](?:19|20)\d{2})?))"""
    DURATION = r"""(?ix)\b(?:(?:(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*ngày\s*(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*đêm)|(?:(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:ngày|tuần|tháng|năm)))\b"""


class ValidateTourForm(FormValidationAction):
    """Form validation action for tour booking."""
    
    def __init__(self):
        self.patterns = ValidationPatterns()
        
    def name(self) -> Text:
        return "validate_tour_form"

    def _confirm_and_return(self, slot_name: str, value: Any, 
                           dispatcher: CollectingDispatcher) -> Dict[Text, Any]:
        if not value:
            dispatcher.utter_message(text=f"Vui lòng cho biết {slot_name}.")
        
            return {slot_name: None}
        response_text = {
            "departure_point": "điểm xuất phát",
            "destination": "điểm đến",
            "departure_date": "ngày xuất phát",
            "duration": "thời gian chuyến đi",
            "budget": "giá tour",
            "number_of_people": "số khách"
        }
        dispatcher.utter_message(text=f"Xác nhận {response_text[slot_name]}: {value}")
        print(slot_name)
        print(f"{value} : {type(value)}")
        return {slot_name: value}

    def validate_departure_point(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        return self._confirm_and_return("departure_point", slot_value, dispatcher)

    def validate_departure_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not re.match(self.patterns.DATE, slot_value):
            dispatcher.utter_message(
                text="Ngày không hợp lệ. Vui lòng cho biết thời điểm xuất phát."
            )
            return {"departure_date": None}
        
        cleaned_date = clean_date(slot_value)
        print(slot_value +" : "+ cleaned_date)
        if not cleaned_date:
            dispatcher.utter_message(text="Ngày tháng không hợp lệ.")
            return {"departure_date": None}
            
        return self._confirm_and_return("departure_date", cleaned_date, dispatcher)

    def validate_destination(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        return self._confirm_and_return("destination", slot_value, dispatcher)

    def validate_number_of_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if not re.match(self.patterns.PEOPLE, slot_value.lower()):
            dispatcher.utter_message(
                text="Số người không hợp lệ. Vui lòng nhập theo định dạng: số + người/khách (VD: 2 người, ba khách)."
            )
            return {"number_of_people": None}
        
        num_people = clean_people_count(slot_value)
        if not num_people:
            dispatcher.utter_message(text="Số người không hợp lệ.")
            return {"number_of_people": None}
        
        return self._confirm_and_return("number_of_people", num_people, dispatcher)

    def validate_budget(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if not re.match(self.patterns.BUDGET, slot_value.lower()):
            dispatcher.utter_message(
                text="Ngân sách không hợp lệ. Vui lòng nhập theo định dạng: số + đơn vị (VD: 5 triệu, 500k, 2m)."
            )
            return {"budget": None}
        
        amount = clean_budget(slot_value)
        if not amount:
            dispatcher.utter_message(text="Ngân sách không hợp lệ.")
            return {"budget": None}
        print(f"{amount:,.0f} :")
        return self._confirm_and_return("budget", f'{amount:,.0f}', dispatcher)

    def validate_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if not re.findall(self.patterns.DURATION, slot_value.lower()):
            dispatcher.utter_message(
                text="Thời gian không hợp lệ. Vui lòng nhập theo một trong các định dạng sau:\n"
                "- X ngày (VD: 3 ngày)\n"
                "- X ngày Y đêm (VD: 3 ngày 2 đêm)\n"
                "- X tuần/tháng (VD: 2 tuần, 1 tháng)"
            )
            return {"duration": None}

        days = clean_duration(slot_value)
        if not days or not 1 <= days <= 90:
            dispatcher.utter_message(text="Thời gian tour phải từ 1 đến 90 ngày.")
            return {"duration": None}
        
        return self._confirm_and_return("duration", f"{days} ngày", dispatcher)
    

class ActionShowPlan(Action):
    def name(self) -> Text:
        return "action_answer_tour"
    
    def run(self, dispatcher, tracker, domain) -> Dict[Text, Any]:
        tour_number = tracker.get_slot("tour_number")
        if tour_number is None:
            dispatcher.utter_message(text="Vui lòng chọn số hiệu của tour.")
            return {"tour_number": None}
        
        user_question = tracker.latest_message.get("text")
        response = requests.get(f"{be_server}/{tour_number}")
        response.raise_for_status()
        tours_data = response.content.decode('utf-8')
        print(f"{user_question}")
    # Prepare prompt for AI server
        prompt = f'''
        Bạn trong vai trò 1 nhân viên tư vấn tour du lịch, dựa vào tour bên trên hãy giải đáp các thắc mắc một cách tự nhiên, thoải mái, chi tiết từng mốc thời gian và cung cấp thêm các thông tin về các địa điểm tham quan để lôi cuốn khách hàng nhưng các thông tin đưa ra phải đảm bảo độ chính xác.
        thắc mắc của user: {user_question}
        '''

        # Send request to AI server
        ai_response = requests.post(
            f"{ai_server}/post",
            json={
                "data": str(tours_data),
                "prompt": prompt
            }
        )
        ai_response.raise_for_status()

        dispatcher.utter_message(text=ai_response.content.decode('utf-8'))
        return {}