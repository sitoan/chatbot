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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        available_date = tracker.get_slot("available_date")
        
        if available_date:
            available_date = datetime.strptime(available_date, "%Y-%m-%d")
            response = requests.get("http://localhost:5175/api/tour")
            
            if response.status_code == 200:
                tours = response.json()
                filtered_tours = [
                    tour for tour in tours 
                    if datetime.fromisoformat(tour["startDate"]) > available_date
                ]
                
                if filtered_tours:
                    response_text = "Các tour có sẵn vào thời gian bạn yêu cầu:\n"
                    for tour in filtered_tours:
                        response_text += (
                            f"🔹 **Điểm đến**: {tour['destination']}\n"
                            f"🔹 **Nơi khởi hành**: {tour['departureLocation']}\n"
                            f"🔹 **Thời gian**: {tour['startDate']} - {tour['endDate']}\n"
                            f"🔹 **Giá**: {tour['price']:.2f} VND\n"
                            f"🔹 **Số lượng còn lại**: {tour['availableSlots']}\n"
                            f"-------------------------\n"  
                        )
                    dispatcher.utter_message(text=response_text)
                else:
                    dispatcher.utter_message(text="Xin lỗi, không có tour nào có sẵn trong khoảng thời gian này.")
            else:
                dispatcher.utter_message(text="Lỗi khi truy xuất dữ liệu tour.")
        else:
            dispatcher.utter_message(text="Xin lỗi, tôi không tìm thấy thông tin ngày bạn đã cung cấp.")
        
        return []

class ActionShowRecentTours(Action):
    def name(self) -> str:
        return "action_show_recent_tours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        today = datetime.now()
        two_months_from_now = today + relativedelta(months=2)

        response = requests.get("http://localhost:5175/api/tour")
        
        if response.status_code == 200:
            tours = response.json()
            recent_tours = [
                tour for tour in tours
                if today <= datetime.fromisoformat(tour["startDate"]) <= two_months_from_now
            ]

            if recent_tours:
                response_text = "Các tour có sẵn trong 2 tháng tới:\n"
                for tour in recent_tours:
                    response_text += (
                        f"🔹 **Điểm đến**: {tour['destination']}\n"
                        f"🔹 **Nơi khởi hành**: {tour['departureLocation']}\n"
                        f"🔹 **Thời gian**: {tour['startDate']} - {tour['endDate']}\n"
                        f"🔹 **Giá**: {tour['price']:.2f} VND\n"
                        f"🔹 **Số lượng còn lại**: {tour['availableSlots']}\n"
                        f"-------------------------\n"
                    )
                dispatcher.utter_message(text=response_text)
            else:
                dispatcher.utter_message(text="Không có tour nào trong 2 tháng tới.")
        else:
            dispatcher.utter_message(text="Lỗi khi truy xuất dữ liệu tour.")
        
        return []

