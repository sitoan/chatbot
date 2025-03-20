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
  Get-Content .env | foreach { $name, $value = $_.split('='); [System.Environment]::SetEnvironmentVariable($name, $value) }
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
