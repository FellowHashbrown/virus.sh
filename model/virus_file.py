from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Directory

from model import NormalFile


class VirusFile(NormalFile):
    """The VirusFile class is the structure that acts as a Virus File on the
    filesystem that still has lines of data but also deletes files that are
    not other virus files in the filesystem

    :param number: The number to give to the VirusFile
    :param name: The name to give to the VirusFile
    :param parent: The parent directory of this VirusFile
    """

    IDENTIFYING_BYTES = [124, 56, 198, 248, 119, 64, 87, 12]
                # in hex: 7c, 38,  c6,  f8,  77, 40, 57, 0c

    def __init__(self, number: int, name: str, parent: 'Directory' = None):
        super().__init__(name, parent)
        self.__number = number
        for byte in range(len(VirusFile.IDENTIFYING_BYTES)):
            self._file_bytes[byte] = VirusFile.IDENTIFYING_BYTES[byte]
        self._file_bytes[-1] = number

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

        return VirusFile(json["number"], json["name"])
