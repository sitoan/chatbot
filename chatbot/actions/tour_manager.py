import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .config import Config
from .text_cleaner import TextCleaner

# Sử dụng dataclass để tạo model cho tour data
# Ưu điểm:
# - Type safety
# - Tự động generate các magic methods (__init__, __repr__, etc.)
# - Code gọn gàng và dễ maintain
@dataclass
class TourData:
    id: str
    city: str
    country: str
    departureLocation: str
    startDate: str
    endDate: str
    duration: str
    price: float
    availableSlots: int


class TourManager:    
    @staticmethod
    def filter_tours(
        tours_data: Union[str, List[Dict[str, Any]]],
        filters: Dict[str, Any],
        intent: Optional[str] = None
    ) -> List[TourData]:
        """
        Lọc danh sách tours theo các tiêu chí
        
        Args:
            tours_data: Data tours dạng JSON string hoặc list
            filters: Dictionary chứa các điều kiện lọc
            intent: Intent của user để xác định cách xử lý
            
        Returns:
            List các tour thỏa mãn điều kiện, đã sort theo ngày và giá
        """
        try:
            # Parse JSON nếu input là string
            suitable_tours = json.loads(tours_data) if isinstance(tours_data, str) else tours_data
            
            # Clean filter values nếu intent là find_tour
            if intent == "find_tour":
                filters = TourManager._clean_filter_values(filters)
                print(f"Filtered filters: {filters}")
            
            # Áp dụng các filters
            suitable_tours = TourManager._apply_filters(suitable_tours, filters)

            # print(f"Overall: {suitable_tours}")
            
            # Sort kết quả theo ngày và giá
            return sorted(
                suitable_tours,
                key=lambda x: (
                    datetime.strptime(x["startDate"], Config.DATE_FORMAT),
                    float(x["price"])
                )
            )
        except Exception as e:
            print(f"Error filtering tours: {str(e)}")
            return []

    @staticmethod
    def _clean_filter_values(filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chuẩn hóa giá trị của các filters
        
        Args:
            filters: Dictionary chứa các filter gốc
            
        Returns:
            Dictionary với các giá trị đã được chuẩn hóa
        """
        # Sử dụng TextCleaner để chuẩn hóa từng loại dữ liệu
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
        """
        Áp dụng các điều kiện lọc lên danh sách tours
        
        Args:
            tours: Danh sách tours gốc
            filters: Dictionary chứa các điều kiện lọc
            
        Returns:
            Danh sách tours đã được lọc
        """
        filtered_tours = tours

        # print(f"Base: {filtered_tours}")

        # Lọc theo điểm khởi hành
        # So sánh case-insensitive và bỏ khoảng trắng thừa
        if departure := filters.get("departure"):
            print(f"Departure filter: {departure}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if departure.lower().strip() in tour["departureLocation"].lower().strip()
            ]
        
        # print(f"After filter departure: {filtered_tours}")

        # Lọc theo điểm đến (city hoặc country)
        if destination := filters.get("destination"):
            print(f"Destination filter: {destination}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if destination.lower().strip() in tour["city"].lower().strip() or 
                   destination.lower().strip() in tour["country"].lower().strip()
            ]

        # print(f"After filter destination: {filtered_tours}")

        # Lọc theo ngày khởi hành
        # Chỉ lấy các tour có ngày khởi hành >= ngày yêu cầu
        if start_date := filters.get("start_date"):
            print(f"Start date filter: {start_date}")
            try:
                start_date_obj = datetime.strptime(start_date, Config.DATE_FORMAT)
                filtered_tours = [
                    tour for tour in filtered_tours 
                    if datetime.strptime(tour["startDate"], Config.DATE_FORMAT) >= start_date_obj
                ]
            except ValueError:
                pass

        # print(f"After filter start date: {filtered_tours}")

        # Lọc theo số ngày
        # Chỉ lấy các tour có số ngày <= yêu cầu
        if duration := filters.get("duration"):
            print(f"Duration filter: {duration}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if int(tour["duration"]) <= int(duration)
            ]

        # print(f"After filter duration: {filtered_tours}")

        # Lọc theo giá
        # Chỉ lấy các tour có giá <= budget
        if price := filters.get("price"):
            print(f"Price filter: {price}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if float(tour["price"]) <= float(price)
            ]

        # print(f"After filter price: {filtered_tours}")

        # Lọc theo số chỗ trống
        # Chỉ lấy các tour có đủ chỗ theo yêu cầu
        if available_slot := filters.get("available_slot"):
            print(f"Available slot filter: {available_slot}")
            filtered_tours = [
                tour for tour in filtered_tours 
                if int(tour["availableSlots"]) >= int(available_slot)
            ]

        print(f"After filter available slot: {filtered_tours}")

        return filtered_tours