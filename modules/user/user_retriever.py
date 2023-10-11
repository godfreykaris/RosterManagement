import json

class UserHandler:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer
        
    def get_user(self, user_id):
        try:
            if not user_id:
                return json.dumps({'message': 'Invalid user ID'}), 400
            
            database_connection = self.database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            # Retrieve the user's information based on user_id
            cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                # If the user exists, return their information as JSON
                
                user_role = user_data['role']
                
                if user_role == 'admin':
                    user_info = {
                    'user_id' : user_data['user_id'],
                    'name': user_data['name'],
                    'email': user_data['email'],
                    }
                elif user_role == 'coach':
                    user_info = {
                    'user_id' : user_data['user_id'],
                    'name': user_data['name'],
                    'email': user_data['email'],
                    'teams':user_data['teams'],
                    }
                else:
                    user_info = {
                    'user_id' : user_data['user_id'],
                    'name': user_data['name'],
                    'email': user_data['email'],
                    'weight_class':user_data['weight_class'],
                    'user_team':user_data['team']
                    }
                
                return json.dumps({'message': 'User retrieved successfully', 'user_info': user_info})
            else:
                return json.dumps({'message': 'User not found'}), 404
        
        except Exception as e:
            # Handle database errors or other exceptions
            return json.dumps({'message': str(e), 'error': str(e)}), 500
        finally:
            cursor.close()
            database_connection.close()