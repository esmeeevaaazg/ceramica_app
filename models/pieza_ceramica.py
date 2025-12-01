# piezas_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.pieza_ceramica import PiezaCeramica

class PiezasFrame(tk.Frame):
    """
    Ventana de gestión de piezas de cerámica.
    Lista piezas existentes y permite agregar, editar y eliminar.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF8F0")

        tk.Label(self, text="Piezas", font=("Segoe UI", 18, "bold"),
                 fg="#5B3E31", bg="#FFF8F0").pack(pady=15)

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Descripción", "Precio", "Tipo", "Material"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=20, pady=10, fill="x")

        btn_frame = tk.Frame(self, bg="#FFF8F0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Agregar Pieza", bg="#FFD9B3", fg="#5B3E31",
                  width=15, command=self.agregar_pieza).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar Pieza", bg="#FFCC99", fg="#5B3E31",
                  width=15, command=self.editar_pieza).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Pieza", bg="#FFB366", fg="#5B3E31",
                  width=15, command=self.eliminar_pieza).grid(row=0, column=2, padx=5)

        self.cargar_piezas()

    def cargar_piezas(self):
        """Carga todas las piezas en la tabla"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in PiezaCeramica.get_all():
            self.tree.insert("", "end", values=p)

    def agregar_pieza(self):
        messagebox.showinfo("Agregar", "Formulario para agregar nueva pieza.")

    def editar_pieza(self):
        messagebox.showinfo("Editar", "Editar pieza seleccionada.")

    def eliminar_pieza(self):
        messagebox.showinfo("Eliminar", "Eliminar pieza seleccionada.")
