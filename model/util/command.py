from typing import List

from model import Entry, Directory, NormalFile


def __dir_arg_parse(console, directory_path: str) -> Entry:
    """Parses a concatenated directory path to return the proper target"""
    dir_split = directory_path.split("/")
    current_dir = console.get_current_dir()
    for target in dir_split:
        if target == "..":
            current_dir = current_dir.get_parent()
        elif current_dir.get_name() != target and target != ".":
            current_dir = current_dir.get_entry(target)
    return current_dir


def ls(console, args):
    """Mimics the ls command to list the contents of a Directory"""

    # Keep track of the options for the ls command
    options = {
        "show_hidden": {
            "identifier": "a",
            "value": False}}
    targets = []

    # Iterate through all of the args, separating options from targets
    for arg in args:
        if arg.startswith("-"):
            for opt in options:
                options[opt]["value"] = options[opt]["identifier"] in arg
        else:
            targets.append(arg)

    # List the results
    if len(targets) == 0:
        return console.get_current_dir().list_contents(options["show_hidden"]["value"])
    results = []
    for target in targets:
        current_dir = __dir_arg_parse(console, target)
        if current_dir:
            if len(targets) > 1:
                results.append(f"{target}{':' if isinstance(current_dir, Directory) else ''}")
            if isinstance(current_dir, Directory):
                results.append(current_dir.list_contents(options["show_hidden"]["value"]))
        else:
            results.append(f"ls: {target}: No such file or directory")
    return "\n".join(results)


def cd(console, args):
    """Mimics the cd command to change Directories"""
    if len(args) > 1:
        return "usage: cd <directory>"
    if len(args) == 0:
        while console.get_current_dir().get_parent():
            console.set_current_dir(console.get_current_dir().get_parent())
        return

    target = args[0].split("/")
    for tgt in target:
        current_dir = console.get_current_dir()
        if tgt == ".":
            continue
        elif tgt == "..":
            if current_dir == console.get_trash() and console.get_current_menu() == "play":
                console.set_current_dir(console.get_previous_dir())
            elif current_dir.get_parent():
                console.set_current_dir(current_dir.get_parent())
            continue
        elif tgt == "Trash":
            console.set_previous_dir(console.get_current_dir())
            console.set_current_dir(console.get_trash())
            return
        found = False
        for entry in current_dir.get_entries():
            if entry.get_name() == tgt:
                found = True
                console.set_current_dir(entry)
        if not found:
            return f"cd: {tgt}: No such file or directory"


def cat(console, args):
    if len(args) == 0:
        return "usage: cat <file(s)>"

    result = []
    for file in args:
        file = __dir_arg_parse(console, file)
        if file:
            if isinstance(file, Directory):
                result.append(f"cat: {file.get_name()}: Is a directory")
                break
            else:
                file_result = ""
                total = 0
                for byte in file.get_bytes():
                    file_result += f"{hex(byte)[2:].rjust(2, '0')} "
                    total += 1
                    if total % 16 == 0:
                        file_result += "\n"
                result.append(file_result)
    return "\n".join(result)


def rm(console, args):
    if len(args) == 0:
        return "usage: rm [-r] file ..."

    recursive = "-r" in args or (len(args) > 0 and args[0].startswith("-") and "r" in args[0])

    target = None
    for entry in console.get_current_dir().get_entries():
        if entry.get_name() == args[-1]:
            target = entry
    if not target:
        return f"rm: {args[-1]}: No such file or directory"
    removed = __rm_helper(target, recursive)
    console.get_current_dir().remove_entry(target)
    for entry in removed:
        entry.set_parent(console.get_trash())
    console.get_trash().add_entries(removed)


def __rm_helper(directory: Directory, recursive: bool = True) -> List[Entry]:
    removed = []
    for entry in directory.get_entries():
        if isinstance(entry, Directory):
            if entry.get_size() == 0 or recursive:
                removed.append(entry)
        elif isinstance(entry, NormalFile):
            removed.append(entry)
    for entry in removed:
        directory.remove_entry(entry)
    return removed


def trace(console, args):
    pass


def chunks(console, args):
    pass


def mntr(console, args):
    pass


def track(console, args):
    pass
