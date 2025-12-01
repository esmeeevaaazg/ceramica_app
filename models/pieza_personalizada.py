# piezas_personalizadas_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.pieza_personalizada import PiezaPersonalizada

class PersonalizadasFrame(tk.Frame):
    """
    Ventana de gestión de piezas personalizadas.
    Muestra las piezas especiales hechas por pedido del cliente.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF8F0")

        tk.Label(self, text="Piezas Personalizadas", font=("Segoe UI", 18, "bold"),
                 fg="#5B3E31", bg="#FFF8F0").pack(pady=15)

        self.tree = ttk.Treeview(self, columns=("ID", "Pieza ID", "Descripción", "Precio Extra", "Diseño Cliente", "Material Extra"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=20, pady=10, fill="x")

        btn_frame = tk.Frame(self, bg="#FFF8F0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Agregar Personalizada", bg="#FFD9B3", fg="#5B3E31",
                  width=20, command=self.agregar_personalizada).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar Personalizada", bg="#FFCC99", fg="#5B3E31",
                  width=20, command=self.editar_personalizada).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Personalizada", bg="#FFB366", fg="#5B3E31",
                  width=20, command=self.eliminar_personalizada).grid(row=0, column=2, padx=5)

        self.cargar_personalizadas()

    def cargar_personalizadas(self):
        """Carga todas las piezas personalizadas en la tabla"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in PiezaPersonalizada.get_all() if hasattr(PiezaPersonalizada, "get_all") else []:
            self.tree.insert("", "end", values=p)

    def agregar_personalizada(self):
        messagebox.showinfo("Agregar", "Formulario para agregar pieza personalizada.")

    def editar_personalizada(self):
        messagebox.showinfo("Editar", "Editar pieza personalizada seleccionada.")

    def eliminar_personalizada(self):
        messagebox.showinfo("Eliminar", "Eliminar pieza personalizada seleccionada.")
