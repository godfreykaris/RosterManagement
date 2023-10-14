import random
import string

from flask_mail import Message
from flask import jsonify

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
            return jsonify({'message': 'An error occurred while sending the email'})
