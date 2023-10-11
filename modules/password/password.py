import random
import string

import app

from flask_mail import Mail, Message
from flask import jsonify

mail = Mail(app)

class PasswordReset:
    #generate new password for user
    def generate_password(length):
        #definne character set for password generation
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = "!@#$%^&*()_+=-[]{}|:;<>,.?/~"

        #ensure that password length is atleast 8 chars
        if length < 8:
            length = 8

        #combine character sets
        all_chars = lowercase + uppercase + digits + special_chars

        #generate password with random chars
        password = ''.join(random.choice(all_chars) for _ in range(length))

        return password

    #send new password to user
    def send_password_reset_email(email, new_password, user_name):
        try:
            # Create a message object for the email
            msg = Message('Password Reset Instructions', recipients=[email])  # Use the provided email parameter

            # Customize the email content with the temporary password
            msg.body = f'Dear {user_name},\n\nWe recently received a request to reset the password for your Kindle Notepad account. To help ensure the security of your account, we have generated a temporary password for you to use:\n\nTemporary Password: {new_password}\n\nPlease follow these steps to reset your password:\n\n1. Go to the Kindle Notepad login page \n2. Enter email, then the temporary password in their respective fields. \n\nFor security reasons, we recommend that you change your password immediately after logging in. If you did not request a password reset or have any concerns about the security of your account, please contact our support team immediately.\n\nThank you for choosing Kindle Notepad for your needs. We apologize for any inconvenience this may have caused and appreciate your understanding as we work to ensure the security of your account.\n\nBest regards,\n Kindle Notepad'

            # Send the email
            mail.send(msg)

        except Exception as e:
            return jsonify({'error': 'Failed to send password reset email'}), 500