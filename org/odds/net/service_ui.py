import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class ServiceWindow:
    def __init__(self, title: str = 'service window', w: int = 640, h: int = 480):
        self.win = tk.Tk()
        self.win.title(title)
        self.w = w
        self.h = h
        self.x_pos = int((self.win.winfo_screenwidth() / 2) - (self.w / 2))
        self.y_pos = int((self.win.winfo_screenheight() / 2) - (self.h / 2))
        self.win.minsize(self.w, self.h)
        self.win.geometry(f"{self.w}x{self.h}+{self.x_pos}+{self.y_pos}")
        self.win.protocol('WM_DELETE_WINDOW', self.on_close)
        self.service = TheService(logs_callback=self.log)

        self.mainframe = None
        self.logging_area = None

        self.build_ui()

    def build_ui(self):
        self.mainframe = tk.Frame(self.win)
        self.mainframe.pack(padx=10, pady=10)

        self.logging_area = ScrolledText(self.mainframe, wrap=tk.WORD, bg='black', fg='lightgreen', state=tk.DISABLED)
        self.logging_area.grid(row=0, column=0)
        self.logging_area.yview(tk.END)
        self.log('welcome')

    def log(self, s: str):
        print(s)
        self.logging_area.config(state=tk.NORMAL)
        self.logging_area.insert(tk.END, 'welcome!')
        self.logging_area.yview(tk.END)
        self.logging_area.config(state=tk.DISABLED)

    def open(self):
        self.win.mainloop()

    def on_close(self):
        self.win.destroy()
        sys.exit(0)


def main():
    win = ServiceWindow()
    win.open()


if __name__ == "__main__":
    main()
