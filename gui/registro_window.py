import tkinter as tk
from tkinter import ttk, messagebox
from ceramica_app.models.usuario import Usuario
import mysql.connector

class RegistroWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro de Usuario")
        self.geometry("400x450") # Tamaño ajustado
        self.config(bg="#FFF8F0")
        self.resizable(False, False)

        tk.Label(self, text="Registro de Usuario", font=("Segoe UI", 16, "bold"), fg="#5B3E31", bg="#FFF8F0").pack(pady=20)

        form = tk.Frame(self, bg="#FFF8F0")
        form.pack(pady=10)

        # CAMPO USUARIO (corresponde a la columna 'nombre' en la DB)
        tk.Label(form, text="Usuario:", font=("Segoe UI", 12), bg="#FFF8F0", fg="#5B3E31").grid(row=0, column=0, sticky="w")
        self.entry_user = ttk.Entry(form, width=30)
        self.entry_user.grid(row=1, column=0, padx=5, pady=5)
        
        # NUEVO CAMPO CORREO
        tk.Label(form, text="Correo:", font=("Segoe UI", 12), bg="#FFF8F0", fg="#5B3E31").grid(row=2, column=0, sticky="w")
        self.entry_email = ttk.Entry(form, width=30)
        self.entry_email.grid(row=3, column=0, padx=5, pady=5)

        # CAMPO CONTRASEÑA
        tk.Label(form, text="Contraseña:", font=("Segoe UI", 12), bg="#FFF8F0", fg="#5B3E31").grid(row=4, column=0, sticky="w")
        self.entry_pass = ttk.Entry(form, width=30, show="*")
        self.entry_pass.grid(row=5, column=0, padx=5, pady=5)

        # CAMPO CONFIRMAR CONTRASEÑA
        tk.Label(form, text="Confirmar contraseña:", font=("Segoe UI", 12), bg="#FFF8F0", fg="#5B3E31").grid(row=6, column=0, sticky="w")
        self.entry_pass2 = ttk.Entry(form, width=30, show="*")
        self.entry_pass2.grid(row=7, column=0, padx=5, pady=5)

        btn_register = tk.Button(form, text="Registrarse", bg="#FFCC99", fg="#5B3E31", font=("Segoe UI",12,"bold"), relief="flat", cursor="hand2", command=self.registrar)
        btn_register.grid(row=8, column=0, pady=15, sticky="ew")

    def registrar(self):
        # OBTENER VALORES (usuario_input es el nombre de la variable)
        usuario_input = self.entry_user.get()
        email = self.entry_email.get()
        password = self.entry_pass.get()
        password2 = self.entry_pass2.get()

        # VALIDACIONES
        if not usuario_input or not email or not password or not password2:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
            return
        if password != password2:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        # Conexión y Guardado en MySQL
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234EsMeVg7-",   # Asegúrate de usar TU contraseña real
                database="ceramica_db"
            )
            cursor = conn.cursor()
            
            # 1. VERIFICACIÓN (USANDO COLUMNA 'nombre')
            cursor.execute("SELECT * FROM usuarios WHERE nombre=%s", (usuario_input,)) 
            if cursor.fetchone():
                messagebox.showerror("Error", "El usuario ya existe.")
                cursor.close()
                conn.close()
                return

            # 2. INSERCIÓN (USANDO COLUMNAS 'nombre', 'correo', 'password', 'rol')
            sql = "INSERT INTO usuarios (nombre, correo, password, rol) VALUES (%s, %s, %s, %s)"
            # Se añade 'cliente' como valor por defecto para el rol
            valores = (usuario_input, email, password, 'cliente') 
            
            cursor.execute(sql, valores)
            conn.commit()
            
            cursor.close()
            conn.close()

            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error MySQL", f"Error al registrar usuario: {err}")