# login_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario

class LoginWindow(tk.Frame):
    """
    Ventana de login de la aplicación.
    Modo claro con colores cálidos y tipografía elegante.
    """
    def __init__(self, parent, on_login_success, on_register):
        super().__init__(parent, bg="#FFF8F0")
        self.parent = parent
        self.on_login_success = on_login_success
        self.on_register = on_register

        # ---------- TÍTULO ----------
        lbl_title = tk.Label(
            self,
            text="CERÁMICA ARTESANAL",
            font=("Segoe UI", 20, "bold"),
            fg="#5B3E31",
            bg="#FFF8F0"
        )
        lbl_title.pack(pady=(40, 20))

        # ---------- FORMULARIO ----------
        form = tk.Frame(self, bg="#FFF8F0")
        form.pack(pady=10)

        tk.Label(form, text="Usuario:", font=("Segoe UI", 12),
                 bg="#FFF8F0", fg="#5B3E31").grid(row=0, column=0, sticky="w")
        self.entry_user = ttk.Entry(form, width=30)
        self.entry_user.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Contraseña:", font=("Segoe UI", 12),
                 bg="#FFF8F0", fg="#5B3E31").grid(row=2, column=0, sticky="w")
        self.entry_pass = ttk.Entry(form, width=30, show="*")
        self.entry_pass.grid(row=3, column=0, padx=5, pady=5)

        # ---------- BOTONES ----------
        btn_frame = tk.Frame(self, bg="#FFF8F0")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Iniciar Sesión", bg="#FFD9B3", fg="#5B3E31",
                  width=20, command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Registrarse", bg="#FFCC99", fg="#5B3E31",
                  width=20, command=on_register).grid(row=0, column=1, padx=5)

        self.pack(fill="both", expand=True)

    def login(self):
        """
        Valida el usuario (placeholder simple)
        """
        usuario = self.entry_user.get()
        password = self.entry_pass.get()
        if usuario and password:
            # Por ahora creamos un objeto usuario dummy para dashboard
            class DummyUser:
                def __init__(self, nombre):
                    self.nombre = usuario
            self.on_login_success(DummyUser(usuario))
        else:
            messagebox.showerror("Error", "Por favor ingresa usuario y contraseña.")
