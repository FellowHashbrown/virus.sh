import os
from pathlib import Path
from typing import List, Tuple

from model import Directory, VirusFile
from model.error import InvalidNameError
from model.util import generate_filesystem, Hexable, choose_random_directory, generate_virus


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
    MINIMUM_SPEED = 3
    SPEED_INTERVAL = 3

    # # # # # # # # # # # # # # # # # # # #

    def __init__(self, username: str):
        for invalid_char in Save.INVALID_CHARS:
            if username.find(invalid_char) != -1:
                raise InvalidNameError(f"{invalid_char} cannot exist in username.")
        self.__username = username
        self.__root = None
        self.__trash = None
        self.__virus_files = self.__deleted_virus_files = 0
        self.__normal_files = self.__deleted_normal_files = self.__restored = 0
        self.__tracked_files = []
        self.__deletion_log: List[Tuple[int, str, str]] = []
        self.__speed = 60  # Time in seconds that a file is deleted
        self.__virus_file_locations = {}

    # # # # # # # # # # # # # # # # # # # #

    def generate(self):
        """Tells the Save object to create a new game save with the
        specified username or to load the existing game save
        """
        try:
            self.load()
            system_json = Hexable.load(f"{Save.SAVE_FOLDER}/{self.get_username()}/filesystem.hex")
            self.__root = Directory.from_json(system_json["root"])
            self.__trash = Directory.from_json(system_json["trash"])
        except FileNotFoundError:
            self.__root, total_files, self.__virus_file_locations = generate_filesystem(self.__username)
            self.__trash = Directory("Trash")
            self.__normal_files = total_files
            self.__virus_files = total_files // 1000
            self.save()

    def get_username(self) -> str:
        """Returns the username for the game save"""
        return self.__username

    def get_root(self) -> Directory:
        """Returns the root of the filesystem for the game save"""
        return self.__root

    def get_trash(self) -> Directory:
        """Returns the Trash directory for the game save"""
        return self.__trash

    def get_speed(self) -> int:
        """Returns the speed at which a file is deleted by the virus, in seconds"""
        return self.__speed

    def get_virus_files(self) -> Tuple[int, int]:
        """Returns a 2-tuple of the amount of deleted virus files and the total amount of virus files"""
        return self.__deleted_virus_files, self.__virus_files

    def get_normal_files(self) -> Tuple[int, int]:
        """Returns a 2-tuple of the amount of deleted normal files and the total amount of normal files"""
        return self.__deleted_normal_files, self.__normal_files

    def get_restored_files(self) -> int:
        """Returns the amount of normal files that have been restored"""
        return self.__restored

    def get_deletion_log(self) -> List[Tuple[int, str, str]]:
        """Returns the log of files, with their full paths, that are deleted by the virus"""
        return list(self.__deletion_log)

    def log_deletion(self, virus_id: int, file: str):
        """Logs a deletion of a file by the virus

        :param virus_id: The file number of the Virus that deleted the file
        :param file: The total pathname of the file that was deleted
        """
        self.__deleted_normal_files += 1
        self.__deletion_log.append((virus_id, file, self.__virus_file_locations[str(virus_id)]))

    def get_tracked_files(self) -> List[str]:
        """Returns a list of tracked files including the full path"""
        return list(self.__tracked_files)

    def track_virus(self, file: VirusFile):
        """Keeps track of a virus file by storing the parent Directory of the
        virus file
        """
        if str(file) not in self.__tracked_files:
            self.__tracked_files.append(str(file))

    # # # # # # # # # # # # # # # # # # # #

    def increase_speed(self, virus_file: VirusFile):
        """Increases the speed of the deletion by the virus and moves
        the specified virus file to a new, random location
        In addition, a new virus file is generated somewhere on the system
        """
        if self.__speed > Save.MINIMUM_SPEED:
            self.__speed -= Save.SPEED_INTERVAL
        if str(virus_file) in self.__tracked_files:
            self.__tracked_files.remove(str(virus_file))

        self.__virus_files += 1
        new_dir = choose_random_directory(self.__root)
        old_dir = virus_file.get_parent()
        old_dir.remove_entry(virus_file)
        virus_file.set_parent(new_dir)
        new_dir.add_entry(virus_file)

        virus_file_2nd_parent = generate_virus(self.__root, self.__virus_files)
        self.__virus_file_locations[str(self.__virus_files)] = virus_file_2nd_parent

    def remove_virus(self, virus_file: VirusFile):
        """Removes the given virus file from the list of possible
        viruses to be used to delete any files on the system
        """
        self.__deleted_virus_files += 1
        old_dir = virus_file.get_parent()
        old_dir.remove_entry(old_dir)
        del virus_file

    # # # # # # # # # # # # # # # # # # # #

    def save(self):
        """Saves the current state of the game into a custom file"""

        # Create the game saves directory if necessary
        if not os.path.exists(Save.SAVE_FOLDER):
            os.mkdir(Save.SAVE_FOLDER)

        # Create this saves' directory
        if not os.path.exists(f"{Save.SAVE_FOLDER}/{self.get_username()}"):
            os.mkdir(f"{Save.SAVE_FOLDER}/{self.get_username()}")

        save_json = {
            "username": self.__username,
            "speed": self.__speed,
            "virus_files": {
                "deleted": self.__deleted_virus_files,
                "total": self.__virus_files,
                "tracked": self.__tracked_files,
                "locations": self.__virus_file_locations
            },
            "normal_files": {
                "deleted": self.__deleted_normal_files,
                "total": self.__normal_files,
                "log": self.__deletion_log
            }
        }
        system_json = {
            "root": self.__root.to_json(),
            "trash": self.__trash.to_json()
        }
        Hexable.save(save_json, f"{Save.SAVE_FOLDER}/{self.get_username()}/save.hex")
        Hexable.save(system_json, f"{Save.SAVE_FOLDER}/{self.get_username()}/filesystem.hex")

    def load(self):
        """Loads a save file based on the username, if it exists

        :raises FileNotFoundError: When the save file for the username does not exist
        """
        save_json = Hexable.load(f"{Save.SAVE_FOLDER}/{self.__username}/save.hex")

        self.__speed = save_json.get("speed", 60)

        self.__deleted_virus_files = save_json["virus_files"]["deleted"]
        self.__virus_files = save_json["virus_files"]["total"]
        self.__tracked_files = save_json["virus_files"]["tracked"]
        self.__virus_file_locations = save_json["virus_files"]["locations"]

        self.__deleted_normal_files = save_json["normal_files"]["deleted"]
        self.__normal_files = save_json["normal_files"]["total"]
        self.__deletion_log = save_json["normal_files"]["log"]
