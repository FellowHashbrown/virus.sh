from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from model import Directory

from model import NormalFile


class SaveFile(NormalFile):
    """A SaveFile is simply a file to display the basic data of an existing game
    save in the game that the user has played before.

    :param name: The username of the Save file
    :param data: The basic stats of the game
    :param parent: The parent Directory (which should be given the game save directory)
    """

    def __init__(self, name: str, data: str, parent: 'Directory' = None):
        super().__init__(name, parent)
        self._file_bytes = data

    def get_bytes(self) -> str:
        """Returns the basic data/stats specified by the Save file data"""
        return self._file_bytes
