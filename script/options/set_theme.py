from model.util import ls, Options


def set_theme(console, command):
    """Controls the logic surrounding the set_theme.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    if command.split("/")[-1] == "set_theme.sh":
        console["on_set_theme"] = True
        result = ls(console, [str(console.get_current_dir().get_entry("themes"))])
        return f"@prompt:{result}\nEnter a theme name: "

    elif console["on_set_theme"]:
        console["on_set_theme"] = False
        for theme, _ in console.get_themes():
            if theme.get_name() == command:
                console.set_current_theme(command)
                Options.get_instance().set_last_theme(command)
                return f"{theme.get_name()} set as new theme"
        return f"{command} is not a valid theme"
