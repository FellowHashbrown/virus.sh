import os
from pathlib import Path
from typing import List, Tuple

from model import Directory
from model.error import InvalidNameError
from model.util import generate_filesystem, Hexable


class Save:
    """A Save object is what is used to save and load a game save
    from the disk given a username

    :param username: The username of the game save to use
    :raises InvalidNameError: When the username has an invalid path character
    """

    @staticmethod
    def load_saves() -> List['Save']:
        """Loads all the saves from the Save folder and returns them in a list"""

        # Check if the save folder exists; If not, create it
        if not os.path.exists(Save.SAVE_FOLDER):
            os.mkdir(Save.SAVE_FOLDER)

        files = []
        for entry in os.listdir(Save.SAVE_FOLDER):
            if os.path.isdir(f"{Save.SAVE_FOLDER}/{entry}"):
                username = entry
                files.append(Save(username))
        saves = []
        for i in range(len(files)):
            try:
                saves.append(files[i])
                saves[i].load()
            except FileNotFoundError:
                print(f"issue loading {files[i].get_username()}")
        return saves

    INVALID_CHARS = "?&:;|[]*,\""
    SAVE_FOLDER = f"{Path.home()}/virus.shSaves"

    def __init__(self, username: str):
        for invalid_char in Save.INVALID_CHARS:
            if username.find(invalid_char) != -1:
                raise InvalidNameError(f"{invalid_char} cannot exist in username.")
        self.__username = username
        self.__root = None
        self.__virus_files = self.__deleted_virus_files = 0
        self.__normal_files = self.__deleted_normal_files = self.__restored = 0
        self.__tracked_files = []

    def generate(self):
        """Tells the Save object to create a new game save with the
        specified username or to load the existing game save
        """
        try:
            self.load()
            root_json = Hexable.load(f"{Save.SAVE_FOLDER}/{self.get_username()}/filesystem.hex")
            self.__root = Directory.from_json(root_json)
        except FileNotFoundError:
            self.__root, total_files = generate_filesystem(self.__username)
            self.__normal_files = total_files
            self.__virus_files = total_files // 1000
            self.save()

    def get_username(self) -> str:
        """Returns the username for the game save"""
        return self.__username

    def get_root(self) -> Directory:
        """Returns the root of the filesystem for the game save"""
        return self.__root

    def get_virus_files(self) -> Tuple[int, int]:
        """Returns a 2-tuple of the amount of deleted virus files and the total amount of virus files"""
        return self.__deleted_virus_files, self.__virus_files

    def get_normal_files(self) -> Tuple[int, int]:
        """Returns a 2-tuple of the amount of deleted normal files and the total amount of normal files"""
        return self.__deleted_normal_files, self.__normal_files

    def get_restored_files(self) -> int:
        """Returns the amount of normal files that have been restored"""
        return self.__restored

    def track_virus(self, directory: Directory):
        """Keeps track of a virus file by storing the parent Directory of the
        virus file
        """
        if str(directory) not in self.__tracked_files:
            self.__tracked_files.append(str(directory))

    def save(self):
        """Saves the current state of the game into a custom file"""

        # Create the game saves directory if necessary
        if not os.path.exists(Save.SAVE_FOLDER):
            os.mkdir(Save.SAVE_FOLDER)

        # Create this saves directory
        if not os.path.exists(f"{Save.SAVE_FOLDER}/{self.get_username()}"):
            os.mkdir(f"{Save.SAVE_FOLDER}/{self.get_username()}")

        save_json = {
            "username": self.__username,
            "virus_files": {
                "deleted": self.__deleted_virus_files,
                "total": self.__virus_files,
                "tracked": self.__tracked_files
            },
            "normal_files": {
                "deleted": self.__deleted_normal_files,
                "total": self.__normal_files
            }
        }
        Hexable.save(save_json, f"{Save.SAVE_FOLDER}/{self.get_username()}/save.hex")
        Hexable.save(self.__root.to_json(), f"{Save.SAVE_FOLDER}/{self.get_username()}/filesystem.hex")

    def load(self):
        """Loads a save file based on the username, if it exists

        :raises FileNotFoundError: When the save file for the username does not exist
        """
        save_json = Hexable.load(f"{Save.SAVE_FOLDER}/{self.__username}/save.hex")

        self.__tracked_files = save_json["virus_files"]["tracked"]
        self.__deleted_virus_files = save_json["virus_files"]["deleted"]
        self.__virus_files = save_json["virus_files"]["total"]
        self.__deleted_normal_files = save_json["normal_files"]["deleted"]
        self.__normal_files = save_json["normal_files"]["total"]
