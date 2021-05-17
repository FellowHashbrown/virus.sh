from random import choice, randint
from typing import List, Tuple, Union

from model import Directory, NormalFile, VirusFile

valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-"
valid_exts = [".py", ".sh", ".png", ".jpeg", ".jpg", ".ico", ".c", ".dat", ".db",
              ".dbf", ".es6", ".exs", ".erl", ".f", ".for", ".frag", ".h", ".jar",
              ".js", ".json", ".lisp", ".m", ".md", ".mpg", ".o", ".p", ".pak",
              ".7z", ".zip", ".pem", ".pkl", ".r", ".svg", ".tar", ".ttf", ".x",
              ".xar", ".yaml", ".yml"]
valid_virus_exts = [".py", ".sh", ".c", ".jar", ".js", ".lisp"]


def choose_random_directory(root_directory: Directory) -> Directory:
    """Returns a random directory from whatever depth starting off at the
    specified root directory
    """

    # Choose a sub-directory
    chosen_dir = None
    if randint(1, 100) % 10 != 0:  # This results in an 90% chance that a directory is chosen
        found_dir = False
        for entry in root_directory.get_entries():
            if isinstance(entry, Directory):
                found_dir = True
                break
        if not found_dir:
            return root_directory
        target = choice(root_directory.get_entries())
        while not isinstance(target, Directory):
            target = choice(root_directory.get_entries())
        chosen_dir = choose_random_directory(target)

    # Choose the given directory if none was found or sub-directory was not wanted
    if chosen_dir is None:
        chosen_dir = root_directory
    return chosen_dir


def choose_random_file(root_directory: Directory) -> NormalFile:
    """Returns a random file from whatever depth starting off at the
    specified root directory
    """

    # Choose a sub-directory
    chosen_dir = choose_random_directory(root_directory)
    while True:
        found_file = False
        for entry in chosen_dir.get_entries():
            if not isinstance(entry, VirusFile) and not isinstance(entry, Directory):
                found_file = True
                break
        if found_file:
            break
        chosen_dir = choose_random_directory(chosen_dir)
    target = choice(chosen_dir.get_entries())
    while not isinstance(target, NormalFile) or isinstance(target, VirusFile):
        target = choice(chosen_dir.get_entries())
    return target


def generate_filename(is_virus: bool = False) -> str:
    """Returns a randomly generated filename with a random extension"""
    if is_virus:
        return "".join([choice(valid_chars) for _ in range(randint(5, 20))]) + choice(valid_virus_exts)
    return "".join([choice(valid_chars) for _ in range(randint(5, 20))]) + choice(valid_exts)


def generate_filesystem(username: str) -> Tuple[Directory, int, dict]:
    """Generates the filesystem to be used for a new game and
    returns the root of the system
    """
    root = Directory("root")
    usr = Directory("usr", parent=root)
    user_dir = Directory(username, parent=usr)
    root.add_entry(usr)
    usr.add_entry(user_dir)

    file_count = 0
    for subdir in range(10):
        tmpdir, amt_files = generate_directory(user_dir)
        user_dir.add_entry(tmpdir)
        file_count += amt_files
    virus_files = generate_virus(user_dir, n=file_count // 1000)
    return root, file_count, virus_files


def generate_virus(root_directory: Directory, virus_id: int = -1, n: int = 1) -> Union[str, dict]:
    """Randomly places virus files throughout the system
    starting at the directory specified

    :param root_directory: The directory to start placing the virus files at
    :param virus_id: The number of the virus file to
    :param n: The amount of virus files to place
    """
    filename = generate_filename(True)
    if virus_id != -1:
        virus_file = VirusFile(virus_id, filename, root_directory)
        root_directory.add_entry(virus_file)
        virus_file_2nd_parent = "/".join(str(virus_file).split("/")[:-2])
        return virus_file_2nd_parent

    virus_files = {}
    for virus in range(n):
        target = choose_random_directory(root_directory)
        virus_files[str(virus + 1)] = generate_virus(target, virus + 1)
    return virus_files


def generate_directory(parent: Directory, depth: int = 0) -> Tuple[Directory, int]:
    """Recursively generates a Directory with a maximum depth of 4 Directories deep

    :param parent: The parent Directory that the generated Directory will belong to
    :param depth: The current directory depth to control the maximum depth
    """

    total_files = 0
    dir_name = "".join([choice(valid_chars) for _ in range(randint(5, 20))])
    directory = Directory(dir_name, parent=parent)

    # Generate a random amount of child Directories
    for i in range(randint(2, 5)):
        if depth < 4:
            tmpdir, amt_files = generate_directory(directory, depth + 1)
            total_files += amt_files
            directory.add_entry(tmpdir)

    # Generate a random amount of files
    used_filenames = []
    for i in range(randint(2, 20)):
        total_files += 1
        filename = generate_filename()
        while filename in used_filenames:
            filename = generate_filename()
        used_filenames.append(filename)
        directory.add_entry(NormalFile(filename, directory))

    return directory, total_files
