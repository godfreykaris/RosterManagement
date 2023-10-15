import os
import logging
from flask import jsonify

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
            # Log the error for debugging purposes
            logging.error('Could not connect to the database: %s', str(e))
            return jsonify({'message': 'An internal error occurred. Please contact support.'}), 500