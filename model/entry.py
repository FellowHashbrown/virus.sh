from typing import Optional

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
        self.__original_parent = str(parent)

    def __str__(self):
        if self.__parent:
            return f"{str(self.__parent)}/{self.__name}"
        return self.__name

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
        self.__name = name

    def set_parent(self, parent: 'Directory'):
        """Sets the parent Directory of this Entry"""
        self.__parent = parent

    def set_original_parent(self, parent: 'Directory'):
        """Sets the original parent Directory of this Entry"""
        self.__original_parent = parent

    # # # # # # # # # # # # # # # # # # # #

    def get_name(self) -> str:
        """Returns the name of this Entry"""
        return self.__name

    def get_parent(self) -> 'Directory':
        """Returns the parent Directory of this Entry"""
        return self.__parent

    def get_original_parent(self) -> 'Directory':
        """Returns the original Directory the Entry started out in
        before being deleted"""
        return self.__original_parent

    def is_hidden(self) -> bool:
        """Returns whether or not this Entry is hidden which is True
        if there is a "." at the beginning of the name
        """
        return self.__name.startswith(".")

    def restore(self, root: 'Directory') -> Optional['Entry']:
        """Restores the entry to its original parent
        when the file was created if the parent was given

        :param root: The root Directory of the entire filesystem which is used to
            parse through the original parent to set the original parent after the file is restored
        """
        print(self.get_parent(), self.__original_parent)
        if self.get_parent():
            self.get_parent().remove_entry(self)
            target = root
            orig_parent_split = self.__original_parent.split("/")
            for entry in orig_parent_split[1:]:  # Ignore the root entry since that's where we are at
                target = target.get_entry(entry)
                if target is None:
                    return
            self.set_parent(target)
            self.__parent.add_entry(self)
            return self

    # # # # # # # # # # # # # # # # # # # #

    def to_json(self) -> dict:
        return {
            "type": "Entry",
            "parent": self.__original_parent,
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
        entry = Entry(json["name"])
        entry.__original_parent = json["parent"]
        return entry
