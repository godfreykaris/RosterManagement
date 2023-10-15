
import email_validator
from flask import jsonify

def validate_email_format(email):
    try:
        email_validator.validate_email(email)
        return True
    except email_validator.EmailNotValidError:
        return False

def success_response(message, status_code=200):
    return jsonify({'message': message}), status_code

def error_response(message, status_code=500):
    return jsonify({'error': message}), status_code
