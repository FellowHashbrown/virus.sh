from tkinter import Tk, Text, END
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
        self.__text.configure(font=("Courier New", 15), bg="black", fg="white")
        self.__text.pack()

        self.__text.bind("<Return>", self.on_enter)
        self.__text.bind("<BackSpace>", self.on_bs)
        self.__text.bind("<KeyPress>", self.on_key_press)

        self.__current_line = ""

    def on_key_press(self, event):
        """Whenever a keyboard key is pressed"""
        self.__current_line += event.char

    def on_enter(self, _):
        """Whenever the enter/return key is pressed"""
        result = self.__console.parse(self.__current_line)
        cleared = result == "@clear"
        prompted = False
        if result:
            if result == "@clear":
                self.__text.delete(1.0, "end")
            elif result == "@exit":
                self.__text.insert("end", "\nbye!")
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
        self.__text.see(END)
        return "break"

    def on_bs(self, _):
        """Whenever the backspace key is pressed"""
        if len(self.__current_line) > 0:
            self.__current_line = self.__current_line[:-1]
            self.__text.delete("insert -1 chars", "insert")
        return "break"


if __name__ == "__main__":
    root = ConsoleUI()
    root.mainloop()
