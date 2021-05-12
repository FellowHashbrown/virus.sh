from random import choice, randint
from typing import Tuple

from model import Directory, NormalFile, VirusFile

valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-"
valid_exts = [".py", ".sh", ".png", ".jpeg", ".jpg", ".ico", ".c", ".dat", ".db",
              ".dbf", ".es6", ".exs", ".erl", ".f", ".for", ".frag", ".h", ".jar",
              ".js", ".json", ".lisp", ".m", ".md", ".mpg", ".o", ".p", ".pak",
              ".7z", ".zip", ".pem", ".pkl", ".r", ".svg", ".tar", ".ttf", ".x",
              ".xar", ".yaml", ".yml"]
valid_virus_exts = [".py", ".sh", ".c", ".jar", ".js", ".lisp"]


def generate_filename() -> str:
    """Returns a randomly generated filename with a random extension"""
    return "".join([choice(valid_chars) for _ in range(randint(5, 20))]) + choice(valid_exts)


def generate_filesystem(username: str) -> Tuple[Directory, int]:
    """Generates the filesystem to be used for a new game and
    returns the root of the system
    """
    root = Directory("root")
    usr = Directory("usr")
    user_dir = Directory(username)
    root.add_entry(usr)
    usr.add_entry(user_dir)

    file_count = 0
    for subdir in range(10):
        tmpdir, amt_files = generate_directory(user_dir)
        root.add_entry(tmpdir)
        file_count += amt_files
    return root, file_count


def generate_virus(root_directory: Directory, n: int = 1):
    """Randomly places virus files throughout the system
    starting at the directory specified

    :param root_directory: The directory to start placing the virus files at
    :param n: The amount of virus files to place
    """
    for virus in range(n):
        choose_dir = randint(1, 100) % 2 == 0
        filename = generate_filename()
        if choose_dir:  # Choose a directory to move into to place the file
            target = choice(root_directory.get_entries())
            while not isinstance(target, Directory):
                target= choice(root_directory.get_entries())
            # noinspection PyTypeChecker
            generate_virus(target)  # Recursively call this but only place 1
        else:  # Place the file in the current directory
            root_directory.add_entry(VirusFile(virus + 1, filename, root_directory))


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
