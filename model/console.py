from model import Directory, NormalFile
from model.util import *


class Console:

    def __init__(self):
        self.__save = None
        self.__trash = Directory("Trash")
        self.__current_menu = "main_menu"
        self.__current_dir = None
        self.__root = None

        self.main_menu()

    # # # # # # # # # # # # # # # # # # # #

    def set_save(self, username: str):
        self.__save = Save(username)
        try:
            self.__save.load()
        except FileNotFoundError:
            self.__save.save()
            self.__save.load()
        self.__root = self.__save.get_root()
        self.__current_dir = self.__root.get_entry("usr").get_entry(username)

    def set_current_menu(self, menu: str):
        self.__current_menu = menu

    def set_current_dir(self, directory: Directory):
        self.__current_dir = directory

    # # # # # # # # # # # # # # # # # # # #

    def get_save(self) -> Save:
        return self.__save

    def get_trash(self) -> Directory:
        return self.__trash

    def get_current_menu(self) -> str:
        return self.__current_menu

    def get_current_dir(self) -> Directory:
        return self.__current_dir

    def get_root(self) -> Directory:
        return self.__root

    def get_prompt(self, in_play: bool) -> str:
        prompt = f"virus.sh@{'play' if in_play else 'main'} {self.__current_dir.get_name()}"
        prompt_char = Options.get_instance().get_prompt_char()
        return f"{prompt} {prompt_char} "

    # # # # # # # # # # # # # # # # # # # #

    def parse(self, cmd: str) -> str:
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

    # # # # # # # # # # # # # # # # # # # #

    def main_menu(self):
        self.__current_dir = Directory("main_menu")

        play_dir = Directory("play", parent=self.__current_dir)
        play_new = NormalFile("new_game.sh", parent=play_dir)
        play_load = NormalFile("load_game.sh", parent=play_dir)
        play_dir.add_entries(play_new, play_load)

        game_saves = Directory("gameSaves", parent=self.__current_dir)

        options_dir = Directory("options", parent=self.__current_dir)
        options_char = NormalFile("change_prompt_character.sh", parent=options_dir)
        options_dir.add_entries(options_char)

        self.__current_dir.add_entries(play_dir, game_saves, options_dir)
