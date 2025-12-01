# pedidos_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.pedido import Pedido

class PedidosFrame(tk.Frame):
    """
    Ventana de gestión de pedidos.
    Lista todos los pedidos y permite actualizar estado o eliminar.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF8F0")

        tk.Label(self, text="Pedidos", font=("Segoe UI", 18, "bold"),
                 fg="#5B3E31", bg="#FFF8F0").pack(pady=15)

        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Estado", "Fecha Creación"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=20, pady=10, fill="x")

        btn_frame = tk.Frame(self, bg="#FFF8F0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Actualizar Estado", bg="#FFD9B3", fg="#5B3E31",
                  width=20, command=self.actualizar_estado).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Eliminar Pedido", bg="#FFB366", fg="#5B3E31",
                  width=20, command=self.eliminar_pedido).grid(row=0, column=1, padx=5)

        self.cargar_pedidos()

    def cargar_pedidos(self):
        """Carga todos los pedidos en la tabla"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in Pedido.get_all():
            self.tree.insert("", "end", values=p)

    def actualizar_estado(self):
        messagebox.showinfo("Actualizar", "Formulario para actualizar estado del pedido.")

    def eliminar_pedido(self):
        messagebox.showinfo("Eliminar", "Eliminar pedido seleccionado.")
