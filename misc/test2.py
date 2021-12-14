import spotipy
import spotipy.util as util
import random

from spotipy import oauth2

token = oauth2.SpotifyClientCredentials(client_id='58d8a0730d2144e48ddea65b6033ad39', client_secret='87ac3f4c385244448cb02b728ab4b9ed')

cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

results1 = spotify.user_playlist_tracks('SkY_iMlTo', '6d0BMqF6SF59tCQHtwA2rP', limit=100, offset=0)
