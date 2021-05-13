from typing import List, Optional, Tuple, Union

from model import Directory, NormalFile, SaveFile
from model.error import InvalidNameError
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

        self.__on_new_game = False
        self.__on_load_game = False
        self.__on_prompt_char = False

        self.__saves: List[Union[Tuple[Save, str], Save]] = Save.load_saves()
        for i in range(len(self.__saves)):
            v_d, v_t = self.__saves[i].get_virus_files()   # Deleted virus files, Total virus files
            n_d, _ = self.__saves[i].get_normal_files()  # Deleted normal files, Total normal files
            n_r = self.__saves[i].get_restored_files()
            save_str = ("username: {}\n" +
                        "\tvirus files (deleted/total): {}/{}\n" +
                        "\tnormal files (restored/deleted): {}/{}\n" +
                        "\t{}% completed").format(
                self.__saves[i].get_username(),
                *self.__saves[i].get_virus_files(),
                self.__saves[i].get_restored_files(), n_d,
                round(
                    Console.VIRUS_WEIGHT * (v_d / (v_t if v_t != 0 else 1)) * 100 +
                    Console.NORMAL_WEIGHT * (n_r / (n_d if n_d != 0 else 1)) * 100, 2))
            self.__saves[i] = (self.__saves[i], save_str)

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
            self.__save.generate()
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

    def parse(self, cmd: str) -> Optional[str]:
        """Parses the given command"""
        cmd = cmd.split(" ")
        cmd, args = cmd[0], cmd[1:]

        # Check if a "script" was run from one of the main menu folders
        if cmd.startswith("./") and cmd.endswith(".sh") and not self.__in_play:
            if cmd.split("/")[-1] == "new_game.sh":
                self.__on_new_game = True
                return "@prompt:Enter a username: "
            elif cmd.split("/")[-1] == "load_game.sh":
                self.__on_load_game = True
                return f"@prompt:{ls(self, [str(self.get_current_dir().get_entry('gameSaves'))])}\nEnter the username: "
            elif cmd.split("/")[-1] == "change_prompt_character.sh":
                self.__on_prompt_char = True
                return "@prompt:Enter the new prompt character: "

        # Check the callback from the new game script
        elif self.__on_new_game:
            self.__on_new_game = False
            for gamesave, _ in self.__saves:
                if gamesave.get_username() == cmd:
                    return f"{gamesave.get_username()} already exists!"
            try:
                self.set_save(cmd)
                self.__in_play = True
                return f"Created gamesave {self.get_save().get_username()} ..."
            except InvalidNameError as e:
                return str(e)

        # Check the callback from the load game script
        elif self.__on_load_game:
            self.__on_load_game = False
            for gamesave, _ in self.__saves:
                if gamesave.get_username() == cmd:
                    self.set_save(gamesave.get_username())
                    self.__in_play = True
                    return f"Loaded gamesave {gamesave.get_username()} ..."
            return f"No gamesave found for {cmd}"

        # Check the callback from the prompt character script
        elif self.__on_prompt_char:
            if len(cmd) != 1:
                return "@prompt:The character must be only 1 character\nEnter the new prompt character: "
            Options.get_instance().set_prompt_char(cmd)
            self.__on_prompt_char = False
            return None

        # Run the commands like normal
        elif cmd == "clear":
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
                return "@main_menu"
            else:
                return "@exit"

    # # # # # # # # # # # # # # # # # # # #

    def main_menu(self):
        """Generates the main menu mini filesystem when starting up the game"""

        # Set the main_menu current directory
        self.__current_dir = Directory("main_menu")

        # Add the play directory
        play_dir = Directory("play", parent=self.__current_dir)
        play_new = NormalFile("new_game.sh", parent=play_dir)
        play_load = NormalFile("load_game.sh", parent=play_dir)
        play_dir.add_entries(play_new, play_load)

        # Add the game saves directory, pulling from the saves loaded from above
        game_saves = Directory("gameSaves", parent=self.__current_dir)
        for save_obj in self.__saves:
            f = SaveFile(save_obj[0].get_username(), save_obj[1], game_saves)
            game_saves.add_entry(f)

        # Add the options directory
        options_dir = Directory("options", parent=self.__current_dir)
        options_char = NormalFile("change_prompt_character.sh", parent=options_dir)
        options_dir.add_entries(options_char)

        self.__current_dir.add_entries(play_dir, game_saves, options_dir)
