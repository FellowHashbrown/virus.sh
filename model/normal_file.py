from random import randint
from typing import List

from model import Entry


class NormalFile(Entry):
    """The NormalFile class is the structure that acts as a File on the
    file system that has lines of data inside it

    :param name: The name to give to the File
    :param lines: The list of lines to put inside the File
    """

    def __init__(self, name: str, size: int = None):
        super().__init__(name)
        self.__size = randint(20, 1000) if size is None else size
        file_bytes = []
        for byte in range(self.__size):
            file_bytes.append(randint(0, 255))

    def __str__(self):
        return f"NormalFile(\"{self.get_name()}\", size: {self.get_size()} bytes)"

    # # # # # # # # # # # # # # # # # # # #

    def get_size(self) -> int:
        """Returns the size of this File (in bytes)"""
        return self.__size

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

        return NormalFile(json["name"], json.get("size"))
