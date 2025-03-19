## AFTER CLONING THE WHOLE PROJECT

# Backend
- Change the connection string to connect to your sqlserver in TourFlow_BE/Models/TourFlowContext.cs line 35
- Run the commands below
  ```
  dotnet ef migrations add InitialCreate
  dotnet ef database update
  ```
- Run the .sql file to insert data

- Run backend
  `dotnet run`

# Frontend
- Run the command below
  ```
  npm pip install
  npm run dev    
  ```
