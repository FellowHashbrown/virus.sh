from model.util import Options


def change_prompt_char(console, command):
    """Controls the logic surrounding the change_prompt_character.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    if command.split("/")[-1] == "change_prompt_character.sh":
        console["on_prompt_char"] = True
        return "@prompt:Enter the new prompt character: "

    elif console["on_prompt_char"]:
        if len(command) != 1:
            return "@prompt:The character must be only 1 character\nEnter the new prompt character: "
        Options.get_instance().set_prompt_char(command)
        console["on_prompt_char"] = False
