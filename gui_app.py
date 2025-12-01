# gui_app.py
import tkinter as tk
from tkinter import messagebox

# Importar ventanas de módulos claras
from login_window import LoginWindow
from usuarios_frame import UsuariosFrame
from materiales_frame import MaterialesFrame
from inventario_frame import InventarioFrame
from piezas_frame import PiezasFrame
from piezas_personalizadas_frame import PersonalizadasFrame
from pedidos_frame import PedidosFrame
from historial_frame import HistorialFrame

# ---------- DASHBOARD ESTILO TARJETAS ----------
class Dashboard(tk.Frame):
    """
    Dashboard principal de la app.
    Muestra tarjetas de acceso rápido a cada módulo.
    """
    def __init__(self, parent, usuario, on_module_select):
        super().__init__(parent, bg="#FFF8F0")
        self.usuario = usuario
        self.on_module_select = on_module_select

        tk.Label(self, text=f"Bienvenido, {usuario.nombre}!", font=("Segoe UI", 18, "bold"),
                 fg="#5B3E31", bg="#FFF8F0").pack(pady=20)

        container = tk.Frame(self, bg="#FFF8F0")
        container.pack(padx=20, pady=20)

        # Módulos y callbacks
        modulos = [
            ("Usuarios", lambda: on_module_select("usuarios")),
            ("Materiales", lambda: on_module_select("materiales")),
            ("Inventario", lambda: on_module_select("inventario")),
            ("Piezas", lambda: on_module_select("piezas")),
            ("Personalizadas", lambda: on_module_select("personalizadas")),
            ("Pedidos", lambda: on_module_select("pedidos")),
            ("Historial", lambda: on_module_select("historial"))
        ]

        # Crear tarjetas
        for i, (nombre, comando) in enumerate(modulos):
            btn = tk.Button(container, text=nombre, command=comando,
                            font=("Segoe UI", 14, "bold"),
                            bg="#FFD9B3", fg="#5B3E31",
                            activebackground="#FFCC99",
                            width=20, height=4, relief="flat")
            btn.grid(row=i//2, column=i%2, padx=15, pady=15)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#FFCC99"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#FFD9B3"))

        self.pack(fill="both", expand=True)


# ---------- APP PRINCIPAL ----------
class App(tk.Tk):
    """
    Clase principal de la aplicación.
    Maneja login, dashboard y módulos.
    """
    def __init__(self):
        super().__init__()
        self.title("Cerámica Artesanal")
        self.geometry("900x700")
        self.resizable(False, False)
        self.configure(bg="#FFF8F0")
        self.current_frame = None
        self.show_login()

    # ---------- LOGIN ----------
    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginWindow(
            self,
            on_login_success=self.show_dashboard,
            on_register=self.show_register
        )

    # ---------- DASHBOARD ----------
    def show_dashboard(self, usuario):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Dashboard(self, usuario, on_module_select=self.show_module)

    # ---------- MÓDULOS ----------
    def show_module(self, modulo):
        if self.current_frame:
            self.current_frame.destroy()

        frames = {
            "usuarios": UsuariosFrame,
            "materiales": MaterialesFrame,
            "inventario": InventarioFrame,
            "piezas": PiezasFrame,
            "personalizadas": PersonalizadasFrame,
            "pedidos": PedidosFrame,
            "historial": HistorialFrame
        }
        frame_class = frames.get(modulo)
        if frame_class:
            self.current_frame = frame_class(self)
            # Botón para volver al dashboard
            tk.Button(self.current_frame, text="← Volver al Dashboard",
                      command=lambda: self.show_dashboard(self.current_frame.usuario if hasattr(self.current_frame, 'usuario') else tipo('Usuario', '', '', '', '', '')),
                      font=("Segoe UI", 12, "bold"),
                      bg="#FFD9B3", fg="#5B3E31", relief="flat").pack(pady=10)

    # ---------- REGISTRO (placeholder) ----------
    def show_register(self):
        messagebox.showinfo("Registro", "Aquí irá la pantalla de registro.")


# ---------- EJECUTAR APP ----------
if __name__ == "__main__":
    app = App()
    app.mainloop()
