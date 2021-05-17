from typing import Union

from model.abstract import Serializable
from model.theme import Element


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

    def __init__(self, name: str, *,
                 game: Element = None, menu: Element = None,
                 curdir: Element = None, directory: Element = None,
                 file: Element = None):
        self.__name = name

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

    def get_name(self) -> str:
        """Returns the name of this Theme"""
        return self.__name

    def to_json(self) -> dict:
        """Returns a JSON representation of this Theme object"""
        return {
            "name": self.get_name(),
            "game": self.__game.to_json(),
            "menu": self.__menu.to_json(),
            "curdir": self.__curdir.to_json(),
            "directory": self.__directory.to_json(),
            "file": self.__file.to_json()}

