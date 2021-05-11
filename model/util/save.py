import os
from pathlib import Path
from typing import Tuple

from model import Directory
from model.error import InvalidNameError
from model.util import generate_filesystem, Hexable


class Save:
    """A Save object is what is used to save and load a game save
    from the disk given a username

    :param username: The username of the game save to use
    :raises InvalidNameError: When the username has an invalid path character
    """

    INVALID_CHARS = "?&:;|[]*,\""
    SAVE_FOLDER = f"{Path.home()}/virus.shSaves"

    def __init__(self, username: str):
        for invalid_char in Save.INVALID_CHARS:
            if username.find(invalid_char) != -1:
                raise InvalidNameError(f"{invalid_char} cannot exist in username.")
        self.__username = username
        self.__root, total_files = generate_filesystem()
        self.__virus_files = total_files // 1000
        self.__deleted_virus_files = 0
        self.__normal_files = total_files
        self.__deleted_normal_files = 0

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

    def save(self):
        """Saves the current state of the game into a custom file"""

        # Create the save directory if necessary
        if not os.path.exists(Save.SAVE_FOLDER):
            os.mkdir(Save.SAVE_FOLDER)

        save_json = {
            "username": self.__username,
            "virus_files": {
                "deleted": self.__deleted_virus_files,
                "total": self.__virus_files
            },
            "normal_files": {
                "deleted": self.__deleted_normal_files,
                "total": self.__normal_files
            },
            "root": self.__root.to_json()
        }
        Hexable.save(save_json, f"{Save.SAVE_FOLDER}/{self.__username}.hex")

    def load(self):
        """Loads a save file based on the username, if it exists

        :raises FileNotFoundError: When the save file for the username does not exist
        """
        save_json = Hexable.load(f"{Save.SAVE_FOLDER}/{self.__username}.hex")

        self.__deleted_virus_files = save_json["virus_files"]["deleted"]
        self.__virus_files = save_json["virus_files"]["total"]
        self.__deleted_normal_files = save_json["normal_files"]["deleted"]
        self.__normal_files = save_json["normal_files"]["total"]
        self.__root = Directory.from_json(save_json["root"])
