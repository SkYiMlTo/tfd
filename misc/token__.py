import requests

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': 'id',
    'client_secret': 'secret',
    'scope': 'playlist-modify-public playlist-modify-private'
})

# convert the response to JSON
auth_response_data = auth_response.json()

print(auth_response_data)

# save the access token
access_token = auth_response_data['access_token']

print(access_token)

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
playlist_id = '6d0BMqF6SF59tCQHtwA2rP'

# actual GET request with proper header
r = requests.get(f'{BASE_URL}playlists/{playlist_id}/tracks', headers=headers)
# r = test_requests.post("https://api.spotify.com/v1/playlists/6d0BMqF6SF59tCQHtwA2rP/tracks?uris=spotify%3Atrack%3A5AtpIUEM221ILCVt93RMj4", headers=headers)
r = r.json()
print(r)
