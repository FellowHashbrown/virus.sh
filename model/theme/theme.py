import os
from pathlib import Path
from typing import Union

from model.abstract import Serializable
from model.theme import Element
from model.util import Hexable


class Theme(Serializable):
    """A Theme is used to style the console with custom colors
    which can be configured using the console itself.
    """

    @staticmethod
    def from_json(json: dict):
        """Returns a Theme object given the specified JSON object"""
        if json.get("name") is None:
            raise KeyError("\"name\" attribute in Theme must be specified")
        return Theme(json["name"],
                     game = Element.from_json(json.get("game")),
                     menu = Element.from_json(json.get("menu")),
                     curdir = Element.from_json(json.get("curdir")),
                     directory = Element.from_json(json.get("directory")),
                     file = Element.from_json(json.get("file")))

    SAVE_FOLDER = f"{Path.home()}/virus.sh/themes"

    def __init__(self, name: str, *,
                 main: Element = None, game: Element = None,
                 menu: Element = None, curdir: Element = None,
                 directory: Element = None, file: Element = None):
        self.__name = name

        self.__main = main or Element()
        self.__game = game or Element()
        self.__menu = menu or Element()
        self.__curdir = curdir or Element()
        self.__directory = directory or Element()
        self.__file = file or Element()

    def __getitem__(self, key: str) -> Element:
        if key == "game":
            return self.__game
        elif key == "menu":
            return self.__menu
        elif key == "curdir":
            return self.__curdir
        elif key == "directory":
            return self.__directory
        elif key == "file":
            return self.__file
        elif key == "main":
            return self.__main

    def __setitem__(self, key: str, value: Union[Element, dict]):
        if isinstance(value, dict):
            value = Element.from_json(value)
        if key == "game":
            self.__game = value
        elif key == "menu":
            self.__menu = value
        elif key == "curdir":
            self.__curdir = value
        elif key == "directory":
            self.__directory = value
        elif key == "file":
            self.__file = value
        elif key == "main":
            self.__main = value

    def get_name(self) -> str:
        """Returns the name of this Theme"""
        return self.__name

    def to_json(self) -> dict:
        """Returns a JSON representation of this Theme object"""
        return {
            "main": self.__main.to_json(),
            "game": self.__game.to_json(),
            "menu": self.__menu.to_json(),
            "curdir": self.__curdir.to_json(),
            "directory": self.__directory.to_json(),
            "file": self.__file.to_json()}

    def save(self):
        """Saves the theme into the themes folder in the home path"""

        # Create the themes folder if necessary
        if not os.path.exists(Theme.SAVE_FOLDER):
            os.makedirs(Theme.SAVE_FOLDER)

        Hexable.save(self.to_json(), f"{Theme.SAVE_FOLDER}/{self.get_name()}.hex")

    def load(self):
        """Loads the theme with this name from the themes folder in the home path"""

        theme_json = Hexable.load(f"{Theme.SAVE_FOLDER}/{self.get_name()}.hex")

        self.__main = Element.from_json(theme_json["main"])
        self.__game = Element.from_json(theme_json["game"])
        self.__menu = Element.from_json(theme_json["menu"])
        self.__curdir = Element.from_json(theme_json["curdir"])
        self.__directory = Element.from_json(theme_json["directory"])
        self.__file = Element.from_json(theme_json["file"])
