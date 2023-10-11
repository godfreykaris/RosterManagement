from flask import jsonify, request
from werkzeug.security import check_password_hash

class UserLogin:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer
        
    def login_user(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        
        if not email or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        
        try:
            # query the atabase to check if the user exists and verify the password
            database_connection = self.database_initializer.get_database_connection()
            cursor = database_connection.cursor()
            
            cursor.execute("SELECT user_id, email, password_hash FROM users WHERE email = %s;", (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[2], password):
                # Authentication successful
                return jsonify({'message': 'Login successful', 'user_id': user[0], 'status': 200})
            else:
                # Authentication failed
                return jsonify({'message': 'Authentication failed', 'status': 401})
            
        except Exception as e:
            print("Error", {e})
            #return jsonify({'message': 'Login failed', 'error': str(e)}), 500
            return jsonify({'message': str(e), 'error': str(e), 'status': 500}) # For testing only
        
        finally:
            cursor.close()
            database_connection.close()