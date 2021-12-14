import time
from datetime import datetime

import requests


class InterfaceSpotifyApi:

    def __init__(self, client_id, client_secret, refresh_token):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__refresh_token = refresh_token
        self.__access_token = None
        self.__access_token_expiration_date = 0
        self.refresh_access_token()

    def do_we_need_to_refresh_access_token(self):
        if self.__access_token_expiration_date - time.time() < 1800:  # Si il reste moins de 30mins de vie au token, on refresh
            self.refresh_access_token()

    def refresh_access_token(self):

        data = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.__refresh_token
        }

        response = requests.post('https://accounts.spotify.com/api/token', data=data)
        response = response.json()
        # print(response)
        self.__access_token = response['access_token']
        self.__access_token_expiration_date = time.time() + 3600  # Token expire au bout de 1H (soit 3600 secs)
        f = open("access_token.txt", "a")
        f.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - New access token generated\n")
        f.close()

    def add_song_here(self, playlist_id, track_id):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.__access_token,
        }

        params = (
            ('uris', 'spotify:track:' + track_id),
        )

        response = requests.post('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers,
                                 params=params)

    def get_tracks(self, playlist_id, OFFSET):
        import requests

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.__access_token,
        }

        params = (
            ('fields', 'items(track(id))'),
        )

        response = requests.get(
            'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks?limit=100&offset=' + str(OFFSET),
            headers=headers,
            params=params)
        return response
        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = test_requests.get('https://api.spotify.com/v1/playlists/7Je5n5Eh00MEiq27PSAkT9/tracks?fields=items(track(id))', headers=headers)

    def delete_song(self, playlist_id, track_id):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.__access_token,
        }

        data = '{"tracks":[{"uri":"spotify:track:' + track_id + '"}]}'

        response = requests.delete('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers,
                                   data=data)
        print(response.json())
