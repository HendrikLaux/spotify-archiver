import os
from datetime import datetime
from typing import List, Tuple

import spotipy
from spotipy import Spotify, SpotifyClientCredentials

from playlists import SpotifyPlaylist


def tutorial() -> str:
    """
    Creates the tutorial string
    """
    tut_str = ""
    tut_str += "Spotify Playlist Crawl (2022) \n -------------------------------------------"
    tut_str += "\nNote: it is only possible to fetch PUBLIC playlists \n (right-click -> 'add to profile' to make them public)"
    tut_str += "\nHow does it work? \n  Go to https://developer.spotify.com/my-applications, log in with your account and click on 'CREATE AN APP'."
    tut_str += "\n  Choose an app name and description (any, not important ..)"
    tut_str += "\n  Note down your Client ID and Client Secret (do not give this to other people!)."
    tut_str += "\n  Now note down your username from https://www.spotify.com/de/account/overview/"
    tut_str += "\n   (you can also enter another username if you want to save another person's playlists)"
    tut_str += "\n  -> You will need it now ... \n -------------------------------------------"
    return tut_str


def prompt_user_information() -> Tuple[str, Spotify]:
    """
    Get user information from the terminal
    :return: tuple (username, spotify object)
    """
    client_id = input("Please enter your Client ID: ")
    client_secret = input("Please enter your Client Secret: ")
    username = input("Please enter your User ID: ")

    try:
        auth_manager = SpotifyClientCredentials(client_id=client_id,
                                                client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        return username, sp

    except Exception as e:
        print("An error occurred while using the script ... \n")
        print(e)
        quit()


def get_playlists(sp: Spotify, user_id: str) -> List[SpotifyPlaylist]:
    """
    Fetch all playlists for a specific user
    :param sp: Spotify object (authorized!)
    :param user_id: user id to fetch playlists from
    :return: List of Spotify Playlists
    """

    # get user playlist ids (in batches because of that annoying API limit)
    playlists = []
    offset = 0
    while True:
        playlist_batch = sp.user_playlists(user_id, limit=50, offset=offset)["items"]
        if playlist_batch:
            playlists.extend(playlist_batch)
            offset += 50
            continue
        else:
            break

    # return a Playlist object for each playlist in the user's list
    playlists_extracted = [SpotifyPlaylist(p, sp) for p in playlists]
    playlists_extracted = [p for p in playlists_extracted if not p.defunct]
    return playlists_extracted


def export_playlists(list_of_playlists: List[SpotifyPlaylist], export_fmt: str, location: str) -> None:
    # create folder for export
    location = os.path.join(location, f"SpotifyExport_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    os.makedirs(location)

    # export one by one
    for i, playlist in enumerate(list_of_playlists):
        # just use alphanumeric chars for the name to avoid errors
        alphanum_name = ''.join(ch for ch in playlist.name if ch.isalnum())
        file = os.path.join(location, f"{i}_{alphanum_name}.{export_fmt.lower()}")
        playlist.export(file=file,
                        style=export_fmt)
