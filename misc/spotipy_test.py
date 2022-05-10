import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#SPOTIPY_CLIENT_ID = 'id'
#SPOTIPY_CLIENT_SECRET = 'secret'

auth_manager = SpotifyClientCredentials('id', 'secret')
sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.user_playlists('spotify')

while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    playlists = sp.next(playlists) if playlists['next'] else None
