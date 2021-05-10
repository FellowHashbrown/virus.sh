from abc import abstractmethod


class Sizable:
    """An abstract class that child classes must implement
    for returning the size of the data structure
    """

    @abstractmethod
    def get_size(self) -> int:
        pass
