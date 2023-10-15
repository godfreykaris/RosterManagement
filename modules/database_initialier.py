import os
import logging
import traceback

from flask import jsonify

import psycopg2
from psycopg2 import OperationalError

from dotenv import load_dotenv

from shared import error_response

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
            logging.error(f'Could not connect to the database:  {str(e)}, Traceback: {traceback.format_exc()}')
            return error_response("An internal error occurred. Please contact support.", 500)
    
    def perform_database_operation(self, query, params=None, fetch=False, fetchall=False):
        try:
            with self.get_database_connection() as database_connection:
            
                cursor = database_connection.cursor()
                cursor.execute(query, params)
                if fetch:
                    if fetchall:
                        result = cursor.fetchall()  # Fetch all records
                    else:
                        result = cursor.fetchone()  # Fetch one record
                    return result
                else:
                    try:
                        affected_rows = cursor.fetchall()
                    except psycopg2.ProgrammingError:
                        affected_rows = ()

                    database_connection.commit()
                return True, affected_rows
        except Exception as e:
            logging.error(f'An error occurred during database operation: {str(e)}, Traceback: {traceback.format_exc()}')
            return False, None
        finally:
            if not fetch:
                cursor.close()
                database_connection.close()
