# Spotify Archiver

_Hendrik Laux, 2022_

Script to export your Spotify playlists (incl. title, artist, album, etc ...) in a readable format for sharing and/or archiving.

All the steps needed to get the required information (client details etc ...) are explained IN the script to make it
easily usable for users that lack experience with the API or using command line tools. 
A command line usage (with argparse) is not implemented but may be intended for the future.

## Usage
Open a terminal inside the repository folder.

Create a python virtual environment:

`python3 -m pip install virtualenv`

`python3 -m venv venv/spotifyarchiver`

Activate the environment, install the requirements pandas and spotipy:

`. venv/spotifyarchiver/bin/activate`

`pip install -r requirements.txt`

Run the main.py script from the terminal

`python main.py`

Follow the steps in the main script.

## Getting the required data from your account
_Note: This is also explained in the output of the script itself_

These are so called API-keys bound to your account. Never pass these to strangers. In this code, they will be processed
exclusively by the Spotify Servers/API.

Go to https://developer.spotify.com/my-applications, log in with your account and click on '**CREATE AN APP**'.
Note down your Client ID and Client Secret in a secure file (or leave the page open if you only want to do this once).

For your username, visit https://www.spotify.com/de/account/overview/.

## Export Location

The script will ask for the desired expoert location. 

By default this is in your current directory (where you opened the terminal), but you could provide any valid path here.

## Export Formats

Export Format can be "csv" and "html" (currently).

While CSVs are easier to be processed in a follow-up code/application, the usage of html makes it more pretty :)
