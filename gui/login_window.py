import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario

class LoginWindow(tk.Frame):
    def __init__(self, parent, on_login_success, on_register):
        super().__init__(parent, bg="#1E1E1E")
        self.parent = parent
        self.on_login_success = on_login_success
        self.on_register = on_register

        # ---------- TÍTULO ----------
        lbl_title = tk.Label(
            self,
            text="CERÁMICA ARTESANAL",
            font=("Segoe UI", 18, "bold"),
            fg="#F0F0F0",
            bg="#1E1E1E"
        )
        lbl_title.pack(pady=(40, 20))

        # ---------- FORMULARIO ----------
        form = tk.Frame(self, bg="#1E1E1E")
        form.pack(pady=10)

        tk.Label(form, text="Usuario:", font=("Segoe UI", 12), bg="#1E1E1E", fg="#CCCCCC").grid(row=0, column=0, sticky="w")
        self.entry_user = ttk.Entry(form, width=30)
        self.entry_user.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Contraseña:", font=("Segoe UI", 12), bg="#1E1E1E", fg="#CCCCCC").grid(row=2, column=0, sticky="w")
        self.entry_pass = ttk.Entry(form, width=30, show="*")
