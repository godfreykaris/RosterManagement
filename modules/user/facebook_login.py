from dotenv import load_dotenv
load_dotenv()

from flask import request, redirect
import facebook

import os

class FacebookAuth:
    def __init__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        # Facebook Oauth Config
        self.FACEBOOK_CLIENT_ID = os.getenv('FACEBOOK_CLIENT_ID')
        self.FACEBOOK_CLIENT_SECRET = os.getenv('FACEBOOK_CLIENT_SECRET')
        self.authorization_base_url = os.getenv('FACEBOOK_AUTHORIZATION_BASE_URL')
        self.token_url = os.getenv('FACEBOOK_TOKEN_URL')
        self.redirect_uri = os.getenv('FACEBOOK_REDIRECT_URI')
        self.api_version = os.getenv('FACEBOOK_API_VERSION')
        
    def login(self):
        redirect_uri = facebook.GraphAPI().get_auth_url(self.FACEBOOK_CLIENT_ID, self.FACEBOOK_CLIENT_SECRET, self.redirect_uri)
        return redirect(redirect_uri)
    
    def callback(self):
        global access_token
        code = request.args.get('code')
        access_token = facebook.GraphAPI().get_access_token_from_code(code, self.FACEBOOK_CLIENT_ID, self.FACEBOOK_CLIENT_SECRET, self.redirect_uri, self.api_version)
        
        if not access_token:
            return 'Access token not obtained. Login failed.'
        
        # Retrieve user name and ID
        graph = facebook.GraphAPI(access_token=access_token['access_token'], version=self.api_version)
        me = graph.get_object('me',)
        
        print(graph)
        id = me['id']
        name = me['name']
        
        print(id)
        print(name)
        
        redirect("/")
