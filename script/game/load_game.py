from model.util.command import ls


def load_game(console, command):
    """Controls the logic surrounding the load_game.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    if command.split("/")[-1] == "load_game.sh":
        console["on_load_game"] = True
        result = ls(console, [str(console.get_current_dir().get_entry("gameSaves"))])
        return f"@prompt:{result}\nEnter a username: "

    elif console["on_load_game"]:
        console["on_load_game"] = False
        for gamesave, _ in console.get_saves():
            if gamesave.get_username() == command:
                gamesave.generate()
                console.set_save(gamesave.get_username())
                console.in_play()
                return f"Loaded gamesave {gamesave.get_username()} ..."
        return f"No gamesave found for {command}"
