import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Cấu hình API key từ biến môi trường - cách này an toàn hơn việc hardcode API key trực tiếp trong code
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiAi:
    def __init__(self):
        # Cấu hình generation để điều chỉnh cách model sinh nội dung
        generation_config = {
            # temperature=1: Cho phép model sáng tạo hơn trong câu trả lời
            # Nếu muốn câu trả lời chính xác và ít ngẫu nhiên hơn, nên giảm xuống 0-0.5
            "temperature": 1,
            
            # Các tham số sau bị comment vì dùng giá trị mặc định là đủ tốt
            # "top_p": 0.95,  # Kiểm soát đa dạng từ vựng
            # "top_k": 64,    # Giới hạn số lượng token được chọn
            # "max_output_tokens": 8192,  # Giới hạn độ dài output
            
            # Chỉ định response dạng text thuần túy, không có formatting
            "response_mime_type": "text/plain",
        }

        # Khởi tạo model với các cấu hình an toàn và chỉ dẫn hệ thống
        self.model = genai.GenerativeModel(
            # Sử dụng Gemini 1.5 Pro - phiên bản mới nhất và mạnh nhất
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            
            # Cấu hình bộ lọc an toàn để tránh nội dung có hại
            # BLOCK_MEDIUM_AND_ABOVE: chặn nội dung có mức độ rủi ro trung bình trở lên
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_DANGEROUS",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ],
            
            # Chỉ dẫn hệ thống bằng tiếng Việt để đảm bảo output như mong muốn
            system_instruction = "chỉ đưa ra câu trả lời, không giải thích thêm và trả lời bằng ngôn ngữ Việt Nam"
        )

    # Hàm chạy model để sinh nội dung từ prompt đầu vào
    def run(self, message):
        response = self.model.generate_content(message)
        return response.text