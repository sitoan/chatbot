import re
from typing import Any, Dict, Optional, Text
from .config import ValidationPatterns
from .text_cleaner import TextCleaner
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, SessionStarted
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker, FormValidationAction

# Lớp ValidateCustomerForm xử lý việc xác thực thông tin khách hàng
# Được tách riêng để:
# 1. Tăng tính module hóa - dễ dàng mở rộng hoặc sửa đổi logic xác thực khách hàng
# 2. Tách biệt concerns giữa xác thực thông tin khách hàng và thông tin tour
class ValidateCustomerForm(FormValidationAction):
    """Form validation for customer information."""
    
    def name(self) -> Text:
        return "validate_customer_form"

    # Xác thực tên khách hàng
    # - Không cần pattern matching vì tên có thể đa dạng
    # - Chỉ xác nhận lại với người dùng để đảm bảo chính xác
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
    
    # Xác thực số điện thoại với các yêu cầu:
    # 1. Phải match với pattern số điện thoại VN
    # 2. Chuẩn hóa format (loại bỏ dấu gạch, chuyển +84 thành 0)
    # 3. Thông báo lỗi rõ ràng nếu không hợp lệ
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
        
        # Chuẩn hóa số điện thoại
        clean_phone = re.sub(r'[-.]', '', slot_value)
        if clean_phone.startswith('+84'):
            clean_phone = '0' + clean_phone[3:]
        
        dispatcher.utter_message(text=f"Xác nhận số điện thoại của bạn là {clean_phone}")
        print(f"Validated phone number: {clean_phone}")
        return {"phone_number": str(clean_phone)}

# Lớp ValidateTourForm xử lý việc xác thực thông tin đặt tour
# Được thiết kế với:
# 1. Phương thức helper _validate_and_confirm để tái sử dụng logic chung
# 2. Validation pattern riêng cho từng loại thông tin
# 3. Text cleaning để chuẩn hóa dữ liệu nhập vào
class ValidateTourForm(FormValidationAction):
    """Form validation for tour booking."""
    
    def name(self) -> Text:
        return "validate_tour_form"

    # Helper method để tránh lặp code trong các hàm validate
    # - Tái sử dụng logic xác nhận và thông báo
    # - Cho phép thêm hàm validation tùy chỉnh
    # - Dễ dàng thay đổi message format
    def _validate_and_confirm(
        self, 
        slot_name: str, 
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        validation_func: Optional[callable] = None
    ) -> Dict[Text, Any]:
        """Generic validation and confirmation method."""
        response_text = {
            "departure_point": "điểm xuất phát",
            "destination": "điểm đến",
            "departure_date": "ngày xuất phát", 
            "duration": "thời gian chuyến đi",
            "budget": "giá tour",
            "number_of_people": "số khách"
        }
        if not slot_value:
            dispatcher.utter_message(text=f"Vui lòng cho biết {response_text[slot_name]}.")
            return {slot_name: None}
            
        if validation_func:
            cleaned_value = validation_func(slot_value)
            if cleaned_value is None:
                return {slot_name: None}
            slot_value = cleaned_value
        
        print(f"validate: {slot_name}: {slot_value}")
        dispatcher.utter_message(text=f"Xác nhận {response_text[slot_name]}: {slot_value}")
        return {slot_name: slot_value}

    # Các điểm đến/đi không cần validation pattern
    # - Cho phép nhập tự do vì tên địa điểm có thể đa dạng
    # - Chỉ xác nhận lại với người dùng
    def validate_departure_point(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        requested_slot = tracker.get_slot("requested_slot")
        print(f"Requested slot (departure_point): {requested_slot}")
        if slot_value is None or requested_slot != "departure_point":
            return {"departure_point": None}
        return self._validate_and_confirm("departure_point", slot_value, dispatcher)

    def validate_destination(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value is None or tracker.get_slot("requested_slot") != "destination":
            return {"destination": None}
        return self._validate_and_confirm("destination", slot_value, dispatcher)

    # Xác thực ngày đi với pattern date
    # - Đảm bảo format ngày hợp lệ
    # - Chuẩn hóa các cách viết ngày khác nhau
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
        return {"departure_date": None}

    # Xác thực số lượng người với pattern people
    # - Hỗ trợ cả chữ và số (hai người, 2 khách)
    # - Chuẩn hóa về dạng số
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
        return {"number_of_people": None}

    # Xác thực ngân sách với pattern budget
    # - Hỗ trợ nhiều format (5 triệu, 500k, 2m)
    # - Chuẩn hóa về dạng số
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
            return self._validate_and_confirm("budget", budget, dispatcher)
        return {"budget": None}

    # Xác thực thời gian với pattern duration
    # - Hỗ trợ nhiều format (3 ngày, 3 ngày 2 đêm, 2 tuần)
    # - Giới hạn từ 1-90 ngày
    # - Chuẩn hóa về số ngày
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
        return {"duration": None}