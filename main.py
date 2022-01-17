"""
Script to export your Spotify playlists in a readable format for sharing and/or archiving.

All the steps needed to get the required information (client details etc ...) are explained IN the script to make it
easily usable for users that lack experience with the API.
A command line usage (with argparse) is not implemented but may be intended for the future.

Usage:
- create a python virtual environment
- Install pandas and spotipy
- run the main.py script from the terminal
- Follow the steps in the main script

Export Format can be csv and html (currently).
While CSVs are easier to be processed in a follow-up code/application, the usage of html makes it more pretty :)

Hendrik Laux, Jan 2022
"""

import os
from playlists import SpotifyPlaylist
from util import export_playlists, get_playlists, prompt_user_information, tutorial


if __name__ == '__main__':
    # 1) print tutorial
    print(tutorial())

    # 2) get user information
    username, spotify = prompt_user_information()

    # 3) fetch playlists
    playlist_list = get_playlists(sp=spotify, user_id=username)
    print(f"Found {len(playlist_list)} playlists!")

    # 4) Print information, select export format
    exp_format = ""
    while exp_format not in SpotifyPlaylist.EXPORT_FORMATS:
        exp_format = input(f"Please select export format [{SpotifyPlaylist.EXPORT_FORMATS_STR}]: ").lower()
        if exp_format not in SpotifyPlaylist.EXPORT_FORMATS:
            print(f"Invalid export format, must be from [{SpotifyPlaylist.EXPORT_FORMATS_STR}]")

    # 5) Select export location
    location = ""
    while not (os.path.exists(location) and os.path.isdir(location)):
        cwd = os.getcwd()
        print(f"Current Working Directory is {cwd}. Leave the following blank to export here.")
        location = input("Enter export location: ")
        location = cwd if not location else location

        if not (os.path.exists(location) and os.path.isdir(location)):
            print("This location does not exist! Please re-enter location ...")

    # 6) export
    export_playlists(playlist_list, exp_format, location)

    print(f"Export to {location} successful!")

