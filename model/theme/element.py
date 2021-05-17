from model.abstract import Serializable


class Element(Serializable):
    """An Element is an object inside a Theme that holds background and foreground colors
    for individual elements
    """

    @staticmethod
    def from_json(json: dict):
        """Returns an Element object from the specified JSON object
        with the background and foreground colors
        """
        return Element(json.get("bg", Element.DEFAULT_BG),
                       json.get("fg", Element.DEFAULT_FG))

    DEFAULT_BG = "black"
    DEFAULT_FG = "white"

    def __init__(self, bg: str = None, fg: str = None):
        self.__bg = bg if bg is not None else Element.DEFAULT_BG
        self.__fg = fg if fg is not None else Element.DEFAULT_FG

    def __getitem__(self, item: str):
        if item.lower() in ["bg", "background", "back"]:
            return self.__bg
        elif item.lower() in ["fg", "foreground", "fore"]:
            return self.__fg

    def __setitem__(self, item: str, value: str):
        if item.lower() in ["bg", "background", "back"]:
            self.__bg = value
        elif item.lower() in ["fg", "foreground", "fore"]:
            self.__fg = value

    def to_json(self) -> dict:
        """Returns a JSON representation of this Element object"""
        return {
            "bg": self.__bg,
            "fg": self.__fg}
