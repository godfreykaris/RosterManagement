from dotenv import load_dotenv
load_dotenv()

import os
import pathlib

import requests
from flask import session, abort, redirect, request
from flask_cors import CORS

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

class GoogleAuth:
    def __init__(self, app):
        self.app = app
        CORS(self.app, resources={r"/*": {"origins": "http://localhost:3000"}})
        
        self.app.secret_key = os.getenv('GOOGLE_CLIENT_SECRET')        
        self.GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
        
        client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secrets.json")
        
        self.flow = Flow.from_client_secrets_file(
            client_secrets_file=client_secrets_file,
            scopes=[os.getenv('GOOGLE_AUTHORIZATION_URL'), os.getenv('GOOGLE_AUTHORIZATION_URL1'), "openid"],
            redirect_uri=os.getenv('GOOGLE_REDIRECT_URI')
        )

    def login(self):
        authorization_url, state = self.flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)

    def callback(self):
        self.flow.fetch_token(authorization_response=request.url)
        
        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match
            
        credentials = self.flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)
        
        id_info = id_token.verify_oauth2_token(
            id_token=credentials.id_token,
            request=token_request,
            audience=self.GOOGLE_CLIENT_ID
        )
        
        print("ID INFO: ", id_info)
        
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        
        return redirect("/")
