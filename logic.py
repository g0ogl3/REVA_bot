import sqlite3
from sqlite3 import Error
from config import DATABASE
# Function to connect to SQLite database (if the database does not exist, it will be created)
def create_connection(path):
    connection = sqlite3.connect(DATABASE)
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite database is successful!")
    except Error as e:
        print(f"Connection error: '{e}'")
    return connection

# Function for executing SQL queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.executescript(query)
        connection.commit()
        print("Request completed successfully!")
    except Error as e:
        print(f"Error executing request: '{e}'")

# Function for getting data (SELECT queries)
def fetch_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error while receiving data: '{e}'")

# Function to initialize the database (create tables and insert data)
def init_db():
    connection = create_connection(DATABASE)

    create_tables_query = """
    CREATE TABLE IF NOT EXISTS Properties (
        property_id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_type TEXT,
        size REAL,
        price REAL,
        num_bedrooms INTEGER,
        num_bathrooms INTEGER,
        location_id INTEGER,
        agent_id INTEGER,
        available_from DATE,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS Agents (
        agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT,
        phone_number TEXT,
        email TEXT,
        agency_name TEXT
    );

    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        phone_number TEXT,
        email TEXT,
        customer_type TEXT
    );

    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER,
        customer_id INTEGER,
        transaction_date DATE,
        transaction_type TEXT,
        final_price REAL
    );

    CREATE TABLE IF NOT EXISTS Locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        district TEXT,
        postal_code TEXT
    );
    """
    execute_query(connection, create_tables_query)

    insert_data_query = """
    INSERT INTO Locations (city, district, postal_code)
    VALUES ('Moscow', 'Central', '101000'),
           ('Saint Petersburg', 'Vasileostrovsky', '199178'),
           ('Novosibirsk', 'Central', '630099');

    INSERT INTO Agents (agent_name, phone_number, email, agency_name)
    VALUES ('Ivan Ivanov', '+79991112233', 'ivanov@realestate.ru', 'RealEstate Agency'),
           ('Anna Smirnova', '+79991112234', 'smirnova@realestate.ru', 'Premium Properties'),
           ('Peter Petrov', '+79991112235', 'petrov@realestate.ru', 'Luxury Realty');

    INSERT INTO Properties (property_type, size, price, num_bedrooms, num_bathrooms, location_id, agent_id, available_from, status)
    VALUES ('Flat', 80.50, 12000000, 3, 2, 1, 1, '2025-01-10', 'on sale'),
           ('House', 150.00, 25000000, 4, 3, 2, 2, '2024-12-01', 'for rent'),
           ('Office', 200.00, 30000000, 0, 2, 3, 3, '2025-02-15', 'sold');

    INSERT INTO Customers (customer_name, phone_number, email, customer_type)
    VALUES ('Sergey Pavlov', '+79991234567', 'sergei@mail.com', 'purchaser'),
           ('Elena Kuznetsova', '+79992345678', 'elena@mail.com', 'renter');

    INSERT INTO Transactions (property_id, customer_id, transaction_date, transaction_type, final_price)
    VALUES (1, 1, '2025-01-20', 'purchase', 11800000),
           (2, 2, '2024-12-10', 'rent', 150000);
    """
    execute_query(connection, insert_data_query)

# Functions for working with queries
def get_properties_for_sale():
    connection = create_connection(DATABASE)
    query = """
    SELECT property_type, size, price, num_bedrooms, num_bathrooms, city, district
    FROM Properties
    JOIN Locations ON Properties.location_id = Locations.location_id
    WHERE status = 'on sale';
    """
    return fetch_query(connection, query)

def get_transactions():
    connection = create_connection(DATABASE)
    query = """
    SELECT Customers.customer_name, Properties.property_type, Transactions.final_price, Transactions.transaction_date
    FROM Transactions
    JOIN Customers ON Transactions.customer_id = Customers.customer_id
    JOIN Properties ON Transactions.property_id = Properties.property_id
    WHERE transaction_type = 'покупка';
    """
    return fetch_query(connection, query)

def get_properties_in_city(city):
    connection = create_connection(DATABASE)
    query = f"""
    SELECT property_type, size, price, num_bedrooms, num_bathrooms
    FROM Properties
    JOIN Locations ON Properties.location_id = Locations.location_id
    WHERE city = '{city}';
    """
    return fetch_query(connection, query)

def get_agents():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT agent_name, phone_number, email, agency_name FROM agents')
    agents = cursor.fetchall()
    conn.close()
    return agents


if __name__ == '__main__':
    init_db()

