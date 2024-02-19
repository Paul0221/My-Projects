import mysql.connector
from enrolmentApp.config import DB_CONFIG

def connect_to_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

connection = connect_to_database()