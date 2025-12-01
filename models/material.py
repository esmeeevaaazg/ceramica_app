# materiales_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.material import Material

class MaterialesFrame(tk.Frame):
    """
    Ventana de gestión de materiales.
    Permite listar, agregar, editar y eliminar materiales.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF8F0")

        tk.Label(self, text="Materiales", font=("Segoe UI", 18, "bold"),
                 fg="#5B3E31", bg="#FFF8F0").pack(pady=15)

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Proveedor", "Costo Unitario"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=20, pady=10, fill="x")

        btn_frame = tk.Frame(self, bg="#FFF8F0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Agregar Material", bg="#FFD9B3", fg="#5B3E31",
                  width=15, command=self.agregar_material).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar Material", bg="#FFCC99", fg="#5B3E31",
                  width=15, command=self.editar_material).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Material", bg="#FFB366", fg="#5B3E31",
                  width=15, command=self.eliminar_material).grid(row=0, column=2, padx=5)

        self.cargar_materiales()

    def cargar_materiales(self):
        """Carga todos los materiales en la tabla"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for m in Material.get_all():
            self.tree.insert("", "end", values=(m[0], m[1], m[2], m[3]))

    def agregar_material(self):
        messagebox.showinfo("Agregar", "Formulario para agregar material.")

    def editar_material(self):
        messagebox.showinfo("Editar", "Editar material seleccionado.")

    def eliminar_material(self):
        messagebox.showinfo("Eliminar", "Eliminar material seleccionado.")
