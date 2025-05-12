import os
import tkinter as tk
import subprocess
import platform
from tkinter import ttk, messagebox
from ui.base_window import BaseWindow
from utils.data_validation import is_number
from services.mongo_service import CompraService
from utils.calculator import get_total, get_total_max, get_total_min
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class MainWindow(BaseWindow):
    def setup_ui(self):
        self.service = CompraService()
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

        self.btn_agregar = tk.Button(self, text="➕ Agregar a la lista", bg="#3500AD", fg="white", command=self.add_item, activebackground="#9B70FF", relief="flat")
        self.btn_agregar.pack(pady=10)

        columns = ("Producto", "Precio Mín", "Precio Máx")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(pady=10)
        
        action_frame = tk.Frame(self, bg=self["bg"])
        action_frame.pack(pady=5)

        self.btn_editar = tk.Button(
            action_frame, text="✏️ Editar seleccionado", bg="#FFA500", fg="black",
            activebackground="#FFCC80", relief="flat",
            command=lambda: self.editar_item(self.obtener_id_seleccionado())
        )
        self.btn_editar.grid(row=0, column=0, padx=10)

        self.btn_eliminar = tk.Button(
            action_frame, text="🗑 Eliminar seleccionado", bg="#FF4C4C", fg="white",
            activebackground="#FF8080", relief="flat",
            command=lambda: self.eliminar_item(self.obtener_id_seleccionado())
        )
        self.btn_eliminar.grid(row=0, column=1, padx=10)


        resumen_frame = tk.Frame(self, bg=self["bg"])
        resumen_frame.pack(pady=10)

        self.label_total_estimado = tk.Label(resumen_frame, text="💰 Total promedio: $0.00", fg="white", bg=self["bg"], font=("Arial", 10))
        self.label_total_estimado.grid(row=0, column=0, padx=15)

        self.label_total_min = tk.Label(resumen_frame, text="🟢 Total mínimo: $0.00", fg="white", bg=self["bg"], font=("Arial", 10))
        self.label_total_min.grid(row=0, column=1, padx=15)

        self.label_total_max = tk.Label(resumen_frame, text="🔴 Total máximo: $0.00", fg="white", bg=self["bg"], font=("Arial", 10))
        self.label_total_max.grid(row=0, column=2, padx=15)
        
        export_frame = tk.Frame(self, bg=self["bg"])
        export_frame.pack(pady=5)

        self.btn_exportar_pdf = tk.Button(
            export_frame, text="📄 Exportar PDF", bg="#444", fg="white", activebackground="#666", relief="flat",command=self.exportar_a_pdf
        )
        self.btn_exportar_pdf.grid(row=0, column=0, padx=10)

        self.btn_exportar_txt = tk.Button(
            export_frame, text="📝 Exportar TXT", bg="#444", fg="white", activebackground="#666", relief="flat", command=self.exportar_a_txt
        )
        self.btn_exportar_txt.grid(row=0, column=1, padx=10)
        
        self.btn_ver_exportados = tk.Button(
            export_frame, text="📂 Ver archivo", bg="#444", fg="white", activebackground="#666", relief="flat", command=self.abrir_carpeta
        )
        self.btn_ver_exportados.grid(row=0, column=2, padx=10)
    
        self.cargar_compras()

        
    def add_item(self):
        producto = self.entry_producto.get()
        precio_min = self.entry_precio_min.get()
        precio_max = self.entry_precio_max.get()

    
        if not is_number(precio_min) or not is_number(precio_max):
            try:
                precio_min = float(precio_min)
                precio_max = float(precio_max)
            except ValueError:
                messagebox.showinfo("Error", "Los precios deben ser números")
                return

        if producto and precio_min and precio_max:
            try:
                item = {
                "producto": producto,
                "precio_min": float(precio_min),
                "precio_max": float(precio_max)
                }   
                self.service.insertar_compra(item)

                self.entry_producto.delete(0, tk.END)
                self.entry_precio_min.delete(0, tk.END)
                self.entry_precio_max.delete(0, tk.END)

                self.cargar_compras()
                self.calculator()
            except ValueError:
                messagebox.showinfo("Error", "Formato de precio inválido")

    def cargar_compras(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        compras = self.service.obtener_compras()
    
        for compra in compras:
            self.tree.insert(
            "", "end", 
            values=(compra["producto"], compra["precio_min"], compra["precio_max"])
        )
            
        self.calculator()

    def obtener_id_seleccionado(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            producto = item["values"][0]
            return self.service.obtener_id_por_producto(producto)
        return None

    def eliminar_item(self, id_seleccionado):
        if id_seleccionado:
            confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este elemento?")
            if confirmacion:
                self.service.eliminar_compra(id_seleccionado)
                self.cargar_compras()
            
            self.calculator()
            
        else:
            messagebox.showinfo("Error", "No se ha seleccionado ningún elemento")

    def editar_item(self, item_id):
        if item_id is None:
            messagebox.showinfo("Error", "Selecciona un producto primero")
            return

        compra = self.service.obtener_compra_por_id(item_id) 

        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.title("Editar compra")
        ventana_edicion.configure(bg="#1e1e1e")
        ventana_edicion.geometry("350x200")

        tk.Label(ventana_edicion, text="Producto", fg="white", bg="#1e1e1e").pack(pady=5)
        entry_producto = tk.Entry(ventana_edicion, bg="#2a2a2a", fg="white")
        entry_producto.insert(0, compra["producto"])
        entry_producto.pack()

        tk.Label(ventana_edicion, text="Precio mínimo", fg="white", bg="#1e1e1e").pack(pady=5)
        entry_min = tk.Entry(ventana_edicion, bg="#2a2a2a", fg="white")
        entry_min.insert(0, compra["precio_min"])
        entry_min.pack()

        tk.Label(ventana_edicion, text="Precio máximo", fg="white", bg="#1e1e1e").pack(pady=5)
        entry_max = tk.Entry(ventana_edicion, bg="#2a2a2a", fg="white")
        entry_max.insert(0, compra["precio_max"])
        entry_max.pack()

        def guardar_cambios():
            nuevo_producto = entry_producto.get()
            nuevo_min = entry_min.get()
            nuevo_max = entry_max.get()
            
            if not is_number(nuevo_min) or not is_number(nuevo_max):
                try:
                    nuevo_min = float(nuevo_min)
                    nuevo_max = float(nuevo_max)
                except ValueError:
                    messagebox.showinfo("Error", "Los precios deben ser números")
                    return

            producto ={
                "producto": nuevo_producto,
                "precio_min": float(nuevo_min),
                "precio_max": float(nuevo_max)
            }
            
            self.service.actualizar_compra(item_id, producto)
            ventana_edicion.destroy()
            self.cargar_compras()

        tk.Button(ventana_edicion, text="Guardar cambios", command=guardar_cambios, bg="#4CAF50", fg="white").pack(pady=10)
        self.calculator()
        
    def calculator(self):
        compras = self.service.obtener_compras()
        
        total_average = get_total(compras)
        total_min_average = get_total_min(compras)
        total_max_average = get_total_max(compras)
        
        self.label_total_estimado.config(text=f"💰 Total promedio: ${total_average}")
        self.label_total_min.config(text=f"🟢 Total mínimo: ${total_min_average}")
        self.label_total_max.config(text=f"🔴 Total máximo: ${total_max_average}")
    
    def exportar_a_txt(self):
        ruta = "exportaciones"
        os.makedirs(ruta, exist_ok=True)
        archivo = os.path.join(ruta, "compras.txt")

        with open(archivo, "w", encoding="utf-8") as f:
                f.write("Listado de Compras Pendientes\n")
                f.write("=" * 30 + "\n\n")
                for item in self.tree.get_children():
                    valores = self.tree.item(item)["values"]
                    f.write(f"Producto: {valores[0]} - Precio Mín: {valores[1]} - Precio Máx: {valores[2]}\n")

                compras = self.service.obtener_compras()
                total_avg = get_total(compras)
                total_min = get_total_min(compras)
                total_max = get_total_max(compras)

                f.write("\n" + "=" * 30 + "\n")
                f.write(f"💰 Total promedio: ${total_avg}\n")
                f.write(f"🟢 Total mínimo: ${total_min}\n")
                f.write(f"🔴 Total máximo: ${total_max}\n")

        messagebox.showinfo("Éxito", f"Exportado a {archivo}")
  
    def exportar_a_pdf(self):
        ruta = "exportaciones"
        os.makedirs(ruta, exist_ok=True)
        archivo = os.path.join(ruta, "compras.pdf")

        c = canvas.Canvas(archivo, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(50, 750, "Listado de Compras Pendientes")
        
        y = 720
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            linea = f"{valores[0]} - Min: ${valores[1]} - Max: ${valores[2]}"
            c.drawString(50, y, linea)
            y -= 20
            if y < 50:
                c.showPage()
                y = 750

        compras = self.service.obtener_compras()
        total_avg = get_total(compras)
        total_min = get_total_min(compras)
        total_max = get_total_max(compras)

        if y < 100:
            c.showPage()
            y = 750

        y -= 30
        c.drawString(50, y, f"💰 Total promedio: ${total_avg}")
        y -= 20
        c.drawString(50, y, f"🟢 Total mínimo: ${total_min}")
        y -= 20
        c.drawString(50, y, f"🔴 Total máximo: ${total_max}")

        c.save()
        messagebox.showinfo("Éxito", f"Exportado a {archivo}")
        
    def abrir_carpeta(self):
        ruta = os.path.abspath("exportaciones")
        if platform.system() == "Windows":
            os.startfile(ruta)
        elif platform.system() == "Darwin":
            subprocess.call(["open", ruta])
        else:
            subprocess.call(["xdg-open", ruta])