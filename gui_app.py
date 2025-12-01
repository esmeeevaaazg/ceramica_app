import tkinter as tk
from tkinter import messagebox
# Importa las ventanas necesarias
from ceramica_app.gui.login_window import LoginWindow
from ceramica_app.gui.registro_window import RegistroWindow
from ceramica_app.gui.home_window import HomeWindow

class MainApp(tk.Tk):
    """Clase principal de la aplicación que gestiona la ventana raíz (Root)
       y el cambio entre vistas (Login y Home)."""
       
    def __init__(self):
        super().__init__()
        self.title("Cerámica Artesanal App")
        # Establece un tamaño base para la ventana principal
        self.geometry("600x600") 
        
        # 1. Crear y mostrar la ventana de Login al inicio
        self.mostrar_login()

    def mostrar_login(self):
        """Muestra el frame de inicio de sesión."""
        # Se pasa una referencia a los métodos para que LoginWindow pueda llamarlos.
        self.login_frame = LoginWindow(
            self, 
            on_login_success=self.on_login_success, 
            on_register=self.abrir_registro 
        )
        self.login_frame.pack(fill="both", expand=True)

    def on_login_success(self, usuario):
        """Método llamado por LoginWindow al iniciar sesión con éxito."""
        
        # 1. Destruye el frame de Login para liberarlo de la ventana principal
        if hasattr(self, 'login_frame') and self.login_frame.winfo_exists():
            self.login_frame.destroy() 
        
        # 2. Crea y empaqueta la nueva ventana Home (Dashboard de productos)
        self.home_frame = HomeWindow(self, usuario)
        self.home_frame.pack(fill="both", expand=True)

        messagebox.showinfo("Éxito", f"¡Bienvenido {usuario.nombre}!")

    def abrir_registro(self):
        """Abre la ventana de registro como una ventana Toplevel."""
        RegistroWindow(self)

    def cerrar_sesion(self):
        """Maneja la lógica de cerrar sesión: destruye Home y muestra Login."""
        if hasattr(self, 'home_frame') and self.home_frame.winfo_exists():
            self.home_frame.destroy()
            
        # Llamamos al método que ya existe para mostrar el frame de Login
        self.mostrar_login()
        messagebox.showinfo("Sesión", "Has cerrado tu sesión.")
    
    def on_login_success(self, usuario):
        """Método llamado por LoginWindow al iniciar sesión con éxito."""
        
        # 1. Destruye el frame de Login
        if hasattr(self, 'login_frame') and self.login_frame.winfo_exists():
            self.login_frame.destroy() 
        
        # 2. Crea HomeWindow y PASA EL CALLBACK DE LOGOUT
        # HomeWindow requiere ahora 3 argumentos, el tercero es on_logout
        self.home_frame = HomeWindow(self, usuario, on_logout=self.cerrar_sesion)
        self.home_frame.pack(fill="both", expand=True)

        messagebox.showinfo("Éxito", f"¡Bienvenido {usuario.nombre}!")
        
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()