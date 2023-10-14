import os
import json
import psycopg2
import logging

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from datetime import timedelta
from flask_login import LoginManager, UserMixin, current_user, login_required,  login_user, logout_user
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_mail import Mail
from werkzeug.security import generate_password_hash

# custom module imports
from modules.database_initialier import DatabaseInitializer
from modules.user.login import UserLogin
from modules.user.register import UserRegistration
from modules.user.user_retriever import UserHandler
from modules.password.password import PasswordReset

# Import Facebook and Google login classes
from modules.user.facebook_login import FacebookAuth
from modules.user.google_login import GoogleAuth

# create a flask application
app = Flask(__name__)

mail = Mail(app)

app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_key",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",  
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.needs_refresh_message = (u"Session timedout, please login again")
login_manager.needs_refresh_message_category = "info"

# csrf = CSRFProtect(app) For Testing only

app.config['PARMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# set the static folder relative to the project directory
static_folder_path = os.path.join(os.path.dirname(__file__), 'roster-react', 'build')
app.static_folder = static_folder_path

#configure flask-mail for sending emails
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')  # Use your email provider's mail server
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')  # Port for mail server
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')  # Use TLS encryption
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Your email address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')  # Default sender for emails

# Initialize FacebookLogin and GoogleLogin
facebook_auth = FacebookAuth()
google_auth = GoogleAuth(app=app)

#initialize the database connection
database_initializer = DatabaseInitializer()
password_reset = PasswordReset(mail)

# Start
@app.route('/')
def hello():
    root_url = request.url_root
    return "Hello World <a href='/google/'><button>Login</button></a>"
    # return render_template('index.html', root_url=root_url)

# Normal Login start
class User(UserMixin):
    def __init__(self, id):
        self.id = id
    
    def get_id(self):
        return str(self.id)
    

@login_manager.user_loader
def load_user(id:int):
    user_handler = UserHandler(database_initializer)
    response = user_handler.get_user(id)
    
    try:
        response_data = json.loads(response)
        user_info = response_data.get('user_info')
        
        if user_info:
            user_model = User(id=user_info['user_id'])
            return user_model
    
    except json.JSONDecodeError:
        # handle the case where the response is not a valid JSON
        return None
    
    return None

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    try:
        # Create an instance of UserLogin with the database connection
        user_authenticator = UserLogin(database_initializer=database_initializer)
        # Call the login_user method to handle user login
        result = user_authenticator.login_user()
        status = result.json['status']
        if status == 200:
            response_data = result.json
            # Access specific properties from the response
            user_id = response_data['user_id']
            # Use Flask-Login's login_user function to set the current_user
            login_user(User(int(user_id), ""))

        return result, status
    
    except Exception as e:
        print(str(e))
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500
    
# Normal Login end

# Google auth start  
@app.route('/google/', methods=['GET', 'POST'])
def google():
    return google_auth.login()

@app.route('/google/auth/')
def google_auth_route():
    return google_auth.callback()

# Google auth end

# Facebook auth start
@app.route('/facebook/', methods=['POST', 'GET'])
def facebook():
    return facebook_auth.login()

@app.route('/facebook/auth/', methods=['POST'])
def facebook_auth_route():
    return facebook_auth.callback()

# Facebook auth start

# route for user logout
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('/'))


# reset password
@app.route('/api/reset_password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        email = data.get('email')
        
        # Check if email and phone_number are provided
        if not email:
            return jsonify({'message': 'Invalid input data'}), 400
        
        
        # Get a database connection using a context manager
        with database_initializer.get_database_connection() as conn:
            with conn.cursor() as cursor:
                # Check if the user exists in the database
                user_query = """
                    SELECT name
                    FROM users
                    WHERE email = %s
                """
                cursor.execute(user_query, (email,))
                user = cursor.fetchone()
                
                if not user:
                    return jsonify({'message': 'User not found!'}), 404
                
                user_name = user[0]
                
                # Generate a new password
                new_password = password_reset.generate_password(8)
                new_pswd_hash = generate_password_hash(new_password)
                
                # Update the user's password in the database
                update_password = """
                    UPDATE users
                    SET password_hash = %s
                    WHERE email = %s
                """
                cursor.execute(update_password, (new_pswd_hash, email,))
                
                # Commit the transaction
                conn.commit()
                
                if cursor.rowcount == 0:
                    return jsonify({'message': 'Failed to update password'}), 500
                
                # Send password reset email
                try:
                    password_reset.send_password_reset_email(email, new_password, user_name)
                except Exception as e:
                    logging.error(f"Failed to send password reset email: {str(e)}")
                    return jsonify({'error': 'Failed to send password reset email'}), 500
                
                return jsonify({'message': 'Password reset was successful'}), 200
    
    except psycopg2.Error as e:
        return jsonify({'error': 'Network error while trying to reset password'}), 500


# route for user registration
@app.route('/api/register', methods=['POST'])
def register():
    try:
        userRegistrar = UserRegistration(database_initializer=database_initializer)
        return userRegistrar.register_user()
    
    except Exception as e:
        logging.error('An error occurred during registration: %s', str(e))
        return jsonify({'error': 'An error occurred during registration.'}), 500


if __name__ == '__main__':
    app.run(debug=True)