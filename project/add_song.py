import requests

# AUTH_URL = 'https://accounts.spotify.com/api/token'
# auth_response = test_requests.post(AUTH_URL, {
#     'grant_type': 'client_credentials',
#     'client_id': 'id',
#     'client_secret': 'secret',
#     'scope': 'playlist-modify-public playlist-modify-private'
# })
# # convert the response to JSON
# auth_response_data = auth_response.json()
#
# print(auth_response_data)
#
# # save the access token
# access_token = auth_response_data['access_token']

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer access_token',
}

params = (
    ('uris', 'spotify:track:5AtpIUEM221ILCVt93RMj4'),
)

C = "7Je5n5Eh00MEiq27PSAkT9"
NC = "6d0BMqF6SF59tCQHtwA2rP"

response = requests.post('https://api.spotify.com/v1/playlists/' + C + '/tracks', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = test_requests.post('https://api.spotify.com/v1/playlists/6d0BMqF6SF59tCQHtwA2rP/tracks?uris=spotify%3Atrack%3A5AtpIUEM221ILCVt93RMj4', headers=headers)