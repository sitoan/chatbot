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

ai_server = os.getenv('AI_SERVER')
be_server = os.getenv('BE_SERVER')


class ActionCleanSlots(Action):
    def name(self) -> Text:
        return "action_clean_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        departure_point = tracker.get_slot("departure_point")
        destination = tracker.get_slot("destination")
        number_of_people = tracker.get_slot("number_of_people")
        departure_date = tracker.get_slot("departure_date")
        budget = tracker.get_slot("budget")
        duration = tracker.get_slot("duration")

        if departure_point:
            departure_point = None
        if destination:
            destination = None
        if number_of_people:
            number_of_people = None
        if departure_date:
            departure_date = None
        if budget:
            budget = None
        if duration:
            duration = None

        return []
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
        duration: Optional[int] = None,
        price: Optional[float] = None,
        available_slot: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        try:
            # Parse tours data from JSON string if needed
            if isinstance(tours_data, str):
                suitable_tours = json.loads(tours_data)
            else:
                suitable_tours = tours_data

            print(f"base: {suitable_tours}")

            # Filter by departure location if specified
            if departure:
                suitable_tours = [
                    tour for tour in suitable_tours 
                    if tour["departureLocation"].lower().strip() == departure.lower().strip()
                ]
            
            print(f"filter departureLocation: {suitable_tours}")
            
            # Filter by destination (city or country) if specified
            if destination:
                destination = destination.lower().strip()
                suitable_tours = [
                    tour for tour in suitable_tours 
                    if destination in tour["city"].lower().strip() or 
                       destination in tour["country"].lower().strip()
                ]
            
            print(f"filter destination: {suitable_tours}")

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
            
            print(suitable_tours)


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

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            # Get tour data from backend server
            response = requests.get(f"{be_server}")
            response.raise_for_status()
            tours_data = response.content.decode('utf-8')

            # Get slots from tracker
            slots = {
                "departure": tracker.get_slot("departure_point"),
                "destination": tracker.get_slot("destination"),
                "start_date": tracker.get_slot("departure_date"),
                "duration": tracker.get_slot("duration"),
                "price": tracker.get_slot("budget"),
                "available_slot": tracker.get_slot("number_of_people")
            }

            # Remove None values from slots
            slots = {k: v for k, v in slots.items() if v is not None}

            # Filter tours based on criteria
            suitable_tours = self.filter_tours(tours_data=tours_data, **slots)
            
            print(suitable_tours)

            if not suitable_tours:
                dispatcher.utter_message(text="Xin lỗi, không tìm thấy tour phù hợp với yêu cầu của bạn.")
                return []

            # Prepare prompt for AI server
            prompt = '''
            Dựa vào dữ liệu trên, hãy đưa ra các thông tin cơ bản về tour theo định dạng sau:

            Tour {id} - {city}:
            * Điểm khởi hành: {departureLocation}
            * Điểm đến: {city}, {country}
            * Thời gian: {startDate} - {endDate} ({days} ngày)
            * Giá tour: {price:,.0f} VND
            * Số chỗ còn trống: {availableSlots}
            '''

            # Send request to AI server
            ai_response = requests.post(
                f"{ai_server}/post",
                json={
                    "data": str(suitable_tours),
                    "prompt": prompt
                }
            )
            ai_response.raise_for_status()

            # Send response to user
            dispatcher.utter_message(text=f"một số tour gợi ý dựa theo yêu cầu của bạn: \n {ai_response.content.decode('utf-8')}")
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
class ValidateTourForm(FormValidationAction):
    
    PEOPLE_PATTERN = r"\b([0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(người|khách)?\b"
    BUDGET_PATTERN = r"\b\d+(\.\d+)?\s*(triệu|nghìn|đ|vnđ|usd|k|m|b)\b"
    DATE_PATTERN = r"\b\d{1,2}[/-]\d{1,2}([/-]\d{4})?\b"

    DURATION_PATTERN = r"""(?x)
    (?:
        # Match X ngày Y đêm pattern
        \b(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*ngày\s*
        (?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*đêm
    )|
    (?:
        # Match simple duration pattern
        \b(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*
        (?:ngày|tuần|tháng|năm)
    )
"""    
    # Vietnamese number mapping
    VN_NUMBERS = {
        'một': '1', 'hai': '2', 'ba': '3', 'bốn': '4', 'năm': '5',
        'sáu': '6', 'bảy': '7', 'tám': '8', 'chín': '9', 'mười': '10'
    }
    def name(self) -> Text:
        return "validate_tour_form"
    
    def validate_departure_point(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate departure point format
        
        print(f"departure: {slot_value} ")
        print(type(slot_value))

        dispatcher.utter_message(text= " Xác nhận điểm xuất phát " + slot_value)
        return {"departure_point": slot_value, }
    
    def validate_departure_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate departure time format

        if not slot_value:
            dispatcher.utter_message(text="Vui lòng cho biết ngày khởi hành.")
            return {"departure_date": None}
        
        if not re.match(self.DATE_PATTERN, slot_value):
            dispatcher.utter_message(
                text="Ngày không hợp lệ. Vui lòng nhập theo định dạng: DD/MM hoặc DD/MM/YYYY."
            )
            return {"departure_date": None}
        
        # Chuẩn hóa ngày
        parts = re.split(r'[/-]', slot_value)
        day = int(parts[0])
        month = int(parts[1])  if len(parts) > 1 else datetime.now().month # Mặc định tháng hiện tại
        year = int(parts[2]) if len(parts) > 2 else datetime.now().year  # Mặc định năm hiện tại
        
        # Kiểm tra tính hợp lệ của ngày
        if not (1 <= month <= 12 and 1 <= day <= 31):
            dispatcher.utter_message(text="Ngày tháng không hợp lệ.")
            return {"departure_date": None}
        
        date = f"{day:02d}-{month:02d}-{year}"

        dispatcher.utter_message(text= f" Xác nhận ngày xuất phát {date}")
        print(f"departure_date: {date}")
        print(type(date))
        
        return {"departure_date": date}
        

    def validate_destination(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # validate destination
        dispatcher.utter_message(text="Xác nhận điểm đến " + slot_value)
        print(f"destination: {slot_value}")
        print(type(slot_value))
        return {"destination": slot_value}

    def validate_number_of_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate number of people
        
        if not slot_value:
            dispatcher.utter_message(text="Vui lòng cho biết số người tham gia.")
            return {"number_of_people": None}
        
        if not re.match(self.PEOPLE_PATTERN, slot_value.lower()):
            dispatcher.utter_message(
                text="Số người không hợp lệ. Vui lòng nhập theo định dạng: số + người/khách (VD: 2 người, ba khách)."
            )
            return {"number_of_people": None}
        
        # Chuẩn hóa số người
        people_text = slot_value.lower()
        for vn_num, num in self.VN_NUMBERS.items():
            if vn_num in people_text:
                return {"number_of_people": num}
                
        # Nếu là số
        num = int(re.search(r'\d+', people_text).group())

        dispatcher.utter_message(text=f"Xác nhận số người tham gia {num}")
        print(f"number_of_people: {num}")
        print(type(num))
        # Cập nhật slot
        return {"number_of_people": num}
    
    def validate_budget(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate budget

        if not slot_value:
            dispatcher.utter_message(text="Vui lòng cho biết ngân sách của bạn.")
            return {"budget": None}
        
        if not re.match(self.BUDGET_PATTERN, slot_value.lower()):
            dispatcher.utter_message(
                text="Ngân sách không hợp lệ. Vui lòng nhập theo định dạng: số + đơn vị (VD: 5 triệu, 500k, 2m)."
            )
            return {"budget": None}
        
        # Chuẩn hóa budget  
        budget_text = slot_value.lower()
        amount = float(re.search(r'\d+(\.\d+)?', budget_text).group())
        
        # Chuyển đổi các đơn vị về VNĐ
        if 'k' in budget_text:
            amount *= 1000
        elif 'm' in budget_text or 'triệu' in budget_text or 'tr' in budget_text:
            amount *= 1000000
        elif 'b' in budget_text or 'tỷ' in budget_text:
            amount *= 1000000000
        print(f"budget: {amount}")
        print(type(amount))
        dispatcher.utter_message(text=f"Xác nhận ngân sách {amount} VND")
        return {"budget": amount}
    
    def _normalize_duration(self, duration_text: str) -> str:


        # Loại bỏ các từ khóa phụ
        duration = duration_text.lower()
        for prefix in ['kéo dài', 'khoảng', 'trong']:
            duration = duration.replace(prefix, '').strip()

        # Chuyển đổi số từ chữ sang số
        for vn_num, num in self.VN_NUMBERS.items():
            duration = duration.replace(vn_num, num)
            
    # Pattern cho các format khác nhau
        patterns = [
            # X ngày Y đêm
            r'(\d+)\s*ngày\s*(\d+)\s*đêm',
            # X ngày
            r'(\d+)\s*ngày(?!\s*\d+\s*đêm)',  
            # X tuần
            r'(\d+)\s*tuần',
            # X tháng
            r'(\d+)\s*tháng'
        ]
        
        for pattern in patterns:
            match = re.search(pattern,  duration)
            if match:
                if len(match.groups()) == 2:  # X ngày Y đêm
                    days, nights = match.groups()
                    return f"{days} ngày {nights} đêm"
                elif pattern == r'(\d+)\s*ngày(?!\s*\d+\s*đêm)':
                    days = match.group(1)
                    return f"{days} ngày"
                elif 'tuần' in pattern:
                    weeks = int(match.group(1))
                    days = weeks * 7
                    return f"{days} ngày"
                elif 'tháng' in pattern:
                    months = int(match.group(1))
                    days = months * 30
                    return f"{days} ngày"

        return duration
        
    def validate_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate duration
        if not slot_value:
            dispatcher.utter_message(text="Vui lòng cho biết thời gian chuyến đi của bạn.")
            return {"duration": None}

        # Kiểm tra định dạng bằng regex
        duration_text = slot_value.strip().lower()
        if not re.findall(self.DURATION_PATTERN, duration_text):
            dispatcher.utter_message(
                text="Thời gian không hợp lệ. Vui lòng nhập theo một trong các định dạng sau:\n"
                "- X ngày (VD: 3 ngày)\n"
                "- X ngày Y đêm (VD: 3 ngày 2 đêm)\n"
                "- X tuần/tháng (VD: 2 tuần, 1 tháng)"
            )
            return {"duration": None}

        # Chuẩn hóa duration
        normalized_duration = self._normalize_duration(duration_text)

       # Extract số ngày
        days = 0
        day_match = re.search(r'(\d+)\s*ngày', normalized_duration)
        if day_match:
            days = int(day_match.group(1))
        
        if days < 1 or days > 90:
            dispatcher.utter_message(text="Thời gian tour phải từ 1 đến 90 ngày.")
            return {"duration": None}
        
        dispatcher.utter_message(text="Xác nhận thời gian tour này " + normalized_duration)
        print(f"normalized_duration: {normalized_duration}")
        print(type(normalized_duration))
        print(f"days: {days}")
        print(type(days))

        return {"duration": days}


