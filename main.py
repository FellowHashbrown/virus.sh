from tkinter import Tk, Text, END
from model.console import Console


class ConsoleUI(Tk):

    def __init__(self):
        super().__init__()
        self.title("virus.sh")
        self.configure(background="black")
        self.__console = Console()

        self.__text = Text(self)
        self.__text.insert("end", f"{self.__console.get_prompt(False)}")
        self.__text.configure(font=("Courier New", 15), bg="black", fg="white")
        self.__text.pack()

        self.__text.bind("<Return>", self.on_enter)
        self.__text.bind("<BackSpace>", self.on_bs)
        self.__text.bind("<KeyPress>", self.on_key_press)

        self.__current_line = ""

    def on_key_press(self, event):
        self.__current_line += event.char

    def on_enter(self, _):
        result = self.__console.parse(self.__current_line)
        cleared = result == "@clear"
        if result:
            if result == "@clear":
                self.__text.delete(1.0, "end")
            else:
                self.__text.insert("end", f"\n{result}")
        if not cleared:
            self.__text.insert("end", "\n")
        self.__text.insert("end", f"{self.__console.get_prompt(False)}")
        self.__current_line = ""
        self.__text.see(END)
        return "break"

    def on_bs(self, _):
        if len(self.__current_line) > 0:
            self.__current_line = self.__current_line[:-1]
            self.__text.delete("insert -1 chars", "insert")
        return "break"


if __name__ == "__main__":
    root = ConsoleUI()
    root.mainloop()
