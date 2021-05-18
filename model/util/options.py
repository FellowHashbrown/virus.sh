import os
from pathlib import Path

from model.util import Hexable


class Options:

    __instance = None
    SAVE_FOLDER = f"{Path.home()}/virus.sh"

    @staticmethod
    def get_instance():
        if Options.__instance is None:
            Options.__instance = Options()
        return Options.__instance

    @staticmethod
    def save():
        options_json = {
            "prompt_char": Options.get_instance().get_prompt_char()
        }
        Hexable.save(options_json, f"{Options.SAVE_FOLDER}/options.hex")

    def __init__(self):
        if Options.__instance is None:

            # Defaults
            prompt_char = "$"

            # Create the game directory if necessary
            if not os.path.exists(Options.SAVE_FOLDER):
                os.makedirs(Options.SAVE_FOLDER)

            # Try loading the file
            if os.path.exists(f"{Options.SAVE_FOLDER}/options.hex"):
                options_json = Hexable.load(f"{Options.SAVE_FOLDER}/options.hex")
                prompt_char = options_json["prompt_char"]

            # Set the instance variables
            self.__prompt_char = prompt_char

        else:
            raise NameError("Instance of Options already exists. Use Options.get_instance()")

    # # # # # # # # # # # # # # # # # # # #

    def get_prompt_char(self) -> str:
        """Returns the character that is being used for the command line prompt"""
        return self.__prompt_char

    def set_prompt_char(self, prompt_char: str):
        """Sets the character that is being used for the command line prompt"""
        self.__prompt_char = prompt_char
        Options.save()
