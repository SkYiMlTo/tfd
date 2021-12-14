import copy
import time
import collections
import requests


def add_song_here(playlist_id, track_id, TOKEN):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + TOKEN,
    }

    params = (
        ('uris', 'spotify:track:' + track_id),
    )

    C = "7Je5n5Eh00MEiq27PSAkT9"
    NC = "6d0BMqF6SF59tCQHtwA2rP"

    response = requests.post('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers,
                             params=params)


def get_tracks(playlist_id, OFFSET, TOKEN):
    import requests

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + TOKEN,
    }

    params = (
        ('fields', 'items(track(id))'),
    )

    response = requests.get(
        'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks?limit=100&offset=' + str(OFFSET), headers=headers,
        params=params)
    return response
    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = test_requests.get('https://api.spotify.com/v1/playlists/7Je5n5Eh00MEiq27PSAkT9/tracks?fields=items(track(id))', headers=headers)


def return_tracks_playlist(playlist_id, TOKEN):
    playlist_elems = []
    OFFSET = 0
    r = get_tracks(playlist_id, OFFSET, TOKEN).json()
    while r['items']:
        tracks = r['items']
        for elem in tracks:
            playlist_elems.append(elem['track']['id'])
        OFFSET += 100
        r = get_tracks(playlist_id, OFFSET, TOKEN).json()
    # print("Nb elems find:" + str(len(playlist_elems)))
    return playlist_elems


def get_token():
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': '58d8a0730d2144e48ddea65b6033ad39',
        'client_secret': '87ac3f4c385244448cb02b728ab4b9ed',
        'scope': 'playlist-modify-public playlist-modify-private'
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    return auth_response_data['access_token']


def get_tracks_main(C, NC, TOKEN):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=TOKEN)
    }

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    # actual GET request with proper header
    C_items = return_tracks_playlist(C, TOKEN)
    NC_items = return_tracks_playlist(NC, TOKEN)
    # print("Collab: ", end='')
    # print(*C_items)
    # print("Private: ", end='')
    # print(*NC_items)

    # items_to_add_in_NC = []
    # for elem in C_items:
    #     if elem not in NC_items:
    #         items_to_add_in_NC.append(elem)

    return C_items, NC_items


def delete_song(playlist_id, track_id, TOKEN):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + TOKEN,
    }

    data = '{"tracks":[{"uri":"spotify:track:' + track_id + '"}]}'

    response = requests.delete('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers,
                               data=data)
    print(response.json())


def refresh_access_token():
    import requests

    data = {
        'client_id': '7c237c11ac7b498e9454371d425cb2e4',
        'client_secret': '5d4d2a40084b4bbf91c43d3b53c89088',
        'grant_type': 'refresh_token',
        'refresh_token': 'AQDLPAgQLMGNVN9HNz7uwxPc6BT9ovxfCyo1qTmL2_GbLyskq2PXHjlk4JlgXf__WMsjj092LfKR7P3snDd5-zGhwC0b2MYCHG5W57VLRJrgvkSJurByWuIXwR6Mw1nfofg'
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=data)
    response = response.json()
    # print(response)
    return response['access_token']


def NC_deleted_tracks(current, save):
    deleted_elements = []
    for elem in save:
        if elem not in current:
            deleted_elements.append(elem)
    return deleted_elements


def C_added_tracks(current, save, current_NC):
    added_elements = []
    for elem in current:
        if elem not in save and elem not in current_NC:
            added_elements.append(elem)
    return added_elements


def compare_playlists(current_C_items, current_NC_items):
    more_tracks_in_C, more_items_in_NC = [], []
    for track in current_C_items:
        if track not in current_NC_items:
            more_tracks_in_C.append(track)
    for track in current_NC_items:
        if track not in current_C_items:
            more_items_in_NC.append(track)
    return more_tracks_in_C, more_items_in_NC


def remove_duplicates(playlist_id, TOKEN):
    tracks = return_tracks_playlist(playlist_id, TOKEN)
    duplicates_tracks = [item for item, count in collections.Counter(tracks).items() if count > 1]
    for track in duplicates_tracks:
        delete_song(playlist_id, track, TOKEN)
        add_song_here(playlist_id, track, TOKEN)


def main():
    # Playlists IDs
    C = "3xFQXlI7Xf93UzQXpuFqEs"
    NC = "28bNg1uPJd9kA4v9F6NuwH"
    saved_C_items, saved_NC_items = get_tracks_main(C, NC, refresh_access_token())
    # time.sleep(10)
    missingTracks = []
    while True:
        # Refresh token to keep access
        TOKEN = refresh_access_token()

        # Remove potential duplicates in C
        remove_duplicates(C, TOKEN)
        remove_duplicates(NC, TOKEN)

        # Get current songs in playlists
        current_C_items, current_NC_items = get_tracks_main(C, NC, TOKEN)

        # Check deleted and added tracks
        list_of_tracks_deleted_from_NC = NC_deleted_tracks(current_NC_items, saved_NC_items)
        list_of_tracks_added_in_C = C_added_tracks(current_C_items, saved_C_items, missingTracks)
        missingTracks = []

        # Update playlists
        for track in list_of_tracks_added_in_C:
            add_song_here(NC, track, TOKEN)
            current_NC_items.append(track)
        for track in list_of_tracks_deleted_from_NC:
            delete_song(C, track, TOKEN)
            current_C_items.remove(track)

        # Compare playlists and check errors
        more_tracks_in_C, more_tracks_in_NC = compare_playlists(current_C_items, current_NC_items)
        for track in more_tracks_in_C:
            add_song_here(NC, track, TOKEN)
            current_NC_items.append(track)
        for track in more_tracks_in_NC:
            add_song_here(C, track, TOKEN)
            missingTracks.append(track)
            current_C_items.append(track)

        # Update saved values
        saved_C_items, saved_NC_items = copy.deepcopy(current_C_items), copy.deepcopy(current_NC_items)
        # Wait a bit
        print("End update")
        time.sleep(10)
        print("Beginning update")


# def main():
#     # Track ID from the URI
#     C = "7Je5n5Eh00MEiq27PSAkT9"
#     NC = "6d0BMqF6SF59tCQHtwA2rP"
#     not_skip = False
#     NC_items_previous = []
#     items_to_delete_in_C = []
#     temp = []
#     while True:
#         TOKEN = refresh_access_token()
#         NC_items, items_to_add_in_NC = get_tracks_main(C, NC, TOKEN)
#         print("Current items: ", end='')
#         print(*NC_items)
#         if not_skip:
#             for elem in NC_items_previous:
#                 if elem not in NC_items:
#                     items_to_delete_in_C.append(elem)
#                     items_to_add_in_NC.remove(elem)
#                     temp.append(elem)
#         for elem in items_to_add_in_NC:
#             add_song_here(NC, elem, TOKEN)
#         for elem in items_to_delete_in_C:
#             print("Item to delete: " + elem)
#             delete_song(C, elem, TOKEN)
#         items_to_delete_in_C = []
#         print("Playlists saved !")
#         NC_items_previous = copy.deepcopy(NC_items)
#         for elem in temp:
#             NC_items_previous.append(elem)
#         temp = []
#         print("Previous items: ", end='')
#         print(*NC_items)
#         time.sleep(30)
#         print("Beginning saving...")
#         not_skip = True


if __name__ == '__main__':
    main()
