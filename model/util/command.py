from typing import List

from model import Entry, Directory, NormalFile


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
        if target == ".":
            entry = console.get_current_dir()
        elif target == "..":
            entry = console.get_current_dir().get_parent()
        else:
            entry = console.get_current_dir().get_entry(target)
        if entry:
            if len(targets) > 1:
                results.append(f"{target}{':' if isinstance(entry, Directory) else ''}")
            if isinstance(entry, Directory):
                results.append(entry.list_contents(options["show_hidden"]["value"]))
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

    current_dir = console.get_current_dir()
    result = []
    for file in args:
        if file == "." or file == "..":
            result.append(f"cat: {file}: Is a directory")
        else:
            for entry in current_dir.get_entries():
                if entry.get_name() == file:
                    if isinstance(entry, Directory):
                        result.append(f"cat: {entry.get_name()}: Is a directory")
                        break
                    else:
                        file_result = ""
                        total = 0
                        for byte in entry.get_bytes():
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
