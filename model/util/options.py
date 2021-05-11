class Options:

    __instance = None

    @staticmethod
    def get_instance():
        if Options.__instance is None:
            Options.__instance = Options()
        return Options.__instance

    def __init__(self):
        if Options.__instance is None:
            self.__prompt_char = "$"
        else:
            raise NameError("Instance of Options already exists. Use Options.get_instance()")

    # # # # # # # # # # # # # # # # # # # #

    def get_prompt_char(self) -> str:
        """Returns the character that is being used for the command line prompt"""
        return self.__prompt_char
