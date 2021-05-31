import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import spotipy.util as util
from secrets import client_id, client_secret, username, redirect_uri
from SpotipyToken import SpotipyToken

class SpotipyRegToken:
    token = None
    def __init__(self):
        scope = 'user-library-read'
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.redirect_uri = redirect_uri
        self.token = SpotipyToken(scope, client_id, client_secret, username, redirect_uri).token