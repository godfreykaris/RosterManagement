import random
import string
import logging
import psycopg2

from flask_mail import Message
from flask import request

from shared import error_response, success_response
from werkzeug.security import generate_password_hash

class PasswordReset:
    def __init__(self, mail):
        self.mail = mail
        
    # Generate a new password for the user
    @staticmethod # doesn't depend on instance specific attributes
    def generate_password(length):
        # Define character sets for password generation
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = "!@#$%^&*()_+=-[]{}|:;<>,.?/~"

        # Ensure that the password length is at least 8 characters
        if length < 8:
            length = 8

        # Combine character sets
        all_chars = lowercase + uppercase + digits + special_chars

        # Generate a password with random characters
        password = ''.join(random.choice(all_chars) for _ in range(length))

        return password

    # Send a new password to the user
    def send_password_reset_email(self, email, new_password, user_name):
        try:
            # Create a message object for the email
            msg = Message('Password Reset Instructions', recipients=[email])

            # Customize the email content with the temporary password
            msg.body = f'Dear {user_name},\n\nWe recently received a request to reset the password for your Roster account. To help ensure the security of your account, we have generated a temporary password for you to use:\n\nTemporary Password: {new_password}\n\nPlease follow these steps to reset your password:\n\n1. Go to the Roster login page\n2. Enter your email and the temporary password in their respective fields.\n\nFor security reasons, we recommend that you change your password immediately after logging in. If you did not request a password reset or have any concerns about the security of your account, please contact our support team immediately.\n\nThank you for choosing Roster for your needs. We apologize for any inconvenience this may have caused and appreciate your understanding as we work to ensure the security of your account.\n\nBest regards,\nRoster'

            # Send the email
            self.mail.send(msg)

        except Exception as e:
            return error_response('An error occurred while sending the email', 400)
        
        
    def reset_password(self):
        try:
            data = request.get_json()
            email = data.get('email')

            # Check if email and phone_number are provided
            if not email:
                return error_response('Invalid input data', 400)            
            
            # Check if the user exists in the database
            user_query = """
                SELECT name
                FROM users
                WHERE email = %s
            """            
            params = (email,)
            fetch = True  # We are fetching data
            fetchall = False  # Fetch all records
            user = self.database_initializer.perform_database_operation(user_query, params, fetch, fetchall)
        
            if not user:
                return error_response('User not found!', 400)
            
            user_name = user[0]

            # Generate a new password
            new_password = self.generate_password(8)
            new_pswd_hash = generate_password_hash(new_password)
            
            # Update the user's password in the database
            update_password = """
                UPDATE users
                SET password_hash = %s
                WHERE email = %s
            """

            params = (new_pswd_hash, email,)
            fetch = False  # We are fetching data
            fetchall = False  # Fetch all records
            
            if not self.database_initializer.perform_database_operation(update_password, params, fetch, fetchall):
                return error_response('Failed to update password', 500)
            
            # Send password reset email
            try:
                self.send_password_reset_email(email, new_password, user_name)
            except Exception as e:
                logging.error(f"Failed to send password reset email: {str(e)}")
                return error_response('Failed to send password reset email', 500)
            
            return success_response('Password reset was successful', 200)
        
        except psycopg2.Error as e:
            return error_response('Network error while trying to reset password', 500)

            
