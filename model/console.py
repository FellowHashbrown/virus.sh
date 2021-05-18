from typing import List, Optional, Tuple, Union

from model import Directory, NormalFile, SaveFile
from model.error import InvalidNameError
from model.theme import Theme, Element
from model.util import *

from script import run_script


class Console:
    """The Console class is what keeps track of the current save, the current directory
    the root directory, the current menu (if on the main menu), and the trash directory
    """

    VIRUS_WEIGHT = 0.7
    NORMAL_WEIGHT = 0.3

    def __init__(self, console_ui):
        self.__console_ui = console_ui
        self.__save = None
        self.__in_play = False
        self.__current_dir = None
        self.__previous_dir = None

        # Main Menu Script states
        self.__on_new_game = False
        self.__on_load_game = False
        self.__on_delete_game = False

        self.__on_prompt_char = False
        self.__on_set_theme = False

        self.__on_new_theme = False
        self.__on_edit_theme = False
        self.__on_delete_theme = False

        # Game variables
        self.__virus = None
        self.__saves = []
        self.__themes = []
        self.__current_theme = None

        self.main_menu()

    def __getitem__(self, key: str):
        if key == "on_new_game":
            return self.__on_new_game
        elif key == "on_load_game":
            return self.__on_load_game
        elif key == "on_delete_game":
            return self.__on_delete_game

        elif key == "on_prompt_char":
            return self.__on_prompt_char
        elif key == "on_set_theme":
            return self.__on_set_theme

        elif key == "on_new_theme":
            return self.__on_new_theme
        elif key == "on_edit_theme":
            return self.__on_edit_theme
        elif key == "on_delete_theme":
            return self.__on_delete_theme

    def __setitem__(self, key: str, value: bool):
        if key == "on_new_game":
            self.__on_new_game = value
        elif key == "on_load_game":
            self.__on_load_game = value
        elif key == "on_delete_game":
            self.__on_delete_game = value

        elif key == "on_prompt_char":
            self.__on_prompt_char = value
        elif key == "on_set_theme":
            self.__on_set_theme = value

        elif key == "on_new_theme":
            self.__on_new_theme = value
        elif key == "on_edit_theme":
            self.__on_edit_theme = value
        elif key == "on_delete_theme":
            self.__on_delete_theme = value

    # # # # # # # # # # # # # # # # # # # #

    def set_save(self, username: str):
        """Sets the save object being used for the Console

        If no save is found with the username, one will be created

        :param username: The username of the object to load from
        """
        self.__save = Save(username)
        self.__save.generate()
        self.__current_dir = self.__save.get_root().get_entry("usr").get_entry(username)
        self.__virus = Virus(self.__save, self.game_over)

    def set_current_dir(self, directory: Directory):
        """Sets the current directory for the console"""
        self.__current_dir = directory

    def set_previous_dir(self, directory: Directory):
        """Sets the previous directory for the console to be used later after leaving the Trash directory"""
        self.__previous_dir = directory

    # # # # # # # # # # # # # # # # # # # #

    def get_saves(self) -> List[Save]:
        """Returns the list of saves that exist in the game"""
        return list(self.__saves)

    def get_save(self) -> Save:
        """Returns the current save being used by the console"""
        return self.__save

    def get_root(self) -> Directory:
        """Returns the very root of the filesystem"""
        return self.__save.get_root()

    def get_trash(self) -> Directory:
        """Returns the Trash directory"""
        return self.__save.get_trash()

    def remove_save(self, username: str):
        """Removes the save with the specified username from the Saves list"""
        for i in range(len(self.__saves)):
            if self.__saves[i][0].get_username() == username:
                self.__saves.pop(i)
                self.__current_dir.get_entry("gameSaves").remove_entry(username)
                break

    def get_current_dir(self) -> Directory:
        """Returns the current directory"""
        return self.__current_dir

    def get_previous_dir(self) -> Directory:
        """Returns the previous directory which is what is used when going back from the Trash"""
        return self.__previous_dir

    def get_prompt(self) -> str:
        """Returns the command line prompt in the console"""
        prompt = f"virus.sh@{'play' if self.__in_play else 'main'} {self.__current_dir.get_name()}"
        prompt_char = Options.get_instance().get_prompt_char()
        return f"{prompt} {prompt_char} "

    def get_prompt_indices(self) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        """Returns a 3-tuple of 2-tuples for the prompt indices meant for the theme options"""
        game_indices = (0, 8)
        menu_indices = (9, 13)
        curdir_indices = (14, 14 + len(self.__current_dir.get_name()))
        return game_indices, menu_indices, curdir_indices

    def is_in_play(self) -> bool:
        """Returns whether or not a game is currently being played"""
        return self.__in_play

    def in_play(self):
        """Sets the game as being currently played"""
        self.__in_play = True

    # # # # # # # # # # # # # # # # # # # #

    def parse(self, cmd: str) -> Optional[str]:
        """Parses the given command"""
        cmd = cmd.split(" ")
        cmd, args = cmd[0], cmd[1:]

        # Run the commands like normal
        if cmd == "clear":
            return "@clear"
        elif cmd == "ls":
            return ls(self, args)
        elif cmd == "cd":
            return cd(self, args)
        elif cmd == "cat" and self.__in_play:
            return cat(self, args)
        elif cmd == "rm" and self.__in_play:
            return rm(self, args)
        elif cmd == "track" and self.__in_play:
            return track(self, args)
        elif cmd == "mntr" and self.__in_play:
            return mntr(self, args)
        elif cmd == "trace" and self.__in_play:
            return trace(self, args)
        elif cmd == "restore" and self.__in_play:
            return restore(self, args)
        elif cmd == "exit":
            if self.__in_play:
                self.__in_play = False
                self.__save.save()
                return "@main_menu"
            return "@exit"

        # Check if a "script" was run from one of the main menu folders
        elif not self.is_in_play():
            return run_script(self, cmd)

    # # # # # # # # # # # # # # # # # # # #

    def game_over(self):
        """The function called when the player has lost the game
        and all the files on the system are deleted
        """
        self.__in_play = False
        return "@game_over"

    def get_themes(self) -> list:
        """Loads the themes from the theme file into the console"""
        return self.__themes

    def get_current_theme(self) -> str:
        """Returns the name of the theme that is currently set"""
        return self.__current_theme

    def set_current_theme(self, theme: str):
        """Sets the current console theme to the one specified"""
        self.__current_theme = theme

    def add_theme(self, theme: Theme):
        """Adds a new theme to the theme list"""
        theme_str = ("name: {}\n" +
                     "\tgame (bg/fg): {}/{}\n" +
                     "\tmenu (bg/fg): {}/{}\n" +
                     "\tcurrent directory (bg/fg): {}/{}\n" +
                     "\tdirectories (bg/fg): {}/{}\n" +
                     "\tfiles (bg/fg): {}/{}").format(
            theme.get_name(),
            theme["game"]["bg"], theme["game"]["fg"],
            theme["menu"]["bg"], theme["menu"]["fg"],
            theme["curdir"]["bg"], theme["curdir"]["fg"],
            theme["directory"]["bg"], theme["directory"]["fg"],
            theme["file"]["bg"], theme["file"]["fg"])
        theme = (theme, theme_str)
        self.__themes.append(theme)
        self.__console_ui.add_theme(theme[0])

    def load_saves(self):
        """Loads the saves from the Save directory"""
        self.__saves: List[Union[Tuple[Save, str], Save]] = Save.load_saves()
        for i in range(len(self.__saves)):
            v_d, v_t = self.__saves[i].get_virus_files()  # Deleted virus files, Total virus files
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

    def load_themes(self):
        """Loads the themes from the Theme directory"""
        self.__themes: List[Union[Tuple[Theme, str], Theme]] = Theme.load_themes()
        for i in range(len(self.__themes)):
            theme_str = ("name: {}\n" +
                         "\tgame (bg/fg): {}/{}\n" +
                         "\tmenu (bg/fg): {}/{}\n" +
                         "\tcurrent directory (bg/fg): {}/{}\n" +
                         "\tdirectories (bg/fg): {}/{}\n" +
                         "\tfiles (bg/fg): {}/{}").format(
                self.__themes[i].get_name(),
                self.__themes[i]["game"]["bg"], self.__themes[i]["game"]["fg"],
                self.__themes[i]["menu"]["bg"], self.__themes[i]["menu"]["fg"],
                self.__themes[i]["curdir"]["bg"], self.__themes[i]["curdir"]["fg"],
                self.__themes[i]["directory"]["bg"], self.__themes[i]["directory"]["fg"],
                self.__themes[i]["file"]["bg"], self.__themes[i]["file"]["fg"])
            self.__themes[i] = (self.__themes[i], theme_str)

    def main_menu(self):
        """Generates the main menu mini filesystem when starting up the game"""

        # Set the main_menu current directory
        self.__current_dir = Directory("main_menu")
        if self.__virus:
            self.__virus.stop()
            self.__virus = None

        self.load_saves()
        self.load_themes()

        # Add the play directory
        play_dir = Directory("play", parent=self.__current_dir)
        play_new = NormalFile("new_game.sh", parent=play_dir)
        play_load = NormalFile("load_game.sh", parent=play_dir)
        play_delete = NormalFile("delete_game.sh", parent=play_dir)
        play_dir.add_entries(play_new, play_load, play_delete)

        # Add the game saves directory, pulling from the saves loaded from above
        game_saves = Directory("gameSaves", parent=self.__current_dir)
        for save_obj in self.__saves:
            game_saves.add_entry(SaveFile(save_obj[0].get_username(), save_obj[1], game_saves))

        # Add the options directory / theme scripts
        options_dir = Directory("options", parent=self.__current_dir)
        options_char = NormalFile("change_prompt_character.sh", parent=options_dir)
        theme_new = NormalFile("new_theme.sh", parent=options_dir)
        theme_edit = NormalFile("edit_theme.sh", parent=options_dir)
        theme_delete = NormalFile("delete_theme.sh", parent=options_dir)
        theme_set = NormalFile("set_theme.sh", parent=options_dir)
        options_dir.add_entries(options_char, theme_new, theme_edit, theme_delete, theme_set)

        # Add the themes directory, pulling from the themes loaded from above
        themes = Directory("themes", parent=self.__current_dir)
        for theme_obj in self.__themes:
            themes.add_entry(SaveFile(theme_obj[0].get_name(), theme_obj[1], themes))

        self.__current_dir.add_entries(play_dir, game_saves, options_dir, themes)
