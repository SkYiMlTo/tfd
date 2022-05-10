import collections
import copy
import time
from datetime import datetime

from secret import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
from InterfaceSpotifyApi import InterfaceSpotifyApi


class PlaylistChecker:

    def __init__(self, file):
        self.__interface_spotify_api = InterfaceSpotifyApi(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
        self.__playlists, self.__saved_songs = self.get_playlists(file)

    def get_playlists(self, file):
        playlists = []
        saved_songs = {}
        with open(file) as f:
            line = f.readline().rstrip()
            while line:
                line = f.readline().rstrip()
                if line:
                    line2 = line.split(',')
                    playlists.append([line2[1], line2[2], line2[3]])
                    saved_songs[line2[2]] = self.return_tracks_playlist(line2[2])
                    saved_songs[line2[3]] = self.return_tracks_playlist(line2[3])
        return playlists, saved_songs

    def return_tracks_playlist(self, playlist_id):
        playlist_elems = []
        OFFSET = 0
        r = self.__interface_spotify_api.get_tracks(playlist_id, OFFSET).json()
        try:
            while r['items']:
                tracks = r['items']
                playlist_elems.extend(elem['track']['id'] for elem in tracks)
                OFFSET += 100
                r = self.__interface_spotify_api.get_tracks(playlist_id, OFFSET).json()
        except KeyError:
            with open("errors.txt", "a") as f:
                f.write(
                    "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - Impossible de recuperer les musique de la playlist: "
                                                                         "" + playlist_id + " | Erreur: " + str(KeyError) +
                    "\n")
        # print("Nb elems find:" + str(len(playlist_elems)))
        return playlist_elems

    def get_tracks_main(self, C, NC):
        C_items = self.return_tracks_playlist(C)
        NC_items = self.return_tracks_playlist(NC)
        return C_items, NC_items

    def remove_duplicates(self, playlist_id, tracks, f, playlist):
        duplicates_tracks = [item for item, count in collections.Counter(tracks).items() if count > 1]
        for track in duplicates_tracks:
            f.write("Playlist " + ("collaborative", "non collaborative ")[playlist] + " | Duplicat retire: " + str(track) + "\n")
            self.__interface_spotify_api.delete_song(playlist_id, track)
            self.__interface_spotify_api.add_song_here(playlist_id, track)

    def compare_playlists(self, current_C_items, current_NC_items):
        more_tracks_in_C, more_items_in_NC = [], []
        more_tracks_in_C.extend(
            track for track in current_C_items if track not in current_NC_items
        )

        more_items_in_NC.extend(
            track for track in current_NC_items if track not in current_C_items
        )

        return more_tracks_in_C, more_items_in_NC

    def NC_deleted_tracks(self, current, save):
        return [elem for elem in save if elem not in current]

    def C_added_tracks(self, current, save):
        return [elem for elem in current if elem not in save]

    def main_playlist_checker(self):
        while True:
            try:
                self.__interface_spotify_api.do_we_need_to_refresh_access_token()
                self.update_playlists()
            except:
                print("Il y a eu une erreur quelque part dans le code")
                time.sleep(180)
            time.sleep(60)

    def update_playlists(self):
        with open("update_playlists_logs.txt", "a") as f:
            f.write("----------\n")
            for playlist in self.__playlists:
                self.update_playlist(playlist[1], playlist[2], playlist[0], f)
            f.write("----------\n\n")

    def update_playlist(self, C, NC, name, f):
        f.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - Beginning update playlist " + name + "\n")
        # print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - Beginning update playlist " + name) # DEBUG/TESTING

        # Get current songs in playlists
        current_C_items, current_NC_items = self.get_tracks_main(C, NC)

        # Remove potential duplicates in C
        self.remove_duplicates(C, current_C_items, f, 0)
        current_C_items = list(set(current_C_items))
        self.remove_duplicates(NC, current_NC_items, f, 1)
        current_NC_items = list(set(current_NC_items))

        # Check deleted and added tracks
        list_of_tracks_deleted_from_NC = self.NC_deleted_tracks(current_NC_items, self.__saved_songs[NC])
        list_of_tracks_added_in_C = self.C_added_tracks(current_C_items, self.__saved_songs[C])

        # Update playlists
        for track in list_of_tracks_added_in_C:
            self.__interface_spotify_api.add_song_here(NC, track)
            current_NC_items.append(track)
        for track in list_of_tracks_deleted_from_NC:
            if track in current_C_items:
                self.__interface_spotify_api.delete_song(C, track)
                current_C_items.remove(track)

        # Compare playlists and check errors
        more_tracks_in_C, more_tracks_in_NC = self.compare_playlists(current_C_items, current_NC_items)
        for track in more_tracks_in_C:
            self.__interface_spotify_api.add_song_here(NC, track)
            current_NC_items.append(track)
        for track in more_tracks_in_NC:
            self.__interface_spotify_api.add_song_here(C, track)
            current_C_items.append(track)

        # Update saved values
        self.__saved_songs[C], self.__saved_songs[NC] = copy.deepcopy(current_C_items), copy.deepcopy(current_NC_items)
        # Wait a bit
        f.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - End update playlist " + name + "\n")
        # print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - End update playlist " + name) # DEBUG/TESTING
