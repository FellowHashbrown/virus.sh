from typing import List, Optional, Union

from model import Entry, NormalFile, VirusFile, Trash
from model.abstract import Listable


class Directory(Listable, Entry):
    """The Directory class is the structure that acts as an actual Directory
    on a filesystem that can hold Files and other Directories

    :param name: The name to give to the Directory
    :param entries: The list of Entry objects to put inside of the Directory
    """

    def __init__(self, name: str, entries: List[Entry] = None):
        super().__init__(name)
        if entries is None:
            entries = []
        self.__entries = entries

    def __str__(self):
        return f"Directory(\"{self.get_name()}\", size: {self.get_size()} bytes)"

    # # # # # # # # # # # # # # # # # # # #

    def get_size(self) -> int:
        """Returns the size of this Directory (in bytes)"""
        total_size = 0
        for entry in self.__entries:
            total_size += entry.get_size()
        return total_size

    def get_entries(self) -> List[Entry]:
        """Returns the list of Entries in this Directory"""
        return list(self.__entries)

    def is_populated(self):
        """Returns whether or not there are any items in this Directory"""
        return len(self.__entries) > 0

    # # # # # # # # # # # # # # # # # # # #

    def add_entry(self, entry: Entry) -> bool:
        """Adds a new Entry to this Directory and returns whether or not
        the Entry was added.

        If the name of the Entry given already exists, it will not be added.
        """
        for e in self.get_entries():
            if e.get_name() == entry.get_name():
                return False
        self.__entries.append(entry)
        self.__entries.sort()
        return True

    def remove_entry(self, entry: Union[int, str, Entry]) -> Optional[Entry]:
        """Removes the specified Entry from this Directory and returns it, if applicable

        The Entry can be specified by an offset, an Entry name, or an
        actual Entry object.

        If no Entry is found with the specified data, nothing will be returned

        :param entry: The target Entry to remove from the Directory
        """
        if isinstance(entry, Entry):
            target = entry
        elif isinstance(entry, int):
            target = self.__entries[entry]
        else:
            target = None
            for e in self.__entries:
                if e.get_name() == entry:
                    target = e
            if target is None:
                return None
        if isinstance(target, Directory) and target.is_populated():
            return None
        self.__entries.remove(target)
        return target

    # # # # # # # # # # # # # # # # # # # #

    def list_contents(self, show_hidden: bool = False):
        """Returns a newline-separated string of the names of the
        Entries contained within this Directory.

        :param show_hidden: Whether or not to show hidden files or directories
        """
        return "\n".join([
            entry.get_name()
            for entry in self.get_entries()
            if not entry.is_hidden() or show_hidden])

    def to_json(self) -> dict:
        return {
            "type": "Directory",
            "name": self.get_name(),
            "entries": [entry.to_json() for entry in self.__entries]}

    # # # # # # # # # # # # # # # # # # # #

    @staticmethod
    def from_json(json: dict):
        """Converts a JSON object into a Directory object

        :param json: The JSON object to convert
        :raises TypeError: When json.type is not 'Directory'
        :raises KeyError: When the Directory's name is not specified in the JSON object
        :raises ValueError: When an Entry in the Directory is of an unknown type
        """
        if json["type"] != "Directory":
            raise TypeError(f"Type of JSON object must match (\"{json['type']}\" != \"Directory\")")
        if "name" not in json:
            raise KeyError("\"name\" key must exist to create Directory object")

        entries = []
        for entry in json.get("entries", []):
            if entry["type"] == "NormalFile":
                entries.append(NormalFile.from_json(entry))
            elif entry["type"] == "VirusFile":
                entries.append(VirusFile.from_json(entry))
            elif entry["type"] == "Directory":
                entries.append(Directory.from_json(entry))
            elif entry["type"] == "Trash":
                entries.append(Trash.from_json(entry))
            else:
                raise ValueError(f"\"{entry['type']}\" not recognized as an Entry type")
        entries.sort()
        return Directory(json["name"], entries)
