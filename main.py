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
        self.__text.focus_set()

        self.__text.bind("<Left>", self.on_left_arrow)
        self.__text.bind("<Right>", self.on_right_arrow)
        self.__text.bind("<Up>", self.on_up_arrow)
        self.__text.bind("<Down>", self.on_down_arrow)

        self.__text.bind("<Return>", self.on_enter)
        self.__text.bind("<BackSpace>", self.on_bs)
        self.__text.bind("<KeyPress>", self.on_key_press)
        self.__text.bind("<Tab>", self.on_tab)

        self.__text.bind("<Button>", lambda _: "break")

        self.__current_line = ""
        self.__current_index = 0

        self.__prev_commands = []
        self.__prev_index = -1

        self.__virus = None

    def on_up_arrow(self, _):
        """This overrides the up arrow key bind to mimic
        loading previous commands run in the console
        """
        if self.__prev_index < len(self.__prev_commands) - 1:
            self.__prev_index += 1
        self.__text.mark_set("insert", END)
        self.__text.delete(f"insert -{len(self.__current_line)} chars", "insert")
        self.__current_line = self.__prev_commands[self.__prev_index]
        self.__current_index = len(self.__current_line)
        self.__text.insert("end", self.__current_line)
        return "break"

    def on_down_arrow(self, _):
        """This overrides the down arrow key bind to mimic
        loading previous commands run in the console
        """
        if self.__prev_index >= 0:
            self.__prev_index -= 1
        self.__text.delete(f"insert -{self.__current_index} chars", "insert")
        if self.__prev_index == -1:
            self.__current_line = ""
        else:
            self.__current_line = self.__prev_commands[self.__prev_index]
        self.__current_index = len(self.__current_line)
        self.__text.insert("end", self.__current_line)
        return "break"

    def on_left_arrow(self, _):
        """This overrides the left arrow key bind to move the insert
        cursor left until the beginning of the current prompt
        """
        if self.__current_index > 0:
            self.__current_index -= 1
            if self.__current_index < 0:
                self.__current_index = 0
                return "break"
        else:
            return "break"

    def on_right_arrow(self, _):
        """This overrides the right arrow key bind to move the insert
        cursor right until the end of the text
        """
        if self.__current_index <= len(self.__current_line):
            self.__current_index += 1
        else:
            return "break"

    def on_tab(self, _):
        """This overrides the tab key bind to try to
        auto-complete any directory entries
        """

        # Try splitting the current line by spaces in order to get the current
        # line and split the possible directory by using the "/" as a separator
        line_split = self.__current_line.split(" ")
        no_spaces = len(line_split) == 1
        if no_spaces:
            dir_line_split = self.__current_line.split("/")
        else:
            dir_line_split = line_split[-1].split("/")

        # Iterate through the entries in the most recent directory to try to auto complete it
        current_dir = self.__console.get_current_dir()
        if len(dir_line_split) > 1:
            for entry in dir_line_split[:-1]:
                if entry == "..":
                    if current_dir.get_parent():
                        current_dir = current_dir.get_parent()
                elif entry != ".":
                    current_dir = current_dir.get_entry(entry)

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
        """This overrides the keypress event to insert text inside the current line properly
        whether the cursor is at the beginning of the current line or the end
        """
        if len(self.__current_line) != self.__current_index:
            line_list = list(self.__current_line)
            line_list.insert(self.__current_index, event.char)
            self.__current_line = "".join(line_list)
        else:
            self.__current_line += event.char
        self.__current_index += 1

    def on_enter(self, _):
        """This overrides the return key bind event to try calling the command
        given and adds the command to the list of previous commands
        """
        result = self.__console.parse(self.__current_line)
        self.__prev_commands.insert(0, self.__current_line)
        self.__prev_index = -1
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
            elif result == "@game_over":
                self.__text.insert("end", "\nFilesystem error: Empty system: Virus has erased all files (You Lost.)")
                self.__console.main_menu()
            elif result == "@won":
                self.__text.insert("end", "\nFilesystem message: Virus eradicated: You have won!")
                self.__console.main_menu()
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
        """This overrides the backspace key bind event to deal with backspacing the current line
        only until the beginning of the prompt is reached.
        If the text cursor is set in the middle of the line, only remove that part from the current line
        that precedes the cursor.
        """
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
