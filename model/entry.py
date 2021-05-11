from model.abstract import Serializable, Sizable
from model.error import InvalidNameError


class Entry(Serializable, Sizable):
    """The Entry class is the parent class for Directory, NormalFile, and VirusFile
    in the game.

    :param name: The name to give to the Entry. *This will be checked for invalid characters*
    :raises InvalidNameError: When the name given has invalid characters.
    """

    INVALID_CHARS="?&:;|[]*,\""

    # # # # # # # # # # # # # # # # # # # #

    def __init__(self, name: str, parent: 'Directory' = None):
        for invalid_char in Entry.INVALID_CHARS:
            if name.find(invalid_char) != -1:
                raise InvalidNameError(f"{invalid_char} cannot exist in entry name.")
        self.__name: str = name
        self.__parent = parent

    def __str__(self):
        return f"Entry(\"{self.get_name()}\", size: {self.get_size()} bytes)"

    def __lt__(self, other: 'Entry'):
        return self.get_name() < other.get_name()

    def __le__(self, other: 'Entry'):
        return self.get_name() <= other.get_name()

    def __gt__(self, other: 'Entry'):
        return self.get_name() > other.get_name()

    def __ge__(self, other: 'Entry'):
        return self.get_name() >= other.get_name()

    def __eq__(self, other: 'Entry'):
        return self.get_name() == other.get_name()

    def __ne__(self, other: 'Entry'):
        return self.get_name() != other.get_name()

    # # # # # # # # # # # # # # # # # # # #

    def set_name(self, name: str):
        """Sets the name of the Entry"""
        self.__name: str = name

    def set_parent(self, parent: 'Directory'):
        """Sets the parent Directory of this Entry"""
        self.__parent= parent

    # # # # # # # # # # # # # # # # # # # #

    def get_name(self) -> str:
        """Returns the name of this Entry"""
        return self.__name

    def get_parent(self) -> 'Directory':
        """Returns the parent Directory of this Entry"""
        return self.__parent

    def is_hidden(self) -> bool:
        """Returns whether or not this Entry is hidden which is True
        if there is a "." at the beginning of the name
        """
        return self.__name.startswith(".")

    # # # # # # # # # # # # # # # # # # # #

    def to_json(self) -> dict:
        return {
            "type": "Entry",
            "name": self.get_name()}

    # # # # # # # # # # # # # # # # # # # #

    @staticmethod
    def from_json(json: dict):
        """Converts a JSON object into an Entry object

        :param json: The JSON object to convert
        :raises TypeError: When json.type is not 'Entry'
        :raises KeyError: When the Entry's name is not specified in the JSON object
        """
        if json["type"] != "Entry":
            raise TypeError(f"Type of JSON object must match (\"{json['type']}\" != \"Entry\")")
        if "name" not in json:
            raise KeyError("\"name\" key must exist to create Entry object")
        return Entry(json["name"])
