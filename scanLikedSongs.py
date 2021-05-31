# Shows a user's saved tracks (need to be authenticated via oauth)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import spotipy.util as util
from SpotipyRegToken import SpotipyRegToken

scope = 'user-library-read'

class SongsScanner:

    def __init__(self):
        tokenClient = SpotipyRegToken()
        username = tokenClient.username
        token = tokenClient.token

        if token:
            self.sp = spotipy.Spotify(auth=token)
        else:
            print("Can't get token for", username)

    def show_tracks(self, token, results):
        for item in results:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])

    def get_songs(self):
        results = []
        no_more_results = False
        index = 0
        while not no_more_results:
            curr_saved_tracks = self.sp.current_user_saved_tracks(offset=index*20)
            curr_items = curr_saved_tracks['items']
            if len(curr_items)>0:
                results = results + curr_items
            else:
                no_more_results=True
            index += 1
        return results

    