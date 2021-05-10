from abc import abstractmethod


class Serializable:
    """An abstract class that child classes must implement
    the abstract methods for JSON conversion and extraction
    """

    @staticmethod
    @abstractmethod
    def from_json(json: dict):
        pass

    @abstractmethod
    def to_json(self):
        pass
