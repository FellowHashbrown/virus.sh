from typing import Union

from model.error import InvalidFilenameError


class File:
    """The File class is the parent class for all directories, normal files, and virus files
    in the game.

    :param filename: The name to give to the file. *This will be checked for invalid characters*
    """

    INVALID_CHARS="?&:;|[]*,\""

    def __init__(self, filename: str):
        for invalid_char in File.INVALID_CHARS:
            if filename.find(invalid_char) != -1:
                raise InvalidFilenameError(f"{invalid_char} cannot exist in filename.")
        self.__filename = filename
        self.__lines = []

    def __str__(self):
        return f"File(\"{self.get_filename()}\")"

    # # # # # Modifiers # # # # #

    def add_line(self, line: str):
        """Adds a line to this File"""
        self.__lines.append(line)

    def remove_line(self, line: Union[int, str]):
        """Removes a line from this File

        :param line: The line number or line content to remove from the file
        """
        if isinstance(line, int):
            if

    # # # # # Setters # # # # #

    def set_filename(self, filename: str):
        """Sets the name of the file

        :param filename: The filename to rename the file to
        """
        self.__filename = filename

    # # # # # Getters # # # # #

    def get_filename(self) -> str:
        """Returns the name of this File"""
        return self.__filename

    def is_hidden(self) -> bool:
        """Returns whether or not this File is hidden"""
        return self.__filename.startswith(".")
