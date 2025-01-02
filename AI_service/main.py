import json
from GeminiAi import GeminiAi
from flask import Flask,request, jsonify

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# call Gemini
@app.route("/api/llm_response", methods=["POST"])
def llm_response():
    bot = GeminiAi()
    response = bot.run(request.data)
    return str(response)

@app.route("/api/get", methods= ["GET"])
def get_method():
    return "Hello World"

@app.route("/api/post", methods=["POST"])
def post_method():
    res = request.get_json()
    bot = GeminiAi()
    response = bot.run(res['data']+res['prompt'])
    print(response)
    return response


if __name__ == "__main__":
    app.run(port= 5000, debug= True)

