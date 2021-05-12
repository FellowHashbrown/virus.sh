from random import randint
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from model import Directory

from model import Entry


class NormalFile(Entry):
    """The NormalFile class is the structure that acts as a File on the
    file system that has lines of data inside it

    :param name: The name to give to the File
    :param parent: The parent Directory of this NormalFile
    """

    MINIMUM_SIZE = 40
    MAXIMUM_SIZE = 100

    def __init__(self, name: str, parent: 'Directory' = None, size: int = None):
        super().__init__(name, parent)
        self.__size = randint(NormalFile.MINIMUM_SIZE, NormalFile.MAXIMUM_SIZE) if size is None else size
        self._file_bytes = []
        for byte in range(self.__size):
            self._file_bytes.append(randint(0, 255))

    # # # # # # # # # # # # # # # # # # # #

    def get_size(self) -> int:
        """Returns the size of this File (in bytes)"""
        return self.__size

    def get_bytes(self) -> List[int]:
        """Returns the bytes of this file"""
        return list(self._file_bytes)

    # # # # # # # # # # # # # # # # # # # #

    def to_json(self) -> dict:
        return {
            "type": "NormalFile",
            "name": self.get_name(),
            "size": self.get_size()}

    # # # # # # # # # # # # # # # # # # # #

    @staticmethod
    def from_json(json: dict):
        """Converts a JSON object into a NormalFile object

        :param json: The JSON object to convert
        :raises TypeError: When json.type is not 'NormalFile'
        :raises KeyError: When the NormalFile's name is not specified in the JSON object
        """
        if json["type"] != "NormalFile":
            raise TypeError(f"Type of JSON object must match (\"{json['type']}\")")
        if "name" not in json:
            raise KeyError("\"name\" key must exist to create NormalFile object")

        return NormalFile(json["name"], size=json.get("size"))
