
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


def is_duplicate_record(database_initializer, user_data, user_id=None): #user_id is provided during update
    select_query = "SELECT user_id, email, username, user_level FROM users WHERE email = %s OR username = %s;"
    params = (user_data['email'], user_data['username'])
    fetch = True  # we are fetching data
    fetchall = False  # fetch only one record
    existing_record = database_initializer.perform_database_operation(select_query, params, fetch, fetchall)

    # If a record with the same details is found
    if existing_record:
        # If user_id is provided and it matches the found record, no conflict
        if user_id and existing_record[0] == user_id:
            return False, None, None

        # Make sure the username and email are unique
        if existing_record[1] == user_data['email']:
            return True, None, 'The email is taken'
        else:
            return True, None, 'The username is taken'

    return False, None, None


def team_exists(database_initializer, team_name):
    select_query = "SELECT team_id FROM teams WHERE name = %s;"
    params = (team_name,)
    fetch = True  # we are fetching data
    fetchall = False  # fetch only one record
    existing_record = database_initializer.perform_database_operation(select_query, params, fetch, fetchall)

    # Was the team found
    if existing_record:
        found_team_id = existing_record[0]
        return True, found_team_id

    return False, None

def add_team(database_initializer, team_name):
    insert_query = "INSERT INTO teams (name) VALUES (%s) RETURNING team_id;"
    params = (team_name,)
    
    return database_initializer.perform_database_operation(insert_query, params, fetch=False, fetchall=False)
