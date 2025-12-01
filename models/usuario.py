# usuarios_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario

class UsuariosFrame(tk.Frame):
    """
    Ventana de gestión de usuarios.
    Permite listar, agregar, editar y eliminar usuarios.
    Estilo: fondo cálido claro, tipografía elegante y botones interactivos.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF8F0")  # Fondo cálido

        # Título
        tk.Label(self, text="Usuarios", font=("Segoe UI", 18, "bold"),
                 fg="#5B3E31", bg="#FFF8F0").pack(pady=15)

        # Tabla de usuarios
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Correo", "Teléfono", "Rol"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=20, pady=10, fill="x")

        # Botones
        btn_frame = tk.Frame(self, bg="#FFF8F0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Agregar Usuario", bg="#FFD9B3", fg="#5B3E31",
                  width=15, command=self.agregar_usuario).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar Usuario", bg="#FFCC99", fg="#5B3E31",
                  width=15, command=self.editar_usuario).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Usuario", bg="#FFB366", fg="#5B3E31",
                  width=15, command=self.eliminar_usuario).grid(row=0, column=2, padx=5)

        # Cargar datos iniciales
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """Carga todos los usuarios en la tabla"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for u in Usuario.get_all():
            self.tree.insert("", "end", values=(u[0], u[1], u[2], u[3], u[4]))

    def agregar_usuario(self):
        """Muestra un formulario para agregar usuario"""
        messagebox.showinfo("Agregar", "Aquí se agregará el formulario para nuevo usuario.")

    def editar_usuario(self):
        """Permite editar el usuario seleccionado"""
        messagebox.showinfo("Editar", "Aquí se editará el usuario seleccionado.")

    def eliminar_usuario(self):
        """Elimina el usuario seleccionado"""
        messagebox.showinfo("Eliminar", "Aquí se eliminará el usuario seleccionado.")

def agregar_usuario(self):
    """Formulario para agregar usuario nuevo"""
    def guardar():
        nombre = entry_nombre.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()
        role = entry_role.get()
        contraseña = entry_pass.get()
        if nombre and correo and role and contraseña:
            Usuario.create(nombre, correo, telefono, role, contraseña)
            self.cargar_usuarios()
            top.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos obligatorios deben llenarse.")

    top = tk.Toplevel(self)
    top.title("Agregar Usuario")
    top.geometry("350x300")
    top.configure(bg="#FFF8F0")

    tk.Label(top, text="Nombre:", bg="#FFF8F0").pack(pady=5)
    entry_nombre = tk.Entry(top, width=30)
    entry_nombre.pack()

    tk.Label(top, text="Correo:", bg="#FFF8F0").pack(pady=5)
    entry_correo = tk.Entry(top, width=30)
    entry_correo.pack()

    tk.Label(top, text="Teléfono:", bg="#FFF8F0").pack(pady=5)
    entry_telefono = tk.Entry(top, width=30)
    entry_telefono.pack()

    tk.Label(top, text="Rol:", bg="#FFF8F0").pack(pady=5)
    entry_role = tk.Entry(top, width=30)
    entry_role.pack()

    tk.Label(top, text="Contraseña:", bg="#FFF8F0").pack(pady=5)
    entry_pass = tk.Entry(top, width=30, show="*")
    entry_pass.pack()

    tk.Button(top, text="Guardar", bg="#FFD9B3", fg="#5B3E31",
              command=guardar).pack(pady=15)

def editar_usuario(self):
    """Formulario para editar usuario seleccionado"""
    selected = self.tree.focus()
    if not selected:
        messagebox.showwarning("Editar", "Selecciona un usuario primero.")
        return

    values = self.tree.item(selected, "values")
    user_id = values[0]

    top = tk.Toplevel(self)
    top.title("Editar Usuario")
    top.geometry("350x280")
    top.configure(bg="#FFF8F0")

    tk.Label(top, text="Nombre:", bg="#FFF8F0").pack(pady=5)
    entry_nombre = tk.Entry(top, width=30)
    entry_nombre.insert(0, values[1])
    entry_nombre.pack()

    tk.Label(top, text="Correo:", bg="#FFF8F0").pack(pady=5)
    entry_correo = tk.Entry(top, width=30)
    entry_correo.insert(0, values[2])
    entry_correo.pack()

    tk.Label(top, text="Teléfono:", bg="#FFF8F0").pack(pady=5)
    entry_telefono = tk.Entry(top, width=30)
    entry_telefono.insert(0, values[3])
    entry_telefono.pack()

    tk.Label(top, text="Rol:", bg="#FFF8F0").pack(pady=5)
    entry_role = tk.Entry(top, width=30)
    entry_role.insert(0, values[4])
    entry_role.pack()

    def guardar():
        Usuario.update(user_id, entry_nombre.get(), entry_correo.get(),
                       entry_telefono.get(), entry_role.get())
        self.cargar_usuarios()
        top.destroy()

    tk.Button(top, text="Guardar Cambios", bg="#FFCC99", fg="#5B3E31",
              command=guardar).pack(pady=15)

def eliminar_usuario(self):
    """Eliminar usuario seleccionado"""
    selected = self.tree.focus()
    if not selected:
        messagebox.showwarning("Eliminar", "Selecciona un usuario primero.")
        return
    values = self.tree.item(selected, "values")
    user_id = values[0]
    if messagebox.askyesno("Eliminar", f"¿Eliminar usuario {values[1]}?"):
        Usuario.delete(user_id)
        self.cargar_usuarios()
