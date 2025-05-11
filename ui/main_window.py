import tkinter as tk
from tkinter import ttk
from ui.base_window import BaseWindow

class MainWindow(BaseWindow):
    def setup_ui(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", 
            background="#1e1e1e",
            foreground="white",
            rowheight=25,
            fieldbackground="#1e1e1e")
        self.style.map('Treeview', background=[('selected', '#2d89ef')])

        title = tk.Label(self, text="Spendly", font=("Arial", 18, "bold"), fg="white", bg=self["bg"])
        title.pack(pady=3)

        subtitle = tk.Label(self, text="Listado de compras pendientes", font=("Arial", 12), fg="white", bg=self["bg"])
        subtitle.pack(pady=10)

        form_frame = tk.Frame(self, bg=self["bg"])
        form_frame.pack(pady=5)

        self.entry_producto = tk.Entry(form_frame, width=40, bg="#2a2a2a", fg="white", insertbackground="white")
        self.entry_producto.grid(row=0, column=0, padx=5)
        self.entry_producto.insert(0, "Producto")

        self.entry_precio_min = tk.Entry(form_frame, width=15, bg="#2a2a2a", fg="white", insertbackground="white")
        self.entry_precio_min.grid(row=0, column=1, padx=5)
        self.entry_precio_min.insert(0, "Min $")

        self.entry_precio_max = tk.Entry(form_frame, width=15, bg="#2a2a2a", fg="white", insertbackground="white")
        self.entry_precio_max.grid(row=0, column=2, padx=5)
        self.entry_precio_max.insert(0, "Max $")

        self.btn_agregar = tk.Button(self, text="➕ Agregar a la lista", bg="#3500AD", fg="white", activebackground="#9B70FF", relief="flat")
        self.btn_agregar.pack(pady=10)

        columns = ("Producto", "Precio Mín", "Precio Máx")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(pady=10)

        resumen_frame = tk.Frame(self, bg=self["bg"])
        resumen_frame.pack(pady=10)

        self.label_total_estimado = tk.Label(resumen_frame, text="💰 Estimado promedio: $0.00", fg="white", bg=self["bg"], font=("Arial", 10))
        self.label_total_estimado.grid(row=0, column=0, padx=15)

        self.label_total_min = tk.Label(resumen_frame, text="🟢 Total mínimo: $0.00", fg="white", bg=self["bg"], font=("Arial", 10))
        self.label_total_min.grid(row=0, column=1, padx=15)

        self.label_total_max = tk.Label(resumen_frame, text="🔴 Total máximo: $0.00", fg="white", bg=self["bg"], font=("Arial", 10))
        self.label_total_max.grid(row=0, column=2, padx=15)
        
        export_frame = tk.Frame(self, bg=self["bg"])
        export_frame.pack(pady=5)

        self.btn_exportar_pdf = tk.Button(
            export_frame, text="📄 Exportar PDF", bg="#444", fg="white", activebackground="#666", relief="flat"
        )
        self.btn_exportar_pdf.grid(row=0, column=0, padx=10)

        self.btn_exportar_txt = tk.Button(
            export_frame, text="📝 Exportar TXT", bg="#444", fg="white", activebackground="#666", relief="flat"
        )
        self.btn_exportar_txt.grid(row=0, column=1, padx=10)
        
        self.btn_ver_exportados = tk.Button(
            export_frame, text="📂 Ver archivo", bg="#444", fg="white", activebackground="#666", relief="flat"
        )
        self.btn_ver_exportados.grid(row=0, column=2, padx=10)

