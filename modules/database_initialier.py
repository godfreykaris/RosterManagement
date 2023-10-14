import os
import psycopg2
from psycopg2 import OperationalError

from dotenv import load_dotenv

class DatabaseInitializer:
    def get_database_connection(self):
        try:
            load_dotenv()
            
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            
            return conn
        
        except OperationalError as e:
            print(f"Error: {e}")
            print("PostgreSQL connection failed")