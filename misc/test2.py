import spotipy
import spotipy.util as util
import random

from spotipy import oauth2

token = oauth2.SpotifyClientCredentials(client_id='id', client_secret='secret')

cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

results1 = spotify.user_playlist_tracks('SkY_iMlTo', '6d0BMqF6SF59tCQHtwA2rP', limit=100, offset=0)
