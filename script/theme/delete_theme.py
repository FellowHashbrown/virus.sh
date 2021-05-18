import os

from model.theme import Theme
from model.util import ls

on_verify = {"value": False,
             "target": None}


def delete_theme(console, command):
    """Controls the logic surrounding the delete_theme.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    global on_verify
    if command.split("/")[-1] == "delete_theme.sh":
        console["on_delete_theme"] = True
        result = ls(console, [str(console.get_current_dir().get_entry("themes"))])
        return f"@prompt:{result}\nEnter a theme name: "

    elif console["on_delete_theme"]:
        if not on_verify["value"]:
            for theme, _ in console.get_themes():
                if theme.get_name() == command:
                    on_verify = {"value": True,
                                 "target": theme}
                    return f"@prompt:Are you sure you want to delete {command}? (yes/no)"
            return f"No theme found for {command}"
        deleted = command.lower() in ["yes", "y"]
        target = on_verify["target"]
        on_verify = {"value": False,
                     "target": None}
        console["on_delete_theme"] = False
        if deleted:
            console.remove_theme(target)
            os.remove(f"{Theme.SAVE_FOLDER}/{target.get_name()}.hex")
            return f"{target.get_name()} theme deleted."
        return f"{target.get_name()} theme not deleted."
