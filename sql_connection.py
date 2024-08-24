import pyodbc

# Connection parameters
SERVER = 'MSI\\SQLEXPRESS01'
DATABASE = 'prayagdb'

# Connection string for Windows authentication
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;TrustServerCertificate=yes'

# Connect to the database
try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")

    # Now you can create a cursor object using the connection
    cursor = conn.cursor()

    # Example query execution
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    print(row)

except Exception as e:
    print("Error while connecting to the database:", e)

finally:
    # Always close the connection when you're done
    if conn:
        conn.close()
        print("Connection closed.")