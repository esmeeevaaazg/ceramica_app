# inventario_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.inventario import Inventario

class InventarioFrame(tk.Frame):
    """
    Ventana de gestión de inventario.
    Lista todos los materiales y sus stocks, permite actualizar stock mínimo y actual.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF8F0")

        tk.Label(self, text="Inventario", font=("Segoe UI", 18, "bold"),
                 fg="#5B3E31", bg="#FFF8F0").pack(pady=15)

        self.tree = ttk.Treeview(self, columns=("ID", "Material", "Stock Actual", "Stock Mínimo"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=20, pady=10, fill="x")

        btn_frame = tk.Frame(self, bg="#FFF8F0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Actualizar Stock", bg="#FFD9B3", fg="#5B3E31",
                  width=20, command=self.actualizar_stock).grid(row=0, column=0, padx=5)

        self.cargar_inventario()

    def cargar_inventario(self):
        """Carga todos los registros de inventario en la tabla"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for inv in Inventario.get_all():
            self.tree.insert("", "end", values=inv)

    def actualizar_stock(self):
        messagebox.showinfo("Actualizar", "Formulario para actualizar stock del inventario.")
