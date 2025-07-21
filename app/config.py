SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc:///?odbc_connect="
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=LAPTOP-JB0341DS\\SQLEXPRESS;"
    "Database=todo_db;"
    "Trusted_Connection=yes;"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "your_secret_key"
