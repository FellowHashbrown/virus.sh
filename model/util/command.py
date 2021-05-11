from typing import List

from model import Entry, Directory, NormalFile


def ls(console, args):
    """Mimics the ls command to list the contents of a Directory"""
    show_hidden = "-a" in args or (len(args) > 0 and "a" in args[0] and args[0].startswith("-"))
    return console.get_current_dir().list_contents(show_hidden)


def cd(console, args):
    """Mimics the cd command to change Directories"""
    if len(args) > 1:
        return "usage: cd <directory>"
    current_dir = console.get_current_dir()
    target = args[0]

    if target == ".":
        return
    elif target == "..":
        if current_dir.get_parent():
            console.set_current_dir(current_dir.get_parent())
        return
    for entry in current_dir.get_entries():
        if entry.get_name() == target:
            console.set_current_dir(entry)
            return


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
