
from flask import jsonify, request
from werkzeug.security import generate_password_hash

from shared import validate_email_format,success_response, error_response, is_duplicate_record, team_exists, add_team


class UserRegistration:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    def register_user(self):
        data = request.get_json()
        user_level = data.get('user_level') # Coach: 2, or Wrestler: 1
        team_name = data.get('team_name') # Wrestlers and coaches must associate with a team
        username = data.get('username')        
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validate user role
        if not user_level or user_level not in [1, 2]:
           return error_response('Invalid user role.', 400)

        # Check for missing or empty fields
        missing_fields = []
        if not username:
            missing_fields.append('username')
        if not email:
            missing_fields.append('email')
        if not password:
            missing_fields.append('password')
        if not confirm_password:
            missing_fields.append('confirm password')        
        if not user_level:
            missing_fields.append('user role')     
        if not team_name:
            missing_fields.append('team name')
        
        if missing_fields:
            return error_response(f'Missing fields or invalid: {", ".join(missing_fields)}', 400)
        
         # Validate the email format
        if not validate_email_format(email):
            return error_response('Invalid email format', 400)
        
        # Make sure the password is confirmed correctly
        if password != confirm_password:
            return error_response('Password confirmation failed', 400)

        # Check for an duplicate record
        exists, found_user_level, error = is_duplicate_record(self.database_initializer, {'email': email, 'username': username })
        if exists:
            return error_response(error, 400)

        added_team_id = None  # Declare added_team_id with a default value for a coach adding a new team

        # Check if the team exists
        exists, found_team_id = team_exists(self.database_initializer, team_name)

        if not exists:
            if user_level == 1:
                return error_response("Invalid team selected", 400)
            else:
                # Insert the team for the coach
                insert_status, affected_rows = add_team(self.database_initializer, team_name)

                if not insert_status:
                    return error_response("An error occurred while adding new team. Please contact support if the issue persists.", 500)
                else:
                    # initiallize the new team id to be added in the team_coach junction table later
                    added_team_id = affected_rows[0][0]
        
        # Insert the user record
        insert_query = "INSERT INTO users (username, email, team_id, password_hash) VALUES (%s, %s, %s, %s) RETURNING user_id;"
        if added_team_id: # The coach is using an existing team or it is a wrestler registering
            params = (username,email, added_team_id ,generate_password_hash(password),)
        else:
            params = (username,email, found_team_id ,generate_password_hash(password),)

        insert_status, affected_rows = self.database_initializer.perform_database_operation(insert_query, params, fetch=False, fetchall=False)

        if not insert_status:
            return error_response("An internal error occurred while registering. Please contact support if the issue persists.", 500)
        else:
            # initiallize the new team id to be added in the team_coach junction table later
            added_user_id = affected_rows[0][0]
        
        # Inser a record in the team_coach junction table for the coach and their team
        if user_level == 2:
            if not added_team_id: # The coach is using an existing team
                 params = (found_team_id, added_user_id,)
            else:
                 params = (added_team_id, added_user_id,)

            insert_query = "INSERT INTO team_coach (team_id, coach_id) VALUES (%s, %s);"
            insert_status = self.database_initializer.perform_database_operation(insert_query, params, fetch=False, fetchall=False)

            if not insert_status:
                return error_response("An internal error occurred setting up the team coach. Please contact support if the issue persists.", 500)
        
        
        return success_response('User registered successfully', 200)
        
        