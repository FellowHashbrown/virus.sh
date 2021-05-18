from model.error import InvalidNameError


def new_game(console, command):
    """Controls the logic surrounding the new_game.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    if command.split("/")[-1] == "new_game.sh":
        console["on_new_game"] = True
        return "@prompt:Enter a username: "

    elif console["on_new_game"]:
        console["on_new_game"] = False
        for gamesave, _ in console.get_saves():
            if gamesave.get_username() == command:
                return f"{gamesave.get_username()} already exists!"
        try:
            console.set_save(command)
            console.in_play()
            return f"Created gamesave {console.get_save().get_username()} ..."
        except InvalidNameError as e:
            return str(e)
