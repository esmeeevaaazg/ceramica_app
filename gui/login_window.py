# login_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario

class LoginWindow(tk.Frame):
    """
    Ventana de login de la app Cerámica Artesanal.
    Diseño en modo claro, colores cálidos y tipografía elegante.
    """
    def __init__(self, parent, on_login_success, on_register):
        super().__init__(parent, bg="#FFF8F0")  # Fondo cálido
        self.parent = parent
        self.on_login_success = on_login_success
        self.on_register = on_register

        # ---------- TÍTULO PRINCIPAL ----------
        lbl_title = tk.Label(
            self,
            text="CERÁMICA ARTESANAL",
            font=("Segoe UI", 20, "bold"),  # Título elegante
            fg="#5B3E31",  # Marrón cálido
            bg="#FFF8F0"
        )
        lbl_title.pack(pady=(40, 20))

        # ---------- FORMULARIO ----------
        form = tk.Frame(self, bg="#FFF8F0")
        form.pack(pady=10)

        # Etiqueta usuario
        tk.Label(
            form,
            text="Usuario:",
            font=("Segoe UI", 12),
            bg="#FFF8F0",
            fg="#5B3E31"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_user = ttk.Entry(form, width=30)
        self.entry_user.grid(row=1, column=0, padx=5, pady=5)

        # Etiqueta contraseña
        tk.Label(
            form,
            text="Contraseña:",
            font=("Segoe UI", 12),
            bg="#FFF8F0",
            fg="#5B3E31"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_pass = ttk.Entry(form, width=30, show="*")
        self.entry_pass.grid(row=3, column=0, padx=5, pady=5)

        # ---------- BOTÓN LOGIN ----------
        btn_login = tk.Button(
            self,
            text="Iniciar Sesión",
            font=("Segoe UI", 12, "bold"),
            bg="#FFD9B3",
            fg="#5B3E31",
            activebackground="#FFB366",
            width=25,
            height=2,
            relief="raised",
            bd=2,
            command=self.login
        )
        btn_login.pack(pady=(20, 10))

        # ---------- BOTÓN REGISTRO ----------
        btn_register = tk.Button(
            self,
            text="Registrarse",
            font=("Segoe UI", 12, "bold"),
            bg="#FFE5CC",
            fg="#5B3E31",
            activebackground="#FFCC99",
            width=25,
            height=2,
            relief="raised",
            bd=2,
            command=self.on_register
        )
        btn_register.pack(pady=(0, 20))

        self.pack(fill="both", expand=True)

    # ---------- MÉTODO DE LOGIN ----------
    def login(self):
        """
        Valida el login del usuario.
        Actualmente es un placeholder que siempre inicia sesión con éxito.
        Aquí se puede agregar la lógica real consultando la base de datos.
        """
        usuario_nombre = self.entry_user.get().strip()
        contraseña = self.entry_pass.get().strip()

        if not usuario_nombre or not contraseña:
            messagebox.showwarning("Error", "Por favor ingrese usuario y contraseña.")
            return

        # Placeholder: simulando usuario válido
        # En producción se valida contra la base de datos y hash de contraseña
        usuario = Usuario(id=1, nombre=usuario_nombre, correo="", telefono="", role="admin", contraseña_hash="")
        self.on_login_success(usuario)
