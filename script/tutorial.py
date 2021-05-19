from model.util import Options


tutorial_stage = -1
command_messages = [
    "The `ls` command lists all the directories and files in the directory you want!\n" +
    "If you leave it empty and just call `ls`, it will show you your current directory.\n",

    "The `cd` command lets you switch to other directories that are in the path.\n" +
    "If you run `cd ..` afterwards, it will bring you back to the original directory.\n" +
    "\tThe `..` directory means the parent directory so it will bring you back up",

    "The `cat` command prints out a file that exists on the directory.\n" +
    "The results are different from how they would normally be on an actual Linux computer\n" +
    "\tSo don't expect these results to be the same.\n" +
    "Note: you'll use this when trying to determine a virus file from a regular file!",

    "The `rm` command will remove a file, or directory, from the current directory.\n" +
    "If a directory has files or other directories in it, this won't remove it. You'll have to\n" +
    "\tuse the -r option to do so, for example `rm -r someDirectory`\n\n" +
    "Every other command after this does not exist in an actual Linux computer. These are all\n" +
    "\tspecifically designed for this game!",

    "The `track` command will allow you to keep track of a virus file you found when going through\n" +
    "the filesystem. For example, if you try running `track 1 someFile.txt` and then running `track`, you\n" +
    "should see it show up!\n" +
    "This exists because it would be annoying having to manually write down the virus files and their locations\n" +
    "while playing the game in case you find a virus file you can't delete yet!",

    "The `trace` command only works in the Trash directory! If you run this on one of the files in there,\n" +
    "This will spit out the directory that is one directory above where a Virus file exists!\n" +
    "\tFor example, if a virus file exists at `root/usr/username/directory1/directory2/virus.sh`\n" +
    "\tThe `trace` command will only show you up to `root/usr/username/directory1`\n" +
    "This exists so it doesn't make finding the virus too simple or else the game would be super short",

    "The `mntr` command will show you the most recently deleted file and also other things\n" +
    "such as what virus file was deleted last, how quickly the files are being deleted, what\n" +
    "regular file was deleted last by the virus, and how many files total the virus has deleted.",

    "The `restore` command only works in the Trash directory as well! This will move the file you specify\n" +
    "out of the Trash and back to where it belongs. You can also run `restore *` to restore all the files in there!",

    "The `help` command is pretty self-explanatory. I'm not going to go in-depth with that one. Just run it!",

    "The Trash directory is a bit different in the fake filesystem you're working with.\n" +
    "If you run the command `cd Trash`, you will be brought into the Trash directory.\n" +
    "There are no other directories inside of it but if you run `cd ..`, you will be brought\n"+
    "back to whichever directory you were at before you went to the Trash directory.",

    "There are color themes you can add into here to make the game just a little more colorful\n" +
    "and fun to play. If you try running the `ls options` command (after this tutorial), you can see the\n" +
    "list of possible 'scripts' to run. There is:\n" +
    "\t`new_theme.sh` which lets you create a new theme in the game\n" +
    "\t`edit_theme.sh` which lets you edit an already existing theme in the game\n" +
    "\t`delete_theme.sh` which allows you to delete a theme you may not use or like anymore!",

    "There are a couple options you have when playing the game which include:\n" +
    "\t`change_prompt_character.sh` which lets you change the little character (normally a $)\n" +
    "\t\tthat appears before you type\n" +
    "\t`set_theme.sh` which lets you choose an existing theme you've downloaded, or have made, to use!"
]


def tutorial_script(console, command):
    """Controls the logic surrounding the tutorial_script.sh fakescript
    in the game

    :param console: The console object that is responsible for the fake console
    :param command: The command that has been entered
    """
    global tutorial_stage
    if command.split("/")[-1] == "tutorial.sh" and not console.is_in_play():
        tutorial_stage += 1
        console.set_tutorial(True)
        return (
            "@prompt:You ran the tutorial script!\n" +
            "Here's a little hint when running main menu scripts:\n" +
            "\tYou don't need to specify the full path for the script you wanna run.\n" +
            "\nAll you have to do is start off with `./` and then tack on the name of the script\n" +
            "\tIt will automatically run, on the main menu, whether or not you're in the same\n" +
            "\tdirectory!\nPress enter when you're ready to move to all the commands and how they work!"
        )

    elif console.is_in_tutorial():
        if tutorial_stage < len(command_messages):
            tutorial_stage += 1
            return f"@prompt:{command_messages[tutorial_stage - 1]}"
        console.set_tutorial(False)
        Options.get_instance().set_tutorial(True)
        return ("That's the end of the tutorial! If you ever need it again, just run `./tutorial.sh`\n" +
                "\tHint: if you forget how the commands work, just run the `help` command!")
