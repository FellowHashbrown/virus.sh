from typing import List

from model import Entry


class NormalFile(Entry):
    """The NormalFile class is the structure that acts as a File on the
    file system that has lines of data inside it

    :param name: The name to give to the File
    :param lines: The list of lines to put inside the File
    """

    def __init__(self, name: str, lines: List[str] = None):
        super().__init__(name)
        if lines is None:
            lines = []
        self.__lines = lines

    def __str__(self):
        return f"NormalFile(\"{self.get_name()}\", size: {self.get_size()} bytes)"

    # # # # # # # # # # # # # # # # # # # #

    def get_size(self) -> int:
        """Returns the size of this File (in bytes)"""
        total_size = len(self.__lines)
        for line in self.__lines:
            total_size += len(line)
        return total_size

    def get_lines(self) -> List[str]:
        """Returns the lines in this File"""
        return list(self.__lines)

    # # # # # # # # # # # # # # # # # # # #

    def add_line(self, line: str):
        """Adds a new line to this File"""
        self.__lines.append(line)

    def add_lines(self, lines: List[str]):
        """Adds a list of lines to this File"""
        for line in lines:
            self.add_line(line)

    def insert_line(self, line: str, index: int):
        """Inserts a line at the specified index

        If the index is out of range, it will not be inserted

        :param line: The line to add
        :param index: The index to insert the line at
        """
        if 0 <= index < len(self.__lines):
            self.__lines.insert(index, line)

    def insert_lines(self, lines: List[str], index: int):
        """Inserts a list of lines starting at the given index

        If the beginning index is out of range, none of the lines
        will be inserted

        :param lines: The list of lines to insert
        :param index: The index to start inserting at
        """
        for line in lines:
            self.insert_line(line, index)
            index += 1

    def remove_line(self, index: int) -> bool:
        """Removes the line at the specified index and returns whether
        or not the line was removed.
        """
        if 0 <= index < len(self.__lines):
            self.__lines.pop(index)
            return True
        return False

    def remove_lines(self, indices: List[int]):
        """Removes the lines at the specified indices if possible"""
        for index in indices:
            self.remove_line(index)

    # # # # # # # # # # # # # # # # # # # #

    def to_json(self) -> dict:
        return {
            "type": "NormalFile",
            "name": self.get_name(),
            "lines": self.get_lines()}

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

        return NormalFile(json["name"], json.get("lines", []))
