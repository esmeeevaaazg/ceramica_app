import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class HomeWindow(tk.Frame):
    """Ventana principal (Dashboard) que muestra el listado de productos y gestiona el carrito."""
    
    def __init__(self, parent, usuario_logueado, on_logout): 
        super().__init__(parent, bg="#FFF8F0")
        self.usuario = usuario_logueado
        self.on_logout = on_logout # Función de callback para cerrar sesión
        self.bolsa_compra = {} # Diccionario para almacenar productos en el carrito

        # --- CONTROLES DE CABECERA ---
        
        # Botón para cerrar sesión 
        btn_logout = tk.Button(self, 
                               text="Cerrar Sesión", 
                               command=self.cerrar_sesion_local,
                               bg="#E0A0A0", fg="#5B3E31")
        # Colocamos el botón en la esquina superior derecha
        btn_logout.pack(anchor="ne", padx=20, pady=10) 

        lbl_welcome = tk.Label(self, text=f"Bienvenido, {self.usuario.nombre}!", 
                               font=("Segoe UI", 16, "bold"), fg="#5B3E31", bg="#FFF8F0")
        lbl_welcome.pack(pady=5)

        lbl_title = tk.Label(self, text="Listado de Productos de Cerámica", 
                             font=("Segoe UI", 14), fg="#5B3E31", bg="#FFF8F0")
        lbl_title.pack(pady=10)
        
        # --- LISTADO DE PRODUCTOS ---
        
        # Frame para el listado de productos
        self.products_frame = tk.Frame(self, bg="#FFFFFF", padx=10, pady=10)
        self.products_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.cargar_productos() # <-- Llamada que causaba el AttributeError
        
        # --- FOOTER / BOLSA DE COMPRA ---

        # Botón para ver la bolsa de compra
        self.btn_view_cart = tk.Button(self, text=f"Ver Bolsa ({self.get_total_items()})", 
                                  command=self.mostrar_bolsa, bg="#FFCC99", fg="#5B3E31")
        self.btn_view_cart.pack(pady=10)

    # --- MÉTODOS DE LÓGICA DE LA APLICACIÓN ---

    def cerrar_sesion_local(self):
        """Método local que llama al callback de MainApp para cambiar de vista."""
        self.on_logout() 
        
    def obtener_productos(self):
        """Obtiene el listado de productos desde la base de datos MySQL."""
        productos = []
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234EsMeVg7-", # Usa TU CONTRASEÑA REAL
                database="ceramica_db"
            )
            cursor = conn.cursor()
            # Consulta a la tabla 'productos' (asumiendo que ya la creaste)
            cursor.execute("SELECT id, nombre, precio FROM productos ORDER BY id ASC")
            
            for (id, nombre, precio) in cursor:
                productos.append({'id': id, 'nombre': nombre, 'precio': float(precio)})
            
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            # Muestra el error si la tabla 'productos' no existe o hay un fallo de conexión
            messagebox.showerror("Error DB", f"No se pudo cargar productos: {err}")
        
        # Si la base de datos está vacía o falló, devuelve datos de ejemplo para evitar la caída total
        if not productos:
             return [
                 {'id': 10, 'nombre': 'Taza de Prueba', 'precio': 10.00},
                 {'id': 11, 'nombre': 'Plato de Prueba', 'precio': 20.00},
             ]
        return productos

    def cargar_productos(self):
        """Crea y muestra el listado de productos en el Frame."""
        products = self.obtener_productos()
        
        # Limpiar frame anterior (en caso de recarga)
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        for i, product in enumerate(products):
            product_id = product['id']
            name = product['nombre']
            price = product['precio']
            
            row = tk.Frame(self.products_frame, bg="#FFFFFF")
            row.grid(row=i, column=0, pady=5, sticky="ew")

            # Nombre y precio
            tk.Label(row, text=f"{name} - ${price:.2f}", font=("Segoe UI", 10), bg="#FFFFFF", width=35, anchor='w').pack(side="left", padx=10)
            
            # Botón "Agregar a la Bolsa"
            add_btn = tk.Button(row, text="Añadir a Bolsa", 
                                command=lambda p=product: self.agregar_a_bolsa(p), 
                                bg="#ADD8E6", fg="#000000")
            add_btn.pack(side="right")
    
    def agregar_a_bolsa(self, product):
        """Agrega un producto al diccionario de la bolsa de compra."""
        product_id = product['id']
        
        if product_id in self.bolsa_compra:
            self.bolsa_compra[product_id]['cantidad'] += 1
        else:
            self.bolsa_compra[product_id] = {'producto': product, 'cantidad': 1}
        
        messagebox.showinfo("Bolsa", f"'{product['nombre']}' añadido a la bolsa.")
        self.update_cart_button()

    def get_total_items(self):
        """Calcula el total de artículos en la bolsa."""
        return sum(item['cantidad'] for item in self.bolsa_compra.values())

    def update_cart_button(self):
        """Actualiza el texto del botón del carrito con el total de artículos."""
        self.btn_view_cart.config(text=f"Ver Bolsa ({self.get_total_items()})")
            
    def mostrar_bolsa(self):
        """Muestra los contenidos de la bolsa de compra."""
        if not self.bolsa_compra:
            messagebox.showinfo("Bolsa de Compra", "La bolsa está vacía.")
            return

        detalle = "Contenido de la Bolsa:\n"
        total = 0
        for item in self.bolsa_compra.values():
            p = item['producto']
            qty = item['cantidad']
            subtotal = p['precio'] * qty
            detalle += f"- {p['nombre']} (x{qty}): ${subtotal:.2f}\n"
            total += subtotal
        
        detalle += f"\nTotal a Pagar: ${total:.2f}"
        messagebox.showinfo("Bolsa de Compra", detalle)