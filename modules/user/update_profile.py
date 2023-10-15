
from flask import jsonify, request
from werkzeug.security import generate_password_hash

import logging

from shared import validate_email_format, success_response, error_response

class UpdateProfile:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer


    def update_profile(self):
        data = request.get_json()
        user_level = data.get('user_level')

        if not user_level:
            return error_response('Missing or invalid user level.', 400)
        
        try:
            user_level = int(user_level)
        except ValueError:
            return error_response('User level must be a valid integer.', 400)

        if user_level == 1:
            return self.update_wrestler_profile(data, user_level)
        return self.update_wrestler_profile(data, user_level)
    
    def update_wrestler_profile(self, data, user_level):

        user_id = data.get('user_id')

        if user_level != 2 and user_level != 1:            
            logging.error('An error occurred during profile update: Unauthorized attempt to update wrestler profile by level %s user for user_id %s',user_level, user_id)
            return error_response('An internal error occurred. Unauthorized operation. Please contact support.', 500)
        
        username = data.get('username')
        email = data.get('email')
        name = data.get('name')
        address = data.get('address')
        weight = data.get('weight')
        team = data.get('team')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Check for missing or empty fields
        missing_fields = []
        if not user_id:
            missing_fields.append('user id')
        if not username:
            missing_fields.append('username')
        if not email:
            missing_fields.append('email')
        if not weight:
            missing_fields.append('weight')
        if not name:
            missing_fields.append('name')        
        if not address:
            missing_fields.append('address')

        if password and not confirm_password:
            missing_fields.append("confirm password")
        
        if confirm_password and not password:
            missing_fields.append("password")

        # If it is a coach, they must place the user in a team
        if user_level == 2 and not team:
            missing_fields.append("team")

        if missing_fields:
            return error_response(f'Missing fields: {", ".join(missing_fields)}', 400)
        
        # Validate the email format
        if not validate_email_format(email):
           return error_response("Invalid email format.", 400)
        
        # Make sure the password is confirmed correctly
        if password and password != confirm_password:
            return error_response("Password confirmation failed.", 400)

        #*********** Check for an existing record *************#
        
        select_query =  "SELECT user_id, email, username FROM users WHERE  email = %s OR username= %s AND user_id != %s;"
        params = (email, username, user_id)
        fetch = True # we are fetching data
        fetchall = False # fetch only one record
        existing_record = self.database_initializer.perform_database_operation(select_query, params, fetch, fetchall)

        # Was a record with the same details found?
        if existing_record and existing_record[0] != user_id:
            # Make sure the username and email are unique
            if existing_record[1] == email:
                return error_response('The email is taken', 400)
            else:
                return error_response('The username is taken', 400)
        
        #************* End of existing recrd checking *************#


        #******************* Perform the update **************#

        # Prepare the query and parameters
        if user_level == 3:
            if password: # Wrestler updating profile as well as changing their password
                update_query = "UPDATE users SET username = %s, email = %s, weight = %s, name = %s, address = %s, password_hash = %s WHERE user_id = %s;"
                params = (username, email, weight, name, address ,generate_password_hash(password), user_id)
            else: # Wrestler updating profile but not changing password
                update_query = "UPDATE users SET username = %s, email = %s, weight = %s, name = %s, address = %s, WHERE user_id = %s;"
                params = (username, email, weight, name, address, user_id)
        elif user_level == 2: # Coach updating the wrestler profile
            update_query = "UPDATE users SET username = %s, email = %s, weight = %s, name = %s, address = %s, team = %s WHERE user_id = %s;"
            params = (username, email, weight, name, address , team, user_id)
        
        fetch = False # we are updating data
        fetchall = False # we are updating data
        update_status = self.database_initializer.perform_database_operation(update_query, params, fetch, fetchall)

        if update_status:
            return success_response('User updated successfully.', 200)
        else:
            return error_response('An internal error occurred. Please contact support.', 500)

        #******************* End of update *****************#
        