from typing import List

from model import NormalFile


class VirusFile(NormalFile):
    """The VirusFile class is the structure that acts as a Virus File on the
    filesystem that still has lines of data but also deletes files that are
    not other virus files in the filesystem

    :param number: The number to give to the Virus File
    :param name: The name to give to the Virus File
    :param lines: The list of lines to put inside the Virus File
    """

    def __init__(self, number: int, name: str, lines: List[str] = None):
        super().__init__(name, lines)
        self.__number = number

    def __str__(self):
        return f"VirusFile(\"{self.get_name()}\", size: {self.get_size()} bytes)"

    # # # # # # # # # # # # # # # # # # # #

    def get_number(self) -> int:
        """Returns the number of this VirusFile"""
        return self.__number

    # # # # # # # # # # # # # # # # # # # #

    def to_json(self) -> dict:
        return {
            "type": "VirusFile",
            "number": self.get_number(),
            "name": self.get_name(),
            "size": self.get_size()}

    @staticmethod
    def from_json(json: dict):
        """Converts a JSON object into a VirusFile object

        :param json: The JSON object to convert
        :raises TypeError: When json.type is not 'VirusFile'
        :raises KeyError: When the VirusFile's number or name is not specified in the JSON object
        """
        if json["type"] != "VirusFile":
            raise TypeError(f"Type of JSON object must match (\"{json['type']}\" != \"VirusFile\")")
        if "number" not in json:
            raise KeyError("\"number\" key must exist to create VirusFile object")
        if "name" not in json:
            raise KeyError("\"name\" key must exist to create VirusFile object")

        return VirusFile(json["number"], json["name"], json.get("lines", []))
