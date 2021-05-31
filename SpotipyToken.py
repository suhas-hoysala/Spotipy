import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import spotipy.util as util


class SpotipyToken:
    token = None
    def __init__(self, scope, client_id, client_secret, username, redirect_uri):
        scope = 'user-library-read'
        self.token = util.prompt_for_user_token(username,
                                scope, 
                                client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri=redirect_uri
        )