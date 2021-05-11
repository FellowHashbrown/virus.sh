from model import Entry, Directory, NormalFile, VirusFile
from model.abstract import Listable


def ls(directory: Listable, show_hidden: bool = False):
    """Mimics the ls command to list the contents of a Directory

    :param directory: The Directory object to list the contents of
    :param show_hidden: Whether or not to show hidden files
    """
    return directory.list_contents(show_hidden)


def cd(target: Directory):
    pass


def rm(entry: Entry):
    pass


def trace(file: NormalFile):
    pass


def chunks():
    pass


def mntr():
    pass


def track(virus_file: VirusFile, number: int):
    pass
