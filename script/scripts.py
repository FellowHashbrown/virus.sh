from script.game import new_game, load_game, delete_game
from script.options import change_prompt_char, set_theme
from script.theme import new_theme, delete_theme
from script.tutorial import tutorial_script


def run_script(console, command):
    """Runs a particular script from the main menu when specified
    and handles all logic individually but dynamically

    In other words, if there are multiple steps to a script which requires
    multiple pieces of input from the player, these "scripts" will handle that
    """
    if command.split("/")[-1] == "new_game.sh" or console["on_new_game"]:
        return new_game(console, command)
    elif command.split("/")[-1] == "load_game.sh" or console["on_load_game"]:
        return load_game(console, command)
    elif command.split("/")[-1] == "delete_game.sh" or console["on_delete_game"]:
        return delete_game(console, command)

    elif command.split("/")[-1] == "change_prompt_character.sh" or console["on_prompt_char"]:
        return change_prompt_char(console, command)
    elif command.split("/")[-1] == "set_theme.sh" or console["on_set_theme"]:
        return set_theme(console, command)

    elif command.split("/")[-1] in ["new_theme.sh", "edit_theme.sh"] or console["on_new_theme"] or console["on_edit_theme"]:
        return new_theme(console, command)
    elif command.split("/")[-1] == "delete_theme.sh" or console["on_delete_theme"]:
        return delete_theme(console, command)

    elif command.split("/")[-1] == "tutorial.sh" or console.is_in_tutorial():
        return tutorial_script(console, command)
