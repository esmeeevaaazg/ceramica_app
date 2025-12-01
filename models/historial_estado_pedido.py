# historial_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.historial_estado_pedido import PedidoEstadoHistorial

class HistorialFrame(tk.Frame):
    """
    Ventana que muestra el historial de estados de un pedido.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF8F0")

        tk.Label(self, text="Historial de Pedidos", font=("Segoe UI", 18, "bold"),
                 fg="#5B3E31", bg="#FFF8F0").pack(pady=15)

        self.tree = ttk.Treeview(self, columns=("Estado", "Fecha"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=20, pady=10, fill="x")

        btn_frame = tk.Frame(self, bg="#FFF8F0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Actualizar Historial", bg="#FFD9B3", fg="#5B3E31",
                  width=20, command=self.actualizar_historial).pack()

        self.cargar_historial()

    def cargar_historial(self):
        """Carga historial de pedidos (placeholder, por defecto vacío)"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Aquí se puede cargar historial real de un pedido
        historial = PedidoEstadoHistorial.get_by_pedido(1) if hasattr(PedidoEstadoHistorial, "get_by_pedido") else []
        for h in historial:
            self.tree.insert("", "end", values=h)

    def actualizar_historial(self):
        messagebox.showinfo("Actualizar", "Actualizar historial de estados del pedido.")
