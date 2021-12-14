import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#SPOTIPY_CLIENT_ID = '58d8a0730d2144e48ddea65b6033ad39'
#SPOTIPY_CLIENT_SECRET = '87ac3f4c385244448cb02b728ab4b9ed'

auth_manager = SpotifyClientCredentials('58d8a0730d2144e48ddea65b6033ad39', '87ac3f4c385244448cb02b728ab4b9ed')
sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.user_playlists('spotify')

while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
