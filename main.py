from tkinter import Tk, Text, END, BOTH
from model.console import Console


class ConsoleUI(Tk):
    """The ConsoleUI manages all communication between the player and the game
    This only mimics the console and filesystem and does not actually
        use the filesystem of the user's machine
    """

    def __init__(self):
        super().__init__()
        self.title("virus.sh")
        self.configure(background="black")
        self.__console = Console()

        self.__text = Text(self)
        self.__text.insert("end", f"{self.__console.get_prompt()}")
        self.__text.configure(font=("Courier New", 15), bg="black", fg="white",
                              insertbackground="white", insertwidth=4)
        self.__text.pack(expand=True, fill=BOTH)

        self.__text.bind("<Left>", self.on_left_arrow)
        self.__text.bind("<Right>", self.on_right_arrow)
        self.__text.bind("<Return>", self.on_enter)
        self.__text.bind("<BackSpace>", self.on_bs)
        self.__text.bind("<KeyPress>", self.on_key_press)
        self.__text.bind("<Tab>", self.on_tab)

        self.__current_line = ""
        self.__current_index = 0

    def on_left_arrow(self, _):
        if self.__current_index > 0:
            self.__current_index -= 1
            if self.__current_index < 0:
                self.__current_index = 0
                return "break"
        else:
            return "break"

    def on_right_arrow(self, _):
        if self.__current_index <= len(self.__current_line):
            self.__current_index += 1
        else:
            return "break"

    def on_tab(self, _):
        """Whenever the tab key is pressed, try auto-completing the text"""

        # Try splitting the current line by spaces in order to get the current
        # line and split the possible directory by using the "/" as a separator
        line_split = self.__current_line.split(" ")
        no_spaces = len(line_split) == 1
        if no_spaces:
            dir_line_split = self.__current_line.split("/")
        else:
            dir_line_split = line_split[-1].split("/")

        # Iterate through the entries in the most recent directory to try to auto complete it
        if len(dir_line_split) == 1:
            current_dir = self.__console.get_current_dir()
        else:
            current_dir = self.__console.get_current_dir().get_entry(dir_line_split[-2])

        # If the directory exists, try finding the entry that matches the last result
        if current_dir and dir_line_split[-1]:
            for entry in current_dir.get_entries():
                if entry.get_name().startswith(dir_line_split[-1]):

                    # Find the text that needs to be appended by only adding the
                    #   text that is left in the found entry
                    # Update the last index of the dir_line_split, join it together using "/"
                    #   and replace the current line with the updated string
                    appended_text = entry.get_name()[len(dir_line_split[-1]):]
                    dir_line_split[-1] = entry.get_name()
                    line_split[-1] = "/".join(dir_line_split)
                    if no_spaces:
                        self.__current_line = "/".join(line_split)
                    else:
                        self.__current_line = " ".join(line_split)
                    self.__current_index = len(self.__current_line)
                    self.__text.insert("end", appended_text)
        return "break"

    def on_key_press(self, event):
        """Whenever a keyboard key is pressed"""
        if len(self.__current_line) != self.__current_index:
            line_list = list(self.__current_line)
            line_list.insert(self.__current_index, event.char)
            self.__current_line = "".join(line_list)
        else:
            self.__current_line += event.char
        self.__current_index += 1

    def on_enter(self, _):
        """Whenever the enter/return key is pressed"""
        result = self.__console.parse(self.__current_line)
        cleared = result == "@clear"
        prompted = False
        if result:
            if result == "@clear":
                self.__text.delete(1.0, "end")
            elif result == "@main_menu":
                self.__console.main_menu()
                self.__text.delete(1.0, "end")
                cleared = True
            elif result == "@exit":
                exit(0)
            else:
                if result.startswith("@prompt:"):
                    result = result[len("@prompt:"):]
                    prompted = True
                self.__text.insert("end", f"\n{result}")
        if not cleared:
            self.__text.insert("end", "\n")
        if not prompted:
            self.__text.insert("end", f"{self.__console.get_prompt()}")
        self.__current_line = ""
        self.__current_index = 0
        self.__text.see(END)
        self.__text.mark_set("insert", END)
        return "break"

    def on_bs(self, _):
        """Whenever the backspace key is pressed"""
        if self.__current_index > 0 and len(self.__current_line) > 0:
            self.__current_index -= 1
            if self.__current_index == len(self.__current_line):
                self.__current_line = self.__current_line[:-1]
            else:
                i = self.__current_index
                self.__current_line = self.__current_line[:i] + self.__current_line[i + 1:]
            self.__text.delete("insert -1 chars", "insert")
        return "break"


if __name__ == "__main__":
    root = ConsoleUI()
    root.mainloop()
