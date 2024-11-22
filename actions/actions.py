
from dataclasses import dataclass
from typing import Dict, Optional, Text, List, Any, Union, TypedDict
from datetime import datetime
from enum import Enum
import re
import json
import os
import requests
from dotenv import load_dotenv
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings."""
    AI_SERVER = os.getenv('AI_SERVER')
    BE_SERVER = os.getenv('BE_SERVER')
    SHORT_DATE_FORMAT = "%d-%m-%Y"

class NumberMapping(TypedDict):
    """Type definition for number mappings."""
    vietnamese: Dict[str, str]
    budget_multipliers: Dict[str, int]

NUMBERS: NumberMapping = {
    "vietnamese": {
        'một': '1', 'hai': '2', 'ba': '3', 'bốn': '4', 'năm': '5',
        'sáu': '6', 'bảy': '7', 'tám': '8', 'chín': '9', 'mười': '10'
    },
    "budget_multipliers": {
        'k': 1000,
        'm': 1000000,
        'triệu': 1000000,
        'tr': 1000000,
        'tỷ': 1000000000
    }
}

class ValidationPatterns:
    """Regex patterns for form validation."""
    PHONE = r"(0|\\+84)[-.]?(3|5|7|8|9)[-.]?[0-9]{3}[-.]?[0-9]{3}[-.]?[0-9]{3}"
    PEOPLE = r"""(?ix)\b(?:(?:\d+(?:\.\d+)?|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:người|khách))\b"""
    BUDGET = r"""(?ix)\b(?:\d+(?:\.\d+)?|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|mươi|trăm|nghìn|triệu|tỷ)\s*(?:k|triệu|tr|tỷ|nghìn|đ|vnđ|usd|vnd|đồng|dollars?)?\b"""
    DATE = r"""(?ix)\b((ngày\s([1-9]|[12][0-9]|3[01])(?:[/-][1-9]|1[0-2])?(?:[/-]\d{4})?)|(tháng\s([1-9]|1[0-2])(?:[/-]\d{4})?)|([0-3]?[0-9][/-][0-1]?[0-9](?:[/-]\d{4})?))\b"""
    DURATION = r"""(?ix)\b(?:(?:(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*ngày\s*(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*đêm)|(?:(?:[0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:ngày|tuần|tháng|năm)))\b"""

@dataclass
class TourData:
    """Data structure for tour information."""
    id: str
    city: str
    country: str
    departureLocation: str
    startDate: str
    endDate: str
    duration: str
    price: float
    availableSlots: int

class TextCleaner:
    """Utility class for cleaning and normalizing text inputs."""
    
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
        """Clean and validate date string."""
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
            year = int(parts[2]) if len(parts) > 2 else current_date.year
            
            print(f"Cleaned date 2: {datetime(year, month, day).strftime(Config.SHORT_DATE_FORMAT)}")
            return datetime(year, month, day).strftime(Config.SHORT_DATE_FORMAT)
        except (ValueError, IndexError):
            return None

    @staticmethod
    def clean_people_count(people_text: str) -> Optional[int]:
        """Clean and convert people count to integer."""
        if not people_text:
            return None
            
        cleaned_text = TextCleaner.clean_vietnamese_numbers(people_text)
        match = re.search(r'\d+', cleaned_text)
        print(f"Cleaned people count: {int(match.group()) if match else None}")
        return int(match.group()) if match else None

    @staticmethod
    def clean_budget(budget_text: str) -> Optional[float]:
        """Clean and normalize budget to VND."""
        if not budget_text:
            return None
            
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
    def clean_duration(duration_text: str) -> Optional[int]:
        """Clean and normalize duration to number of days."""
        if not duration_text:
            return None

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

class TourManager:
    """Manager class for tour-related operations."""
    
    @staticmethod
    def filter_tours(
        tours_data: Union[str, List[Dict[str, Any]]],
        filters: Dict[str, Any],
        action: Optional[str] = None
    ) -> List[TourData]:
        """Filter tours based on given criteria."""
        try:
            suitable_tours = json.loads(tours_data) if isinstance(tours_data, str) else tours_data
            
            if action == "action_listen":
                filters = TourManager._clean_filter_values(filters)
                print(f"Filtered filters: {filters}")
            
            suitable_tours = TourManager._apply_filters(suitable_tours, filters)

            print(f"Overall: {suitable_tours}")
            
            return sorted(
                suitable_tours,
                key=lambda x: (
                    datetime.strptime(x["startDate"], Config.SHORT_DATE_FORMAT),
                    float(x["price"])
                )
            )
        except Exception as e:
            print(f"Error filtering tours: {str(e)}")
            return []

    @staticmethod
    def _clean_filter_values(filters: Dict[str, Any]) -> Dict[str, Any]:
        """Clean filter values before applying them."""
        if filters.get("start_date"):
            filters["start_date"] = TextCleaner.clean_date(filters["start_date"])
        if filters.get("duration"):
            filters["duration"] = TextCleaner.clean_duration(filters["duration"])
        if filters.get("price"):
            filters["price"] = TextCleaner.clean_budget(filters["price"])
        if filters.get("available_slot"):
            filters["available_slot"] = TextCleaner.clean_people_count(filters["available_slot"])
        return filters

    @staticmethod
    def _apply_filters(tours: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply filters to tours list."""
        filtered_tours = tours

        print(f"Base: {filtered_tours}")

        if departure := filters.get("departure"):
            print(f"Departure filter: {departure}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if departure.lower().strip() in tour["departureLocation"].lower().strip()
            ]
        
        print(f"After filter departure: {filtered_tours}")

        if destination := filters.get("destination"):
            print(f"Destination filter: {destination}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if destination.lower().strip() in tour["city"].lower().strip() or 
                   destination.lower().strip() in tour["country"].lower().strip()
            ]

        print(f"After filter destination: {filtered_tours}")

        if start_date := filters.get("start_date"):
            print(f"Start date filter: {start_date}")
            try:
                start_date_obj = datetime.strptime(start_date, Config.SHORT_DATE_FORMAT)
                filtered_tours = [
                    tour for tour in filtered_tours 
                    if datetime.strptime(tour["startDate"], Config.SHORT_DATE_FORMAT) >= start_date_obj
                ]
            except ValueError:
                pass

        print(f"After filter start date: {filtered_tours}")

        if duration := filters.get("duration"):
            print(f"Duration filter: {duration}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if int(tour["duration"]) <= int(duration)
            ]

        print(f"After filter duration: {filtered_tours}")

        if price := filters.get("price"):
            print(f"Price filter: {price}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if float(tour["price"]) <= float(price)
            ]

        print(f"After filter price: {filtered_tours}")

        if available_slot := filters.get("available_slot"):
            print(f"Available slot filter: {available_slot}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if int(tour["availableSlots"]) >= int(available_slot)
            ]

        print(f"After filter available slot: {filtered_tours}")

        return filtered_tours

class ActionClearSlots(Action):
    """Action to clear all slots."""
    
    def name(self) -> Text:
        return "action_clear_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        slots = [
            "departure_point", "destination", "number_of_people",
            "departure_date", "budget", "duration"
        ]
        return [SlotSet(slot, None) for slot in slots if tracker.get_slot(slot) is not None]

class ValidateCustomerForm(FormValidationAction):
    """Form validation for customer information."""
    
    def name(self) -> Text:
        return "validate_customer_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"Xác nhận tên của bạn là {slot_value}")
        print(f"Validated name: {slot_value}")
        return {"name": slot_value}
    
    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not re.match(ValidationPatterns.PHONE, slot_value):
            dispatcher.utter_message(
                text="Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại di động Việt Nam (VD: 0912345678)."
            )
            return {"phone_number": None}
        
        clean_phone = re.sub(r'[-.]', '', slot_value)
        if clean_phone.startswith('+84'):
            clean_phone = '0' + clean_phone[3:]
        
        dispatcher.utter_message(text=f"Xác nhận số điện thoại của bạn là {clean_phone}")
        print(f"Validated phone number: {clean_phone}")
        return {"phone_number": clean_phone}

class ActionShowTours(Action):
    """Action to display filtered tours."""
    
    def name(self) -> Text:
        return "action_show_tours"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            response = requests.get(f"{Config.BE_SERVER}/getallforai")
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

            action = tracker.latest_action_name
            print(f"Latest action: {action}")
            slots = {k: v for k, v in slots.items() if v is not None}
            
            suitable_tours = TourManager.filter_tours(
                tours_data=tours_data,
                filters=slots,
                action=action
            )

            print(f"After sort: {suitable_tours}")

            if not suitable_tours:
                dispatcher.utter_message(text="Xin lỗi, không tìm thấy tour phù hợp với yêu cầu của bạn.")
                return []

            self._display_tours(dispatcher, suitable_tours, slots)
            return []

        except requests.RequestException as e:
            print(f"Server connection error: {str(e)}")
            dispatcher.utter_message(text="Xin lỗi, không thể lấy thông tin tour lúc này. Vui lòng thử lại sau.")
            return []
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            dispatcher.utter_message(text="Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn.")
            return []

    def _display_tours(
            self,
            dispatcher: CollectingDispatcher,
            tours: List[Dict[str, Any]],
            filters: Dict[str, Any]
        ) -> None:
            """Display formatted tour information."""
            dispatcher.utter_message(
                text=f"Tour gợi ý dựa theo yêu cầu của bạn: "
            )
            print(filters)

            for tour in tours:
                dispatcher.utter_message(text=f"""
    Tour {tour['id']} - {tour['city']}:
    * Điểm khởi hành: {tour['departureLocation']}
    * Điểm đến: {tour['city']}, {tour['country']}
    * Thời gian: {tour['startDate']} - {tour['endDate']} ({tour['duration']} ngày)
    * Giá tour: {tour['price']:,.0f} VND
    * Số chỗ còn trống: {tour['availableSlots']}
    """)
                dispatcher.utter_message(text=f"{tour['id']}")

    class ValidateTourForm(FormValidationAction):
        """Form validation for tour booking."""
        
        def name(self) -> Text:
            return "validate_tour_form"

        def _validate_and_confirm(
            self, 
            slot_name: str, 
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            validation_func: Optional[callable] = None
        ) -> Dict[Text, Any]:
            """Generic validation and confirmation method."""
            if not slot_value:
                dispatcher.utter_message(text=f"Vui lòng cho biết {slot_name}.")
                return {slot_name: None}
                
            if validation_func:
                cleaned_value = validation_func(slot_value)
                if cleaned_value is None:
                    return {slot_name: None}
                slot_value = cleaned_value

            response_text = {
                "departure_point": "điểm xuất phát",
                "destination": "điểm đến",
                "departure_date": "ngày xuất phát",
                "duration": "thời gian chuyến đi",
                "budget": "giá tour",
                "number_of_people": "số khách"
            }
            print(f"validate: {slot_name}: {slot_value}")
            dispatcher.utter_message(text=f"Xác nhận {response_text[slot_name]}: {slot_value}")
            return {slot_name: slot_value}

        def validate_departure_point(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
            if slot_value is not None:
                return self._validate_and_confirm("departure_point", slot_value, dispatcher)
            return {}

        def validate_destination(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
            if slot_value is not None:
                return self._validate_and_confirm("destination", slot_value, dispatcher)
            return {}

        def validate_departure_date(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
            if slot_value is not None:
                if not re.match(ValidationPatterns.DATE, slot_value):
                    dispatcher.utter_message(
                        text="Ngày không hợp lệ. Vui lòng cho biết thời điểm xuất phát."
                    )
                    return {"departure_date": None}
                
                return self._validate_and_confirm(
                    "departure_date", 
                    slot_value, 
                    dispatcher, 
                    TextCleaner.clean_date
                )
            return {}

        def validate_number_of_people(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
            if slot_value is not None:
                if not re.match(ValidationPatterns.PEOPLE, slot_value.lower()):
                    dispatcher.utter_message(
                        text="Số người không hợp lệ. Vui lòng nhập theo định dạng: số + người/khách (VD: 2 người, ba khách)."
                    )
                    return {"number_of_people": None}
                
                return self._validate_and_confirm(
                    "number_of_people", 
                    slot_value, 
                    dispatcher, 
                    TextCleaner.clean_people_count
                )
            return {}

        def validate_budget(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
            if slot_value is not None:
                if not re.match(ValidationPatterns.BUDGET, slot_value.lower()):
                    dispatcher.utter_message(
                        text="Ngân sách không hợp lệ. Vui lòng nhập theo định dạng: số + đơn vị (VD: 5 triệu, 500k, 2m)."
                    )
                    return {"budget": None}
                
                budget = TextCleaner.clean_budget(slot_value)
                # if budget:
                #     budget = f"{budget:,.0f}"
                    
                return self._validate_and_confirm("budget", budget, dispatcher)
            return {}

        def validate_duration(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
            if slot_value is not None:
                if not re.findall(ValidationPatterns.DURATION, slot_value.lower()):
                    dispatcher.utter_message(
                        text="""Thời gian không hợp lệ. Vui lòng nhập theo một trong các định dạng sau:
    - X ngày (VD: 3 ngày)
    - X ngày Y đêm (VD: 3 ngày 2 đêm)
    - X tuần/tháng (VD: 2 tuần, 1 tháng)"""
                    )
                    return {"duration": None}

                days = TextCleaner.clean_duration(slot_value)
                if not days or not 1 <= days <= 90:
                    dispatcher.utter_message(text="Thời gian tour phải từ 1 đến 90 ngày.")
                    return {"duration": None}
                
                return self._validate_and_confirm("duration", days , dispatcher)
            return {}

    class ActionShowPlan(Action):
        """Action to show detailed tour plan and answer questions."""
        
        def name(self) -> Text:
            return "action_answer_tour"
        
        def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
            tour_number = tracker.get_slot("tour_number")
            if not tour_number:
                dispatcher.utter_message(text="Vui lòng chọn số hiệu của tour.")
                return []
            
            try:
                # Fetch tour data
                response = requests.get(f"{Config.BE_SERVER}/{tour_number}")
                response.raise_for_status()
                tour_data = response.content.decode('utf-8')
                
                # Get user question and prepare AI prompt
                user_question = tracker.latest_message.get("text")
                prompt = self._create_ai_prompt(user_question)
                
                # Get AI response
                ai_response = self._get_ai_response(tour_data, prompt)
                dispatcher.utter_message(text=ai_response)
                
                return []
                
            except requests.RequestException as e:
                print(f"API request error: {str(e)}")
                dispatcher.utter_message(text="Xin lỗi, không thể lấy thông tin tour lúc này. Vui lòng thử lại sau.")
                return []
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                dispatcher.utter_message(text="Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn.")
                return []

        def _create_ai_prompt(self, user_question: str) -> str:
            """Create prompt for AI service."""
            return f"""
            Bạn trong vai trò 1 nhân viên tư vấn tour du lịch, dựa vào tour bên trên hãy giải đáp các thắc mắc một cách tự nhiên, 
            thoải mái, chi tiết từng mốc thời gian và cung cấp thêm các thông tin về các địa điểm tham quan để lôi cuốn khách hàng 
            nhưng các thông tin đưa ra phải đảm bảo độ chính xác.
            thắc mắc của user: {user_question}
            """

        def _get_ai_response(self, tour_data: str, prompt: str) -> str:
            """Get response from AI service."""
            response = requests.post(
                f"{Config.AI_SERVER}/post",
                json={"data": tour_data, "prompt": prompt}
            )
            response.raise_for_status()
            return response.content.decode('utf-8')