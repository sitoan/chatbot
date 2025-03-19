## AFTER CLONING THE WHOLE PROJECT

## Backend
- Change the connection string to connect to your sqlserver in TourFlow_BE/Models/TourFlowContext.cs line 35 to replace your USERNAME and PASSWORD
- Change directory to chatbot/TourFlow_BE
- Run the commands below
  ```
  dotnet ef migrations add InitialCreate
  dotnet ef database update
  ```
- Run the .sql file to insert data

- Run backend
  `dotnet run`

## Frontend
- Open another terminal and change directory to chatbot/TourFlow-client
- Run the command below
  ```
  npm install
  npm run dev    
  ```
