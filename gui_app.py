import tkinter as tk
from tkinter import ttk, messagebox
from gui.login_window import LoginWindow

# ---------- VENTANAS / FRAMES DE CADA MÓDULO ----------
class UsuariosFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")
        tk.Label(self, text="Usuarios", font=("Segoe UI", 18, "bold"), fg="#F0F0F0", bg="#1E1E1E").pack(pady=20)
        # Aquí agregarás widgets para la gestión de usuarios

class MaterialesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")
        tk.Label(self, text="Materiales", font=("Segoe UI", 18, "bold"), fg="#F0F0F0", bg="#1E1E1E").pack(pady=20)

class InventarioFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")
        tk.Label(self, text="Inventario", font=("Segoe UI", 18, "bold"), fg="#F0F0F0", bg="#1E1E1E").pack(pady=20)

class PiezasFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")
        tk.Label(self, text="Piezas", font=("Segoe UI", 18, "bold"), fg="#F0F0F0", bg="#1E1E1E").pack(pady=20)

class PersonalizadasFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")
        tk.Label(self, text="Personalizadas", font=("Segoe UI", 18, "bold"), fg="#F0F0F0", bg="#1E1E1E").pack(pady=20)

class PedidosFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")
        tk.Label(self, text="Pedidos", font=("Segoe UI", 18, "bold"), fg="#F0F0F0", bg="#1E1E1E").pack(pady=20)

class HistorialFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")
        tk.Label(self, text="Historial", font=("Segoe UI", 18, "bold"), fg="#F0F0F0", bg="#1E1E1E").pack(pady=20)

# ---------- DASHBOARD ESTILO TARJETAS ----------
class Dashboard(tk.Frame):
    def __init__(self, parent, usuario, on_module_select):
        super().__init__(parent, bg="#1E1E1E")
        self.usuario = usuario
        self.on_module_select = on_module_select

        tk.Label(self, text=f"Bienvenido, {usuario.nombre}!", font=("Segoe UI", 18, "bold"),
                 fg="#F0F0F0", bg="#1E1E1E").pack(pady=20)

        container = tk.Frame(self, bg="#1E1E1E")
        container.pack(padx=20, pady=20)

        # Módulos y sus callbacks
        modulos = [
            ("Usuarios", lambda: on_module_select("usuarios")),
            ("Materiales", lambda: on_module_select("materiales")),
            ("Inventario", lambda: on_module_select("inventario")),
            ("Piezas", lambda: on_module_select("piezas")),
            ("Personalizadas", lambda: on_module_select("personalizadas")),
            ("Pedidos", lambda: on_module_select("pedidos")),
            ("Historial", lambda: on_module_select("historial"))
        ]

        # Crear tarjetas con efecto hover
        for i, (nombre, comando) in enumerate(modulos):
            btn = tk.Button(container, text=nombre, command=comando,
                            font=("Segoe UI", 14, "bold"),
                            bg="#2E2E2E", fg="#F0F0F0", activebackground="#3E3E3E",
                            width=20, height=4, relief="flat")
            btn.grid(row=i//2, column=i%2, padx=15, pady=15)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3E3E3E"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2E2E2E"))

        self.pack(fill="both", expand=True)

# ---------- APP PRINCIPAL ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cerámica Artesanal")
        self.geometry("900x700")
        self.resizable(False, False)
        self.configure(bg="#1E1E1E")

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
            tk.Button(self.current_frame, text="← Volver al Dashboard", command=lambda: self.show_dashboard(self.current_frame.usuario if hasattr(self.current_frame, 'usuario') else usuario),
                      font=("Segoe UI", 12, "bold"), bg="#2E2E2E", fg="#F0F0F0", relief="flat").pack(pady=10)

    # ---------- REGISTRO (placeholder) ----------
    def show_register(self):
        messagebox.showinfo("Registro", "Aquí irá la pantalla de registro.")

# ---------- EJECUTAR APP ----------
if __name__ == "__main__":
    app = App()
    app.mainloop()
