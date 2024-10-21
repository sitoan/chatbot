import pyodbc

class DatabaseConnection:
    def __init__(self):
        self.server = "VUONGTRAN\SQLEXPRESS"
        self.database = "TourFlow"
        self.user = "sa"
        self.password = "dockerStrongPwd123"
        self.connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password};TrustServerCertificate=yes;"
        self.connection = None
        try:
            self.connection = pyodbc.connect(self.connection_string)
            print("Connection successful")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def execute_query(self, query):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        else:
            print("Connection not established")
            return None
        
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")
        else:
            print("Connection not established")