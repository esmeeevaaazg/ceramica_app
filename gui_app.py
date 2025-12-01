import tkinter as tk
from tkinter import messagebox
from ceramica_app.gui.login_window import LoginWindow  # Import absoluto correcto

def on_login_success(usuario):
    messagebox.showinfo("Éxito", f"¡Bienvenido {usuario.usuario}!")
    root.destroy()  # cerrar ventana login

def on_register():
    messagebox.showinfo("Registro", "Aquí iría la ventana de registro.")

root = tk.Tk()
root.title("Cerámica Artesanal")
root.geometry("400x500")
root.config(bg="#FFF8F0")

login_frame = LoginWindow(root, on_login_success, on_register)
login_frame.pack(fill="both", expand=True)

root.mainloop()
