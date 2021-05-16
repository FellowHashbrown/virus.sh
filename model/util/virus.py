from random import randint
from threading import Thread
from time import sleep

from model.util import Save, choose_random_file


class Virus(Thread):
    """The Virus Thread works separately from the main game thread
    and deletes a file at the speed of which the game holds

    :param save: The Save object that the Virus is working on
    :param callback: The function that will be called if the Virus successfully
        deletes all files on the system
    """

    def __init__(self, save: Save, callback: callable):
        super().__init__(target=self.run)
        self.__save = save
        self.__is_alive = True
        self.__callback = callback
        self.start()

    def delete_file(self):
        """Deletes a random file from the filesystem and adds it to the deletion log
        which is used in the mntr command
        """
        target_file = choose_random_file(self.__save.get_root())
        file_log = str(target_file)
        parent_dir = target_file.get_parent()
        parent_dir.remove_entry(target_file)
        target_file.set_parent(self.__save.get_trash())
        virus_id = randint(1, self.__save.get_virus_files()[1])
        self.__save.log_deletion(virus_id, file_log)

    def stop(self):
        """Sets the Thread as being dead"""
        self.__is_alive = False

    def run(self):
        """This function is what is executed when the Virus deletes a file
        but only while there are still normal files on the system
        """
        while self.__save.get_normal_files()[0] < self.__save.get_normal_files()[1]:
            self.delete_file()
            for _ in range(self.__save.get_speed()):
                if self.__is_alive:
                    sleep(1)
                    continue
                return
        self.__callback()
