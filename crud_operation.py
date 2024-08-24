import pyodbc

class DatabaseManager:
    def __init__(self, server, driver):
        self.server = server
        self.driver = driver
        self.conn = None
        self.cursor = None

    def connect(self, database=None, autocommit=False):
        """
    Description:
        Establishes a connection to the SQL Server, optionally specifying a database and whether to use autocommit.
    Parameters:
        database (str, optional): The name of the database to connect to. Defaults to None, connecting only to the SQL Server.
        autocommit (bool, optional): Whether to use autocommit mode. Defaults to False.
    Returns:
        None
        """
        connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};Trusted_Connection=yes;TrustServerCertificate=yes'
        self.conn = pyodbc.connect(connection_string, autocommit=autocommit)
        self.cursor = self.conn.cursor()
        print(f"Connected to {'database ' + database if database else 'SQL Server'} successfully!")

    def create_database(self, db_name):
        """
    Description:
        Creates a new database on the SQL Server if it does not already exist.
    Parameters:
        db_name (str): The name of the database to be created.
    Returns:
        None
        """
        # Connect to the SQL Server without specifying a database
        # connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE=master;Trusted_Connection=yes;TrustServerCertificate=yes'
        if self.database_exists(db_name):
            print(f"Database '{db_name}' already exists.")
            return
        self.connect(autocommit=True)
        # self.conn = pyodbc.connect(connection_string, autocommit=True)
        # self.cursor = self.conn.cursor()

        # Execute the create database command
        self.cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully!")

    def delete_database(self, db_name):
        """
    Description:
        Deletes a database from the SQL Server if it exists.
    Parameters:
        db_name (str): The name of the database to be deleted.
    Returns:
        None
        """

        if not self.database_exists(db_name):
            print(f"Database '{db_name}' does not exist.")
            return
        
        # Connect to the SQL Server without specifying a database
        self.connect(database='master', autocommit=True)
        
        # Execute the drop database command
        self.cursor.execute(f"DROP DATABASE {db_name}")
        print(f"Database '{db_name}' deleted successfully!")    

    def create_table(self, db_name, table_name):
        """
    Description:
        Creates a new table in the specified database if the database exists.
    Parameters:
        db_name (str): The name of the database where the table will be created.
        table_name (str): The name of the table to be created.
    Returns:
        None
        """
        if not self.database_exists(db_name):
            print(f"Database '{db_name}' does not exist.")
            return
        
        self.connect(db_name)
        create_table_query = f'''
        CREATE TABLE {table_name} (
            EmployeeID INT PRIMARY KEY IDENTITY(1,1),
            FirstName NVARCHAR(50),
            LastName NVARCHAR(50),
            Age INT,
            Department NVARCHAR(50)
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()
        print(f"Table '{table_name}' created successfully in database '{db_name}'!")

    def insert_record(self, db_name, table_name, first_name, last_name, age, department):
        """
    Description:
        Inserts a new record into the specified table within the specified database.
    Parameters:
        db_name (str): The name of the database containing the table.
        table_name (str): The name of the table where the record will be inserted.
        first_name (str): The first name of the employee.
        last_name (str): The last name of the employee.
        age (int): The age of the employee.
        department (str): The department where the employee works.
    Returns:
        None
        """
        if not self.database_exists(db_name):
            print(f"Database '{db_name}' does not exist.")
            return
        
        self.connect(db_name)
        insert_query = f'''
        INSERT INTO {table_name} (FirstName, LastName, Age, Department)
        VALUES (?, ?, ?, ?)
        '''
        self.cursor.execute(insert_query, (first_name, last_name, age, department))
        self.conn.commit()
        print(f"Record for {first_name} {last_name} inserted successfully!")

    def read_records(self, db_name, table_name):
        """
    Description:
        Retrieves and displays all records from the specified table within the specified database.
    Parameters:
        db_name (str): The name of the database containing the table.
        table_name (str): The name of the table from which records will be retrieved.
    Returns:
        None
        """
        if not self.database_exists(db_name):
            print(f"Database '{db_name}' does not exist.")
            return
        
        self.connect(db_name)
        select_query = f"SELECT * FROM {table_name}"
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()
        print(f"\nRecords in table '{table_name}':")
        for row in rows:
            print(f"ID: {row.EmployeeID}, Name: {row.FirstName} {row.LastName}, Age: {row.Age}, Department: {row.Department}")

    def delete_record(self, db_name, table_name, employee_id):
        """
    Description:
        Deletes a specific record from the specified table within the specified database based on the Employee ID.
    Parameters:
        db_name (str): The name of the database containing the table.
        table_name (str): The name of the table from which the record will be deleted.
        employee_id (int): The Employee ID of the record to be deleted.
    Returns:
        None
        """
        if not self.database_exists(db_name):
            print(f"Database '{db_name}' does not exist.")
            return
        
        self.connect(db_name)
        delete_query = f'''
        DELETE FROM {table_name}
        WHERE EmployeeID = ?
        '''
        self.cursor.execute(delete_query, employee_id)
        self.conn.commit()
        print(f"Record with ID {employee_id} deleted successfully!")

    def close_connection(self):
        """
    Description:
        Closes the current database connection and cursor if they are open.
    Parameters:
        None
    Returns:
        None
        """

        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Connection closed.")

    def get_existing_databases(self):
        """
    Description:
        Retrieves and returns a list of all existing databases on the SQL Server.
    Parameters:
        None
    Returns:
        databases (list): A list of database names present on the SQL Server.
        """
        self.connect()
        self.cursor.execute("SELECT name FROM sys.databases")
        databases = [row.name for row in self.cursor.fetchall()]
        return databases

    def database_exists(self, db_name):
        """
    Description:
        Checks if a specified database exists on the SQL Server.
    Parameters:
        db_name (str): The name of the database to check for existence.
    Returns:
        bool: True if the database exists, False otherwise.
        """
        databases = self.get_existing_databases()
        return db_name in databases

def main():
    server = 'localhost\\SQLEXPRESS01'
    driver = '{ODBC Driver 18 for SQL Server}'
    # database = 'prayagdb'
    # password
    # username 
    # for sql connection
    db_manager = DatabaseManager(server, driver)
    
    while True:
        print("\nChoose an option:")
        print("1. Create Database")
        print("2. Create Table")
        print("3. Insert Record")
        print("4. Read Records")
        print("5. Delete Record")
        print("6. Delete Database")  # New option for deleting a database
        print("7. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        match choice:
            case 1:
                databases = db_manager.get_existing_databases()
                print("Existing databases:")
                for db in databases:
                    print(f" - {db}")
                db_name = input("Enter database name: ")
                db_manager.create_database(db_name)
            case 2:
                databases = db_manager.get_existing_databases()
                print("Existing databases:")
                for db in databases:
                    print(f" - {db}")
                db_name = input("Enter the name of the database to create the table in: ")
                if not db_manager.database_exists(db_name):
                    print(f"Database '{db_name}' does not exist.")
                    continue
                table_name = input("Enter table name: ")
                db_manager.create_table(db_name, table_name)
            case 3:
                databases = db_manager.get_existing_databases()
                print("Existing databases:")
                for db in databases:
                    print(f" - {db}")
                db_name = input("Enter database name: ")
                table_name = input("Enter table name: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                age = int(input("Enter age: "))
                department = input("Enter department: ")
                db_manager.insert_record(db_name, table_name, first_name, last_name, age, department)
            case 4:
                databases = db_manager.get_existing_databases()
                print("Existing databases:")
                for db in databases:
                    print(f" - {db}")                
                db_name = input("Enter database name: ")
                table_name = input("Enter table name: ")
                db_manager.read_records(db_name, table_name)
            case 5:
                databases = db_manager.get_existing_databases()
                print("Existing databases:")
                for db in databases:
                    print(f" - {db}")
                db_name = input("Enter database name: ")
                table_name = input("Enter table name: ")
                employee_id = int(input("Enter Employee ID to delete: "))
                db_manager.delete_record(db_name, table_name, employee_id)
            case 6:
                databases = db_manager.get_existing_databases()
                print("Existing databases:")
                for db in databases:
                    print(f" - {db}")
                db_name = input("Enter database name to delete: ")
                db_manager.delete_database(db_name)
            case 7:
                print("Exiting the program...")
                db_manager.close_connection()
                break
            case _:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
