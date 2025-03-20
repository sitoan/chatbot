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
