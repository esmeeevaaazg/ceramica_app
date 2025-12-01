import tkinter as tk
from tkinter import ttk, messagebox
from ceramica_app.models.usuario import Usuario  # Import absoluto correcto

class LoginWindow(tk.Frame):
    def __init__(self, parent, on_login_success, on_register):
        super().__init__(parent, bg="#FFF8F0")
        self.parent = parent
        self.on_login_success = on_login_success
        self.on_register = on_register

        # ---------- TÍTULO ----------
        lbl_title = tk.Label(
            self,
            text="CERÁMICA ARTESANAL",
            font=("Segoe UI", 18, "bold"),
            fg="#5B3E31",
            bg="#FFF8F0"
        )
        lbl_title.pack(pady=(40, 20))

        # ---------- FORMULARIO ----------
        form = tk.Frame(self, bg="#FFF8F0")
        form.pack(pady=10)

        tk.Label(form, text="Usuario:", font=("Segoe UI", 12), bg="#FFF8F0", fg="#5B3E31").grid(row=0, column=0, sticky="w")
        self.entry_user = ttk.Entry(form, width=30)
        self.entry_user.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Contraseña:", font=("Segoe UI", 12), bg="#FFF8F0", fg="#5B3E31").grid(row=2, column=0, sticky="w")
        self.entry_pass = ttk.Entry(form, width=30, show="*")
        self.entry_pass.grid(row=3, column=0, padx=5, pady=5)

        # ---------- BOTONES ----------
        btn_login = tk.Button(form, text="Iniciar Sesión", bg="#FFD9B3", fg="#5B3E31", font=("Segoe UI",12,"bold"), relief="flat", cursor="hand2", command=self.login)
        btn_login.grid(row=4, column=0, pady=10, sticky="ew")

        btn_register = tk.Button(form, text="Registrarse", bg="#FFCC99", fg="#5B3E31", font=("Segoe UI",12,"bold"), relief="flat", cursor="hand2", command=self.on_register)
        btn_register.grid(row=5, column=0, pady=5, sticky="ew")

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y contraseña.")
            return

        usuario = Usuario.validar(username, password)
        if usuario:
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
