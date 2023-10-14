
from flask import jsonify, request
from werkzeug.security import generate_password_hash
import email_validator

import logging

class UserRegistration:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    def register_user(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')

        # Check for missing or empty fields
        missing_fields = []
        if not username:
            missing_fields.append('username')
        if not email:
            missing_fields.append('email')
        if not password:
            missing_fields.append('password')
        if not confirmPassword:
            missing_fields.append('confirmPassword')
        
        if missing_fields:
            return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
         # Validate the email format
        try:
            email_validator.validate_email(email)
        except email_validator.EmailNotValidError:
            return jsonify({'message': 'Invalid email format'}), 400
        
        # Make sure the password is confirmed correctly
        if password != confirmPassword:
            return jsonify({'message': 'Password confirmation failed'}), 400


        try:

            # Acquire the database connection from the database initializere
            with self.database_initializer.get_database_connection() as database_connection:

                cursor = database_connection.cursor() 

                # Check if a record with the provided  email exists
                cursor.execute("SELECT user_id, email, username FROM users WHERE  email = %s OR username= %s;", (email, username))
                existing_record = cursor.fetchone()

                # Was a record with the same details found?
                if existing_record:
                    # Make sure the username and email are unique
                    if existing_record[1] == email:
                        return jsonify({'message': 'The email is taken'}), 400   
                    else:
                        return jsonify({'message': 'The username is taken'}), 400   
    
                else:
                    # No existing record found; insert a new one
                    insert_query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s);"
                    cursor.execute(insert_query, (username, email, generate_password_hash(password)))

                database_connection.commit()
            
            return jsonify({'message': 'User registered successfully'}), 200

        except Exception as e:
            # Log the error for debugging purposes
            logging.error('An error occurred during registration: %s', str(e))
            return jsonify({'message': 'An error occured. Please contact support.'}), 500
        finally:
            cursor.close()
            database_connection.close()