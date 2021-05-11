import os
from json import dumps, loads
from pathlib import Path
from typing import Tuple

from model.util.filesystem import generate_filesystem
from model import Directory
from model.error import InvalidNameError


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

        save_json = dumps({
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
        })

        # Convert the JSON object into a list of hex bytes
        result = []
        for char in save_json:
            result.append(hex(ord(char))[2:])

        # Save the file separating each line of
        with open(f"{Save.SAVE_FOLDER}/{self.__username}.hex", "w") as save_file:
            total_processed = 0
            for hex_byte in result:
                save_file.write(hex_byte + " ")
                total_processed += 1
                if total_processed % 16 == 0:
                    save_file.write("\n")

    def load(self):
        """Loads a save file based on the username, if it exists

        :raises FileNotFoundError: When the save file for the username does not exist
        """

        if not os.path.exists(f"{Save.SAVE_FOLDER}/{self.__username}.hex"):
            raise FileNotFoundError(f"The {self.__username} save file does not exist")

        with open(f"{Save.SAVE_FOLDER}/{self.__username}.hex", "r") as save_file:
            hex_data = "".join(save_file.readlines()).strip().split(" ")

        # Convert the list of hex data bytes back into a JSON object
        save_json = ""
        for hex_byte in hex_data:
            save_json += chr(int(hex_byte, 16))
        save_json = loads(save_json)

        self.__deleted_virus_files = save_json["virus_files"]["deleted"]
        self.__virus_files = save_json["virus_files"]["total"]
        self.__deleted_normal_files = save_json["normal_files"]["deleted"]
        self.__normal_files = save_json["normal_files"]["total"]
        self.__root = Directory.from_json(save_json["root"])
