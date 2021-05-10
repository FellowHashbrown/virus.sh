from abc import abstractmethod


class Listable:
    """An abstract class that child classes must implement
    if there are contents that can be listed simply by the name
    """

    @abstractmethod
    def list_contents(self):
        pass
