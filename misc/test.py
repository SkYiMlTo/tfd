from bottle import route, run, request
import spotipy
from spotipy import oauth2

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'id'
SPOTIPY_CLIENT_SECRET = 'secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,
                               cache_path=CACHE)
url = request.url
code = sp_oauth.parse_response_code(SPOTIPY_REDIRECT_URI)
acces_token = ""
if code:
    print("Found Spotify auth code in Request URL! Trying to get valid access token...")
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']
if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        print(results)