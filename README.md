## AFTER CLONING THE WHOLE PROJECT

## Backend
- Change the connection string to connect to your sqlserver in <mark>backend/Models/TourFlowContext.cs line 35 to replace your USERNAME and PASSWORD<mark/>
- Change directory to <mark>chatbot/backend<mark/>
- Run the commands below
  ```
  dotnet ef migrations add InitialCreate
  dotnet ef database update
  ```
- Run the .sql file to insert data

- Run backend
  `dotnet run`

## Frontend
- Open another terminal and change directory to <mark>chatbot/frontend<mark/>
- Run the command below
  ```
  npm install
  npm run dev    
  ```
## Chatbot
- Create virtualenv (recommended)
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
- Install dependencies
  ```
  pip install -r requirements.txt
  ```
- Load environment variables (.env file)
  ```
  set RASA_PRO_LICENSE=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5NTJkMzJiMi1kNzBiLTRlMTMtOTY4Yy0wODI0OWM3YmNmMWEiLCJpYXQiOjE3MjgyMDEwNzQsIm5iZiI6MTcyODIwMTA3MSwic2NvcGUiOiJyYXNhOnBybyByYXNhOnBybzpjaGFtcGlvbiIsImV4cCI6MTgyMjgwOTA3MSwiZW1haWwiOiJzLnRvYW44ODNAZ21haWwuY29tIiwiY29tcGFueSI6IlJhc2EgQ2hhbXBpb25zIn0.CnsMHcyONMNuNoLQ8JUGczYjdvb4C3M__n0WJXkXE2vW_Jw00jXA9j73hE5dtxyHO4oL3ymJnSxTdTlIqtptC_p275Le_wrpQeOxb6EB-ypjViCtWYVStf_GKafErRIzM6xLeUWjAaFNta4-uIrLipCh92kkxnuXf5V1FdJAjWlohNAOQVU7WCLrvRAVvxziA_sib6LiNrd5dcTFdNr0LeP_rilfcmIzx91lky47EeQKmUOA_kWh1KsshPpJVSPi2UV8oEdrmvTut-iGmrCo7VDPLsC_hIzw2b2qg5aLY05I5WdtyI-VnIyOjF4k13XLRfWjsf2mIDXB4t3-8OuJuA
  set AI_SERVER=http://127.0.0.1:5000/api
  set BE_SERVER=http://localhost:5175/api
  set GEMINI_API_KEY=AIzaSyAqZW_aWtA1eUqGM3vHk5s2vATkG2g_EiM
  ```
- Change directory to <mark>chatbot/chatbot<mark/> 
- Train Rasa Model, this will generate a model file in the models/ directory
  ```
  rasa train
  ```
- Need 2 terminal windows to run the Rasa server and the custom action server
  
Terminal 1 – Run Rasa Server
  ```
  rasa run -m models --enable-api --cors "*"
  ```

Terminal 2 – Run Custom Actions
  ```
  rasa run actions
  ```

## AI_service
- Change directory to <mark>chatbot/ai_service<mark/>
- Run
  ```
  python main.py
  ```
