from typing import List, Tuple, Union

from model import Directory, NormalFile, SaveFile
from model.util import *


class Console:
    """The Console class is what keeps track of the current save, the current directory
    the root directory, the current menu (if on the main menu), and the trash directory
    """

    VIRUS_WEIGHT = 0.7
    NORMAL_WEIGHT = 0.3

    def __init__(self):
        self.__save = None
        self.__trash = Directory("Trash")
        self.__in_play = False
        self.__current_dir = None
        self.__previous_dir = None
        self.__root = None
        self.__tracked_files = {}

        self.main_menu()

    # # # # # # # # # # # # # # # # # # # #

    def set_save(self, username: str):
        """Sets the save object being used for the Console

        If no save is found with the username, one will be created

        :param username: The username of the object to load from
        """
        self.__save = Save(username)
        try:
            self.__save.load()
        except FileNotFoundError:
            self.__save.save()
            self.__save.load()
        self.__root = self.__save.get_root()
        self.__current_dir = self.__root.get_entry("usr").get_entry(username)

    def set_current_dir(self, directory: Directory):
        """Sets the current directory for the console"""
        self.__current_dir = directory

    def set_previous_dir(self, directory: Directory):
        """Sets the previous directory for the console to be used later after leaving the Trash directory"""
        self.__previous_dir = directory

    # # # # # # # # # # # # # # # # # # # #

    def get_save(self) -> Save:
        """Returns the current save being used by the console"""
        return self.__save

    def get_trash(self) -> Directory:
        """Returns the Trash directory"""
        return self.__trash

    def get_current_dir(self) -> Directory:
        """Returns the current directory"""
        return self.__current_dir

    def get_previous_dir(self) -> Directory:
        """Returns the previous directory which is what is used when going back from the Trash"""
        return self.__previous_dir

    def get_root(self) -> Directory:
        """Returns the very root of the filesystem"""
        return self.__root

    def get_prompt(self) -> str:
        """Returns the command line prompt in the console"""
        prompt = f"virus.sh@{'play' if self.__in_play else 'main'} {self.__current_dir.get_name()}"
        prompt_char = Options.get_instance().get_prompt_char()
        return f"{prompt} {prompt_char} "

    # # # # # # # # # # # # # # # # # # # #

    def parse(self, cmd: str) -> str:
        """Parses the given command"""
        cmd = cmd.split(" ")
        cmd, args = cmd[0], cmd[1:]

        if cmd == "clear":
            return "@clear"
        elif cmd == "ls":
            return ls(self, args)
        elif cmd == "cd":
            return cd(self, args)
        elif cmd == "cat":
            return cat(self, args)
        elif cmd == "rm":
            return rm(self, args)
        elif cmd == "exit":
            if self.__in_play:
                self.__in_play = False
                return "@clear"
            else:
                return "@exit"

    # # # # # # # # # # # # # # # # # # # #

    def main_menu(self):
        """Generates the main menu mini filesystem when starting up the game"""

        # Load the game saves from the game save folder
        saves: List[Union[Tuple[Save, str], Save]] = Save.load_saves()
        for i in range(len(saves)):
            save_str = ("username: {}\n" +
                        "\tvirus files (deleted/total): {}/{}\n" +
                        "\tnormal files (remaining/total): {}/{}\n" +
                        "\t{}% completed").format(
                saves[i].get_username(),
                *saves[i].get_virus_files(),
                *saves[i].get_normal_files(),
                round((saves[i].get_virus_files()[0] / saves[i].get_normal_files()[1]) * 100, 2))
            saves[i] = (saves[i], save_str)

        # Set the main_menu current directory
        self.__current_dir = Directory("main_menu")

        # Add the play directory
        play_dir = Directory("play", parent=self.__current_dir)
        play_new = NormalFile("new_game.sh", parent=play_dir)
        play_load = NormalFile("load_game.sh", parent=play_dir)
        play_dir.add_entries(play_new, play_load)

        # Add the game saves directory, pulling from the saves loaded from above
        game_saves = Directory("gameSaves", parent=self.__current_dir)
        for save_obj in saves:
            f = SaveFile(save_obj[0].get_username(), save_obj[1], game_saves)
            game_saves.add_entry(f)

        # Add the options directory
        options_dir = Directory("options", parent=self.__current_dir)
        options_char = NormalFile("change_prompt_character.sh", parent=options_dir)
        options_dir.add_entries(options_char)

        self.__current_dir.add_entries(play_dir, game_saves, options_dir)
