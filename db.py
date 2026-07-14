import mysql.connector
from mysql.connector import Error

def get_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='cognixia_bank',
            user='root',
            password='abc123'
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    
connection = get_connection()

if connection is not None:
    print("Connection to MySQL database established successfully.")
    connection.close()
