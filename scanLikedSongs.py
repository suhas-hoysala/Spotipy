# Shows a user's saved tracks (need to be authenticated via oauth)

from requests.exceptions import ReadTimeout
import spotipy
from spotipy.exceptions import SpotifyException
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
            print(track['name'] + ' -', ', '.join( [y['name'] for y in track['artists']]))

    def get_songs(self):
        results = []
        index = 0
        while True:
            retries = 5
            retry = 0
            #retry call five times
            while True:
                try:
                    curr_saved_tracks = self.sp.current_user_saved_tracks(offset=index*20)
                except(SpotifyException, ReadTimeout) as error:
                    retry += 1
                    if retry >= retries:
                        raise(error)
                    continue
                break
            curr_items = curr_saved_tracks['items']
            if len(curr_items)>0:
                results = results + curr_items
            else:
                break
            index += 1
        return results

    