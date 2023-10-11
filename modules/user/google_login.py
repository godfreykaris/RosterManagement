import os
import pathlib

from dotenv import load_dotenv
load_dotenv()

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" #to allow Http traffic for local development

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
client_secret_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401) #Authorization required
        else:
            return function()
    return wrapper

# google login route
@app.route('/google_login')
def login():
    authrization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authrization_url)


# The function called after google has authenticated the user
@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    
    if not session["state"] == request.args["state"]:
        abort(500) # state does not match
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    
    return redirect("/protected_area")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")