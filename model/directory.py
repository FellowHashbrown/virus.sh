from typing import List, Union

from .entry import Entry


class Directory(Entry):

    def __init__(self, name: str, entries: List[Entry] = None):
        super().__init__(name)
        if entries is None:
            entries = []
        self.__entries = entries

    def __str__(self):
        pass

    def is_populated(self):
        return len(self.__entries) > 0

    def add_entry(self, entry: Entry):
        if entry not in self.__entries:
            self.__entries.append(entry)
            # self.__entries.sort()

    def remove_entry(self, entry: Union[int, str, Entry]) -> bool:
        if isinstance(entry, Entry):
            target = entry
        elif isinstance(entry, int):
            target = self.__entries[entry]
        else:
            target = None
            for e in self.__entries:
                if e.get_name() == entry:
                    target = e
        if isinstance(target, Directory) and target.is_populated():
            return False
        self.__entries.remove(target)
        return True
