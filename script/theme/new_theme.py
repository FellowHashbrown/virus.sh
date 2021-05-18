from model.theme import Theme, Element

new_theme_stage = -1
new_theme_name = ""
new_theme_names = ["game_bg", "game_fg",
                   "menu_bg", "menu_fg",
                   "curdir_bg", "curdir_fg",
                   "directory_bg", "directory_fg",
                   "file_bg", "file_fg"]
new_theme_config = [None] * len(new_theme_names)
on_verify = False
target_theme = None
valid_hex = "0123456789abcdefABCDEF"


def new_theme(console, command):
    """Controls the logic surrounding the new_theme.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    global new_theme_stage, new_theme_name, new_theme_names, new_theme_config, on_verify
    global target_theme
    if command.split("/")[-1] in ["new_theme.sh", "edit_theme.sh"]:
        console["on_new_theme"] = command.split("/")[-1] == "new_theme.sh"
        console["on_edit_theme"] = command.split("/")[-1] == "edit_theme.sh"
        new_theme_stage = -1
        new_theme_name = ""
        new_theme_config = [None] * len(new_theme_names)
        on_verify = False
        return "@prompt:Enter the theme name: "

    elif console["on_new_theme"] or console["on_edit_theme"]:
        if not on_verify:
            if new_theme_stage == -1:
                new_theme_stage += 1
                if console["on_edit_theme"]:
                    for theme in Theme.load_themes():
                        if theme.get_name() == command:
                            target_theme = theme
                            new_theme_name = command
                            new_theme_config = [
                                theme["game"]["bg"], theme["game"]["fg"],
                                theme["menu"]["bg"], theme["menu"]["fg"],
                                theme["curdir"]["bg"], theme["curdir"]["fg"],
                                theme["directory"]["bg"], theme["directory"]["fg"],
                                theme["file"]["bg"], theme["file"]["fg"]]
                            return "@prompt:Enter the new {} color in hex format or as a word (current: {}): ".format(
                                new_theme_names[new_theme_stage],
                                new_theme_config[new_theme_stage])
                    console["on_edit_theme"] = False
                    return f"No theme found with name {command}"
                new_theme_name = command
                return "@prompt:Enter the {} color in hex format or as a word: ".format(
                    new_theme_names[new_theme_stage])

            elif new_theme_stage < len(new_theme_names):
                if len(command) == 0:
                    if console["on_new_theme"]:
                        if new_theme_stage % 2 == 0:  # Background
                            command = "black"
                        else:   # Foreground
                            command = "white"
                    else:
                        command = new_theme_config[new_theme_stage]
                else:
                    if not command.startswith("#") and len([h for h in command if h in valid_hex]) == len(command):
                        command = f"#{command}"
                new_theme_config[new_theme_stage] = command
                new_theme_stage += 1
                if new_theme_stage < len(new_theme_names):
                    if console["on_edit_theme"]:
                        return "@prompt:Enter the {} color in hex format or as a word (current: {})".format(
                            new_theme_names[new_theme_stage],
                            new_theme_config[new_theme_stage])
                    return f"@prompt:Enter the {new_theme_names[new_theme_stage]} color in hex format or as a word: "

            result = "\n".join([
                f"{new_theme_names[i]}: {new_theme_config[i] or 'Default'}"
                for i in range(len(new_theme_names))
            ])
            on_verify = True
            return f"@prompt:{result}\nConfirm choices (yes/no): "

        confirmed = command.lower() in ["yes", "y"]
        was_on_edit = console["on_edit_theme"]
        console["on_new_theme"] = False
        console["on_edit_theme"] = False
        if confirmed:
            if was_on_edit:
                console.remove_theme(target_theme)
            theme = Theme(new_theme_name,
                          game=Element(*new_theme_config[:2]),
                          menu=Element(*new_theme_config[2:4]),
                          curdir=Element(*new_theme_config[4:6]),
                          directory=Element(*new_theme_config[6:8]),
                          file=Element(*new_theme_config[8:10]))
            theme.save()
            console.add_theme(theme)
            if was_on_edit:
                return f"Theme {theme.get_name()} updated and saved"
            return f"New theme ({theme.get_name()}) created and saved"
        if was_on_edit:
            return "Editing theme canceled"
        return "New theme creation canceled"