class ActionShowToursBySpecificDate(Action):
    def name(self) -> str:
        return "action_show_tours_by_specific_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        month = tracker.get_slot("month")
        if month is None:
            dispatcher.utter_message(text="Xin lỗi, bạn cần cung cấp tháng.")
            return []
        
        try:
            month = int(month)
        except ValueError:
            dispatcher.utter_message(text="Tháng không hợp lệ.")
            return []

        year = datetime.now().year
        start_date = datetime(year, month, 1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        response = requests.get("http://localhost:5175/api/tour")
        
        if response.status_code == 200:
            tours = response.json()
            specific_tours = [
                tour for tour in tours
                if start_date <= datetime.fromisoformat(tour["startDate"]) <= end_date
            ]

            if specific_tours:
                response_text = f"Các tour có sẵn trong tháng {month}:\n"
                for tour in specific_tours:
                    response_text += (
                        f"🔹 **Điểm đến**: {tour['destination']}\n"
                        f"🔹 **Nơi khởi hành**: {tour['departureLocation']}\n"
                        f"🔹 **Thời gian**: {tour['startDate']} - {tour['endDate']}\n"
                        f"🔹 **Giá**: {tour['price']:.2f} VND\n"
                        f"🔹 **Số lượng còn lại**: {tour['availableSlots']}\n"
                        f"-------------------------\n"
                    )
                dispatcher.utter_message(text=response_text)
            else:
                dispatcher.utter_message(text=f"Xin lỗi, không có tour nào có sẵn trong tháng {month}.")
        else:
            dispatcher.utter_message(text="Lỗi khi truy xuất dữ liệu tour.")
        
        return []
    
class ActionShowToursByBudget(Action):
    def name(self) -> str:
        return "action_show_tours_by_budget"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        # Lấy ngân sách từ tin nhắn khách hàng
        message = tracker.latest_message['text']
        
        # Cập nhật regex để nhận diện cả số nguyên và số có phần nghìn
        budget_pattern = r'(\d{1,3}(?:\.\d{3})*|\d+)\s*(triệu|ngàn)?'
        match = re.search(budget_pattern, message)

        if match:
            budget_str = match.group(1).replace('.', '')  
            unit = match.group(2)  
            
            if unit == "triệu":
                budget = int(budget_str) * 1000000  
            elif unit == "ngàn":
                budget = int(budget_str) * 1000  
            else:
                budget = int(budget_str)  

            display_budget = budget

            if budget < 10000:  # Ngân sách tối thiểu đề xuất
                dispatcher.utter_message(text="Xin lỗi, hiện không có tour nào phù hợp với ngân sách của bạn.")
                return []

        else:
            dispatcher.utter_message(text="Xin lỗi, bạn vui lòng cung cấp ngân sách cụ thể để tìm tour phù hợp.")
            return []

        try:
            response = requests.get(f"http://localhost:5175/api/tour?max_price={budget}")
            response.raise_for_status()  
            tours = response.json()  

            if tours:
                response_text = f"Các tour phù hợp với ngân sách của bạn ({display_budget} VND):\n"
                found_tours = False  # Biến để theo dõi có tour nào hợp lệ không
                for tour in tours:
                    if tour['price'] <= budget:  # Chỉ hiển thị tour nếu giá <= ngân sách
                        found_tours = True
                        response_text += (
                            f"🔹 **Điểm đến**: {tour['destination']}\n"
                            f"🔹 **Nơi khởi hành**: {tour['departureLocation']}\n"
                            f"🔹 **Thời gian**: {tour['startDate']} - {tour['endDate']}\n"
                            f"🔹 **Giá**: {tour['price']:.2f} VND\n"
                            f"🔹 **Số lượng còn lại**: {tour['availableSlots']}\n"
                            f"-------------------------\n"
                        )

                if not found_tours:
                    additional_budget = budget + 1000  # Ngân sách thêm 1000 VND
                    response = requests.get(f"http://localhost:5175/api/tour?min_price={budget}&max_price={additional_budget}")
                    response.raise_for_status()
                    alternative_tours = response.json()

                    if alternative_tours:
                        response_text += (
                            f"Không tìm thấy tour nào trong ngân sách {display_budget} VND của bạn. "
                            f"Nhưng đây là một số tour trong tầm giá hơn {display_budget} VND một chút:\n"
                        )
                        for tour in alternative_tours:
                            response_text += (
                                f"🔹 **Điểm đến**: {tour['destination']}\n"
                                f"🔹 **Nơi khởi hành**: {tour['departureLocation']}\n"
                                f"🔹 **Thời gian**: {tour['startDate']} - {tour['endDate']}\n"
                                f"🔹 **Giá**: {tour['price']:.2f} VND\n"
                                f"🔹 **Số lượng còn lại**: {tour['availableSlots']}\n"
                                f"-------------------------\n"
                            )
                    else:
                        dispatcher.utter_message(text="Xin lỗi, hiện không có tour nào phù hợp với ngân sách của bạn.")
                else:
                    dispatcher.utter_message(text=response_text)
            else:
                dispatcher.utter_message(text="Xin lỗi, hiện không có tour nào phù hợp với ngân sách của bạn.")

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Xin lỗi, đã xảy ra lỗi khi kết nối với hệ thống. Vui lòng thử lại sau.")
            print(f"API request error: {e}")

        return []

class ActionShowToursBySpecificDuration(Action):
    def name(self) -> str:
        return "action_show_tours_by_specific_duration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        message = tracker.latest_message['text']
        duration_pattern = r'(\d+)\s*ngày\s*(\d+)\s*đêm'
        match = re.search(duration_pattern, message)

        if match:
            num_days = int(match.group(1))
            num_nights = int(match.group(2))
            
            if num_days != num_nights + 1:
                dispatcher.utter_message(text="Số ngày không đúng với số đêm. Vui lòng kiểm tra lại.")
                return []

            # Gọi API để lấy danh sách tour
            response = requests.get("http://localhost:5175/api/tour")
            if response.status_code == 200:
                tours = response.json()
            else:
                dispatcher.utter_message(text="Xin lỗi, không thể lấy dữ liệu tour từ hệ thống.")
                return []

            found_tours = []
            for tour in tours:
                start_date = datetime.fromisoformat(tour['startDate'])
                end_date = datetime.fromisoformat(tour['endDate'])
                duration_days = (end_date - start_date).days

                if duration_days == num_days:
                    found_tours.append(tour)

            if found_tours:
                response_text = f"Các tour phù hợp với yêu cầu của bạn ({num_days} ngày, {num_nights} đêm):\n"
                for tour in found_tours:
                    response_text += (
                        f"🔹 **Điểm đến**: {tour['destination']}\n"
                        f"🔹 **Nơi khởi hành**: {tour['departureLocation']}\n"
                        f"🔹 **Thời gian**: {tour['startDate']} - {tour['endDate']}\n"
                        f"🔹 **Giá**: {tour['price']:.2f} VND\n"
                        f"🔹 **Số lượng còn lại**: {tour['availableSlots']}\n"
                        f"-------------------------\n"
                    )
                dispatcher.utter_message(text=response_text)
            else:
                response_text = "Xin lỗi, hiện không có tour nào phù hợp với yêu cầu của bạn. Đây là một số tour khác:\n"
                for tour in tours[:5]:  # Lấy tối đa 5 tour từ danh sách tour
                    response_text += (
                        f"🔹 **Điểm đến**: {tour['destination']}\n"
                        f"🔹 **Nơi khởi hành**: {tour['departureLocation']}\n"
                        f"🔹 **Thời gian**: {tour['startDate']} - {tour['endDate']}\n"
                        f"🔹 **Giá**: {tour['price']:.2f} VND\n"
                        f"🔹 **Số lượng còn lại**: {tour['availableSlots']}\n"
                        f"-------------------------\n"
                    )
                dispatcher.utter_message(text=response_text)
        else:
            dispatcher.utter_message(text="Xin lỗi, bạn vui lòng cung cấp thông tin ngày và đêm cụ thể.")

        return []