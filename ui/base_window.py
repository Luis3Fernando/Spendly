import tkinter as tk

class BaseWindow(tk.Tk):
    def __init__(self, title="Spendly", size="600x600"):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.configure(bg="#121212")
        self.resizable(False, False)

        self.setup_ui()
