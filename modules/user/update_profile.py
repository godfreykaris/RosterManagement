
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

        
        return self.update_user_profile(data, user_level)
    

    def update_user_profile(self, data, user_level):
        user_id = data.get('user_id')

        if not self.is_valid_user_level(user_level):
            return error_response('Unauthorized operation.', 500)

        # Validate input and get user details or an error that can be returned
        user_data, error = self.validate_and_get_user_data(data, user_level)

        if not user_data:
            return error_response(error, 400)

        # Check for an existing record
        exists, found_user_level, error = self.is_existing_record(user_data, user_id)
        if exists:
            return error_response(error, 400)

        # Construct and execute the update query
        update_query, params, error = self.build_update_query(user_data, user_level, found_user_level, user_id)
        if error:
            return  error_response(error, 500)
        
        success = self.execute_update_query(update_query, params)

        if success:
            return success_response('User updated successfully.', 200)
        else:
            return error_response('An internal error occurred. Please contact support.', 500)

    def is_valid_user_level(self, user_level):
        return user_level in [1, 2, 3]

    def validate_and_get_user_data(self, data, user_level):
        # Initialize an empty dictionary to store validated parameters
        user_data = {}

        # Extract and validate each parameter
        user_id = data.get('user_id')
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
        if not weight and user_level != 3: # Wrestler and coach must provide weight
            missing_fields.append('weight')
        if not name:
            missing_fields.append('name')        
        if not address:
            missing_fields.append('address')

        if password and not confirm_password:
            missing_fields.append("confirm password")
        
        if confirm_password and not password:
            missing_fields.append("password")

        # If user_level is 2 (Coach), validate the 'team' field
        if user_level == 2 and not team:
            missing_fields.append("team")

        if missing_fields:
            return None, error_response(f'Missing or invalid fields: {", ".join(missing_fields)}', 400)

    
        # If all validations pass, populate the params dictionary
        user_data['user_id'] = user_id
        user_data['username'] = username
        user_data['email'] = email
        user_data['name'] = name
        user_data['address'] = address
        user_data['weight'] = weight

        if user_level == 2:
            user_data['team'] = team  # Add 'team' if user_level is 2

        # Return the validated parameters as a dictionary
        return user_data, None

    def is_existing_record(self, user_data, user_id):
        
        select_query =  "SELECT user_id, email, username, user_level FROM users WHERE  email = %s OR username= %s;"
        params = (user_data['email'], user_data['username'])
        fetch = True # we are fetching data
        fetchall = False # fetch only one record
        existing_record = self.database_initializer.perform_database_operation(select_query, params, fetch, fetchall)

        # Was a record with the same details found?
        if existing_record and existing_record[0] != user_id:
            # Make sure the username and email are unique
            if existing_record[1] == user_data['email']:
                return True, None, 'The email is taken'
            else:
                return True, None, 'The username is taken'
        
        # Get the record of the found user level for use when users 
        # update profiles of other users e.g. Coach updating wrestler
        
        found_user_level = existing_record[0]

        return False, found_user_level, None

    def build_update_query(self,user_data, current_user_level, user_being_updated_level, user_id):
          if current_user_level < user_being_updated_level:            
            logging.error('An error occurred during profile update: Unauthorized attempt to update wrestler profile by level %s user for user_id %s',current_user_level, user_id)
            return None, None, 'An internal error occurred. Unauthorized operation. Please contact support.'
        
          # Prepare the query and parameters
          if current_user_level == user_being_updated_level:
              if user_data['password']: # User updating profile as well as changing their password
                  if current_user_level == 3: # Admin
                      update_query = "UPDATE users SET username = %s, email = %s, name = %s, address = %s, password_hash = %s WHERE user_id = %s;"
                      params = (user_data['username'], user_data['email'], user_data['name'], user_data['address'] ,generate_password_hash(user_data['password']), user_id)
                  else:
                      update_query = "UPDATE users SET username = %s, email = %s, weight = %s, name = %s, address = %s, password_hash = %s WHERE user_id = %s;"
                      params = (user_data['username'], user_data['email'], user_data['weight'], user_data['name'], user_data['address'] ,generate_password_hash(user_data['password']), user_id)
              else: # User updating profile but not changing password
                  if current_user_level == 3: # Admin
                      update_query = "UPDATE users SET username = %s, email = %s, name = %s, address = %s, WHERE user_id = %s;"
                      params = (user_data['username'], user_data['email'], user_data['name'], user_data['address'], user_id)
                  else:
                      update_query = "UPDATE users SET username = %s, email = %s, weight = %s, name = %s, address = %s, WHERE user_id = %s;"
                      params = (user_data['username'], user_data['email'], user_data['weight'], user_data['name'], user_data['address'], user_id)
          else: # Coach updating the wrestler profile or admin updating coach profile
              update_query = "UPDATE users SET username = %s, email = %s, weight = %s, name = %s, address = %s, team = %s WHERE user_id = %s;"
              params = (user_data['username'], user_data['email'], user_data['weight'], user_data['name'], user_data['address'] , user_data['team'], user_id)
          
          return update_query, params, None          
          

    def execute_update_query(self, query, params):
        fetch = False # we are updating data
        fetchall = False # we are updating datas
        update_status = self.database_initializer.perform_database_operation(query, params, fetch, fetchall)
          
        return update_status
    