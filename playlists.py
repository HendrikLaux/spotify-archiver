from copy import copy


class SpotifyPlaylist:
    """
    Class representing a Spotify Playlist
    Initialized using a playlist id and a Spotify object
    Saves all important properties of the playlist in member variables for easy, dict-free access.
    """

    # possible export formats
    EXPORT_FORMATS = ["csv", "html"]
    EXPORT_FORMATS_STR = "/".join(EXPORT_FORMATS)

    # Keys to export
    EXPORT_KEY_ORDER = ["title", "artists", "album", "release", "duration", "added"]
    EXPORT_KEY_DESCRIPTION = ["Title", "Artists", "Album", "Release", "Duration [sec]", "Added to Playlist"]

    def __init__(self, playlist, spotify_object):

        self.defunct = False

        try:
            self.name = playlist["name"]

            self._items = spotify_object.playlist_items(playlist["id"])

            self.count = self._items["total"]

            self.tracks = []

            # extract all the information from the tracks
            for track in self._items["items"]:
                track_dict = {}
                track_dict["added"] = track["added_at"].split("T")[0]
                track_dict["album"] = track["track"]["album"]["name"]
                track_dict["title"] = track["track"]["name"]
                track_dict["artists"] = ", ".join([a["name"] for a in track["track"]["artists"]])
                track_dict["duration"] = track["track"]["duration_ms"]//1000 + 1
                track_dict["release"] = track["track"]["album"]["release_date"]
                self.tracks.append(copy(track_dict))

        except Exception as e:
            print(f"Warning: Could not extract playlist {playlist['name']}. This is usually because it is not a normal playlist (podcast collection, etc..).")
            self.defunct = True

    def print(self):
        """
        Used for debugging mainly, prints the playlist (halfway) pretty
        """
        print(f"Playlist Name: {self.name}")
        print(f"Track Count: {self.count}")

        for t in self.tracks:
            print(str(t))

    def export(self, file, style='csv'):
        """
        Exports this playlist object
        :param file: file to export to
        :param style: export style
        """
        if style.lower() == "csv":
            self._export_csv(file)
        elif style.lower() == "html":
            self._export_html(file)
        else:
            print(f"Invalid export style {style}!")
            quit()

    def _export_csv(self, file):
        """
        export as csv (comma separated values)
        """

        import csv
        # tracks to csv rows according to export key order
        rows = []
        for track in self.tracks:
            row = [track[key] for key in self.EXPORT_KEY_ORDER]
            rows.append(row)

        # write to csv
        with open(file, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.EXPORT_KEY_DESCRIPTION)
            for row in rows:
                writer.writerow(row)

    def _export_html(self, file):
        """
        export as html table
        """

        import pandas as pd
        # tracks to csv rows according to export key order
        rows = []
        for track in self.tracks:
            row = [track[key] for key in self.EXPORT_KEY_ORDER]
            rows.append(row)

        # use a data frame for exporting
        columns = self.EXPORT_KEY_DESCRIPTION
        df = pd.DataFrame(data=rows, columns=columns)

        # export to html
        with open(file, "w") as file:
            file.write(df.to_html())
