import json
import logging
import traceback

from shared import error_response, success_response

class UserHandler:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer
     
    ############# Fetch data start #############     
    # Fetch a single user data   
    def get_user(self, user_id):
        try:
            if not user_id:
                return error_response('Invalid user ID', 400)           
                
            user_query = """
                SELECT user_level
                FROM users
                WHERE user_id = %s
            """
            # fetch user role for the given user_id                                  
            params = (user_id,)
            fetch = True # we are not fetching data
            fetchall = False # fetch one record
            user_level = self.database_initializer.perform_database_operation(user_query, params, fetch, fetchall)
            
            if not user_level:
                return error_response('User does not exist or there was an issue sending the request', 404)
            
            # variable to hold user data
            user_info = None
            
            # fetch user data based on the returned user level
            if user_level[0] == 1:
                admin_query = """
                    SELECT user_level, name, email, address
                    FROM users
                    WHERE user_id = %s 
                """
                params = (user_id,)
                fetch = True # we are not fetching data
                fetchall = False # fetch one record
                user_info = self.database_initializer.perform_database_operation(admin_query, params, fetch, fetchall)                    
            elif user_level[0] == 2:
                coach_query = """
                    SELECT
                        u.user_id AS coach_id,
                        u.name AS coach_name,
                        u.email AS coach_email,
                        u.team_id AS coach_team,
                        u.address AS coach_address,
                        u.user_level AS coach_user_level
                        t.name,
                        t.team_id
                    FROM users u
                    LEFT JOIN teams t ON u.team_id = t.team_id
                    WHERE u.user_id = %s
                """
                params = (user_id,)  # Use a tuple with the user_id to fetch
                fetch = True  # We are fetching data
                fetchall = False  # Fetch one record
                user_info = self.database_initializer.perform_database_operation(coach_query, params, fetch, fetchall)
            else:
                wrestler_query = """
                    SELECT user_level, name, username, email, weight, weight_class, team, address  
                    FROM users
                    WHERE id = %s 
                """
                params = (user_id,)
                fetch = True # we are not fetching data
                fetchall = False # fetch one record
                user_info = self.database_initializer.perform_database_operation(wrestler_query, params, fetch, fetchall)
            
            return json.dumps({'user_info': user_info})
        
        except Exception as e:
            # Handle database errors or other exceptions
            # Log the error for debugging purposes
            logging.error(f'Could not connect to the database:  {str(e)}, Traceback: {traceback.format_exc()}')
            return error_response("An internal error occurred. Please contact support.", 500)
     
     # fetch all coaches       
    def get_coaches(self):
        coach_query = """
            SELECT
                u.user_id AS coach_id,
                u.name AS coach_name,
                u.email AS coach_email,
                u.team_id AS coach_team,
                u.address AS coach_address,
                u.user_level AS coach_user_level
                t.name,
                t.team_id
            FROM users u
            LEFT JOIN teams t ON u.team_id = t.team_id
            WHERE u.user_level = %s
        """
        
        params = (2,)
        fetch = True  # We are fetching data
        fetchall = True  # Fetch all records
        coaches = self.database_initializer.perform_database_operation(coach_query, params, fetch, fetchall)
        
        if not coaches:
            return error_response('Failed to fetch coaches', 500)
                
        return coaches 
    
    # fetch all wrestlers for a specific team
    def get_wrestlers(self, team_id):
        wrestler_query = """
            SELECT user_level, name, username, email, weight, team_id, address
            FROM users
            WHERE team_id = %s AND user_level = %s
        """
        
        params = (team_id, 3,)
        fetch = True  # We are fetching data
        fetchall = True  # Fetch all records
        wrestlers = self.database_initializer.perform_database_operation(wrestler_query, params, fetch, fetchall)
        
        if not wrestlers:
            return error_response(f'Failed to fetch wrestlers for team {team_id}', 500)
                
        return wrestlers    
    
    ############## Fetch data end ##################
    
    
    ############## Delete Records start #############
    
    ############# Delete a coach ####################
    def delete_user(self, user_id):        
        if not user_id:
            return error_response('Invalid user id', 400)
        
        delete_query = """
            DELETE
            FROM users
            WHERE user_id = %s
        """        
        params = (user_id,)
        fetch = False  # We are fetching data
        fetchall = False  # Fetch all records
        
        if self.database_initializer.perform_database_operation(delete_query, params, fetch, fetchall):
            return success_response('Deleted successfully!', 200)
        
        return error_response('Error deleting user', 500)   
    
    ############## Delete Records end ##################"