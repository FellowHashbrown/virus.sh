from shutil import rmtree

from model.util import Save, ls

on_verify = {"value": False,
             "target": None}


def delete_game(console, command):
    """Controls the logic surrounding the delete_game.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    global on_verify
    if command.split("/")[-1] == "delete_game.sh":
        console["on_delete_game"] = True
        result = ls(console, [str(console.get_current_dir().get_entry("gameSaves"))])
        return f"@prompt:{result}\nEnter a username: "

    elif console["on_delete_game"]:
        if not on_verify["value"]:
            for gamesave, _ in console.get_saves():
                if gamesave.get_username() == command:
                    on_verify = {"value": True,
                                 "target": command}
                    return f"@prompt:Are you sure you want to delete {command}? (yes/no)"
            return f"No gamesave found for {command}"
        deleted = command.lower() in ["yes", "y"]
        target = on_verify["target"]
        on_verify = {"value": False,
                     "target": None}
        console["on_delete_game"] = False
        if deleted:
            console.remove_save(target)
            rmtree(f"{Save.SAVE_FOLDER}/{target}")
            return f"{target} save deleted."
        return f"{target} save not deleted."
