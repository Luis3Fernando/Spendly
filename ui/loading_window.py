import tkinter as tk
from tkinter import messagebox
from config.db import get_db
from ui.main_window import MainWindow


class LoadingWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cargando...")
        self.geometry("300x100")
        self.configure(bg="#1e1e1e")

        label = tk.Label(
            self, text="🔄 Conectando con la base de datos...", fg="white", bg="#1e1e1e"
        )
        label.pack(pady=30)

        self.after(100, self.connect_to_db)

    def connect_to_db(self):
        try:
            db = get_db()

            db.list_collection_names()
            messagebox.showinfo("Éxito", "Conexión con MongoDB exitosa.")
            self.destroy()
            main_app = MainWindow()
            main_app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar con MongoDB:\n\n{e}")
            self.destroy()
