
from datetime import datetime
import re
from typing import Dict, Text, List, Any
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from .text_cleaner import TextCleaner

from .tour_manager import TourManager
from .config import NUMBERS, Config

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
            "departure_date", "budget", "duration", "name", "phone_number"
        ]
        return [SlotSet(slot, None) for slot in slots if tracker.get_slot(slot) is not None]

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
            intent = tracker.get_intent_of_latest_message()
            print(f"Latest action: {intent}")
            if intent == "show_tours":
                response = requests.get(f"{Config.BE_SERVER}/tour/gettop5forai")
            else:
                response = requests.get(f"{Config.BE_SERVER}/tour/getallforai")
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

            slots = {k: v for k, v in slots.items() if v is not None}
            
            suitable_tours = TourManager.filter_tours(
                tours_data=tours_data,
                filters=slots,
                intent=intent
            )

            # print(f"After sort: {suitable_tours}")

            if not suitable_tours:
                dispatcher.utter_message(text="Xin lỗi, không tìm thấy tour phù hợp với yêu cầu của bạn.")
                return []

            self._display_tours(dispatcher, suitable_tours)
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
        ) -> None:
            """Display formatted tour information."""
            dispatcher.utter_message(
                text=f"Tour gợi ý dựa theo yêu cầu của bạn: "
            )

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

class ActionAnswerTour(Action):
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
            response = requests.get(f"{Config.BE_SERVER}/tour/{tour_number}")
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

class ActionPostUserAnswer(Action):
    def name(self) -> Text:
        return "action_post_user_answer"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        print("-"*50)

        print(f"User ID: {tracker.sender_id}") 
        
        start_date = tracker.get_slot("departure_date")
        if start_date:  # Kiểm tra nếu có giá trị
            start_date = datetime.strptime(start_date, Config.DATE_FORMAT)
            start_date = start_date.strftime("%Y-%m-%d")\

        budget = tracker.get_slot("budget")
        if budget is not None:
            budget = TextCleaner.clean_budget(budget)
        
        number_of_people = tracker.get_slot("number_of_people")
        if number_of_people is not None:
            number_of_people = TextCleaner.clean_people_count(number_of_people)


        data = {
            'userId': int(tracker.sender_id) if tracker.sender_id else None,
            'PhoneNumber': tracker.get_slot("phone_number"),
            'TourId': int(tracker.get_slot("tour_number")) if tracker.get_slot("tour_number") else None,
            'StarPos': tracker.get_slot("departure_point"),
            'EndPos': tracker.get_slot("destination"),
            'StartDate': start_date,
            'Duration': str(tracker.get_slot("duration")) if tracker.get_slot("duration") else None,
            'Budget': budget,
            'AvailableSlot': number_of_people
        }

        print(data)

        try:
            response = requests.post(f"{Config.BE_SERVER}/userdatacollection", json=data)
            response.raise_for_status()  # Raise exception cho các mã lỗi HTTP
            print('Success:', response.text)
        except requests.exceptions.RequestException as e:
            print('Failed to post data:', e)

        return []