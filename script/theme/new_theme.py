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


def new_theme(console, command):
    """Controls the logic surrounding the new_theme.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    global new_theme_stage, new_theme_name, new_theme_names, new_theme_config, on_verify
    if command.split("/")[-1] == "new_theme.sh":
        console["on_new_theme"] = True
        new_theme_stage = -1
        new_theme_name = ""
        new_theme_config = [None] * len(new_theme_names)
        on_verify = False
        return "@prompt:Enter the theme name: "

    elif console["on_new_theme"]:
        if not on_verify:
            if new_theme_stage == -1:
                new_theme_name = command
                new_theme_stage += 1
                return f"@prompt:Enter the {new_theme_names[new_theme_stage]} color in the hex color format (#000000): "
            elif new_theme_stage < len(new_theme_names):
                if len(command) == 0:
                    if new_theme_stage % 2 == 0:  # Background
                        command = "black"
                    else:   # Foreground
                        command = "white"
                else:
                    if not command.startswith("#"):
                        command = f"#{command}"
                new_theme_config[new_theme_stage] = command
                new_theme_stage += 1
                if new_theme_stage < len(new_theme_names):
                    return f"@prompt:Enter the {new_theme_names[new_theme_stage]} color in the hex color format (#000000): "
            result = "\n".join([
                f"{new_theme_names[i]}: {new_theme_config[i] or 'Default'}"
                for i in range(len(new_theme_names))
            ])
            on_verify = True
            return f"@prompt:{result}\nConfirm choices (yes/no): "
        confirmed = command.lower() in ["yes", "y"]
        console["on_new_theme"] = False
        if confirmed:
            theme = Theme(new_theme_name,
                          game=Element(*new_theme_config[:2]),
                          menu=Element(*new_theme_config[2:4]),
                          curdir=Element(*new_theme_config[4:6]),
                          directory=Element(*new_theme_config[6:8]),
                          file=Element(*new_theme_config[8:10]))
            theme.save()
            console.add_theme(theme)
            return f"New theme ({theme.get_name()}) created and saved"
        return "New theme creation canceled"
