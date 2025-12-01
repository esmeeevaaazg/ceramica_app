import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_connection import get_conn
import hashlib

# ---------- Helpers ----------
def hash_text(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest() if s else None

def run_query(sql, params=(), fetch=False, many=False):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(sql, params)
        if fetch:
            rows = cur.fetchall()
            return rows
        else:
            conn.commit()
            if many:
                return cur.rowcount
            return cur.lastrowid
    finally:
        cur.close()
        conn.close()

# ---------- App and Frames ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cerámica Artesanal — Sistema")
        self.geometry("1000x600")
        self.minsize(900, 500)

        self.current_user = None  # dict {id, nombre, rol}

        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}
        for F in (LoginFrame, DashboardFrame, AdminFrame, ArtesanoFrame, ClienteFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()

    def login_success(self, user_row):
        # user_row: (id, nombre, correo, rol, password)
        self.current_user = {'id': user_row[0], 'nombre': user_row[1], 'correo': user_row[2], 'rol': user_row[3]}
        self.show_frame("DashboardFrame")

# ---------- Login Frame ----------
class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=16)
        self.controller = controller

        title = ttk.Label(self, text="Cerámica Artesanal — Login", font=("Segoe UI", 18, "bold"))
        title.pack(pady=8)

        frm = ttk.Frame(self)
        frm.pack(pady=10)

        ttk.Label(frm, text="Nombre:").grid(row=0, column=0, sticky="e")
        self.ent_name = ttk.Entry(frm, width=30)
        self.ent_name.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frm, text="Contraseña:").grid(row=1, column=0, sticky="e")
        self.ent_pwd = ttk.Entry(frm, width=30, show="*")
        self.ent_pwd.grid(row=1, column=1, padx=6, pady=6)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Iniciar sesión", command=self.login).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="Registrar (cliente)", command=self.register).grid(row=0, column=1, padx=6)

        self.msg = ttk.Label(self, text="")
        self.msg.pack(pady=6)

    def login(self):
        nombre = self.ent_name.get().strip()
        pwd = self.ent_pwd.get().strip()
        if not nombre or not pwd:
            messagebox.showwarning("Datos faltantes", "Ingresa nombre y contraseña.")
            return
        sql = "SELECT id, nombre, correo, rol, password FROM usuarios WHERE nombre = %s"
        rows = run_query(sql, (nombre,), fetch=True)
        if not rows:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return
        row = rows[0]
        stored = row[4]
        if stored is None:
            messagebox.showerror("Error", "Usuario sin contraseña. Pide registro.")
            return
        if hash_text(pwd) != stored:
            messagebox.showerror("Error", "Contraseña incorrecta.")
            return
        # success
        self.controller.login_success(row)

    def register(self):
        nombre = simpledialog.askstring("Registro", "Nombre:")
        if not nombre:
            return
        correo = simpledialog.askstring("Registro", "Correo (opcional):")
        pwd = simpledialog.askstring("Registro", "Contraseña:", show="*")
        pwd_hash = hash_text(pwd) if pwd else None
        sql = "INSERT INTO usuarios (nombre, correo, rol, password) VALUES (%s,%s,%s,%s)"
        try:
            run_query(sql, (nombre.strip(), correo, 'cliente', pwd_hash))
            messagebox.showinfo("OK", "Usuario registrado. Inicia sesión.")
        except Exception as e:
            messagebox.showerror("Error", f"No fue posible registrar: {e}")

# ---------- Dashboard (route to role-specific) ----------
class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=8)
        self.controller = controller

        top = ttk.Frame(self)
        top.pack(fill=tk.X, pady=6)
        self.lbl_user = ttk.Label(top, text="Usuario: —", font=("Segoe UI", 11))
        self.lbl_user.pack(side=tk.LEFT)

        btn_logout = ttk.Button(top, text="Cerrar sesión", command=self.do_logout)
        btn_logout.pack(side=tk.RIGHT)

        # content placeholder
        content = ttk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Panel principal", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.btn_admin = ttk.Button(content, text="Abrir panel Admin", command=lambda: controller.show_frame("AdminFrame"))
        self.btn_artesano = ttk.Button(content, text="Abrir panel Artesano", command=lambda: controller.show_frame("ArtesanoFrame"))
        self.btn_cliente = ttk.Button(content, text="Abrir panel Cliente", command=lambda: controller.show_frame("ClienteFrame"))

        for w in (self.btn_admin, self.btn_artesano, self.btn_cliente):
            w.pack(pady=6)

    def refresh(self):
        u = self.controller.current_user
        if not u:
            return
        self.lbl_user.config(text=f"Usuario: {u['nombre']} ({u['rol']})")
        rol = u['rol']
        # show only relevant buttons
        self.btn_admin.pack_forget()
        self.btn_artesano.pack_forget()
        self.btn_cliente.pack_forget()
        if rol == 'administrador':
            self.btn_admin.pack(pady=6)
        if rol == 'artesano':
            self.btn_artesano.pack(pady=6)
        if rol == 'cliente':
            self.btn_cliente.pack(pady=6)

    def do_logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")

# ---------- Admin Frame ----------
class AdminFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=8)
        self.controller = controller

        top = ttk.Frame(self)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Panel Administrador", font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(top, text="Volver", command=lambda: controller.show_frame("DashboardFrame")).pack(side=tk.RIGHT)

        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, pady=8)

        self.tab_users = ttk.Frame(nb)
        self.tab_material = ttk.Frame(nb)
        self.tab_piezas = ttk.Frame(nb)
        self.tab_inventario = ttk.Frame(nb)
        self.tab_pedidos = ttk.Frame(nb)

        nb.add(self.tab_users, text="Usuarios")
        nb.add(self.tab_material, text="Materiales")
        nb.add(self.tab_piezas, text="Piezas")
        nb.add(self.tab_inventario, text="Inventario")
        nb.add(self.tab_pedidos, text="Pedidos")

        self._build_users_tab()
        self._build_material_tab()
        self._build_piezas_tab()
        self._build_inventario_tab()
        self._build_pedidos_tab()

    def refresh(self):
        # refresh lists
        self._load_users()
        self._load_material()
        self._load_piezas()
        self._load_inventario()
        self._load_pedidos()

    # ---- Users tab ----
    def _build_users_tab(self):
        frame = self.tab_users
        top = ttk.Frame(frame)
        top.pack(fill=tk.X, pady=6)
        ttk.Button(top, text="Crear usuario", command=self._create_user).pack(side=tk.LEFT)
        ttk.Button(top, text="Eliminar seleccionado", command=self._delete_user).pack(side=tk.LEFT, padx=6)

        cols = ("id","nombre","correo","rol")
        self.tree_users = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree_users.heading(c, text=c.capitalize())
            self.tree_users.column(c, width=150)
        self.tree_users.pack(fill=tk.BOTH, expand=True, pady=6)
        self._load_users()

    def _load_users(self):
        rows = run_query("SELECT id, nombre, correo, rol FROM usuarios ORDER BY nombre", fetch=True)
        self.tree_users.delete(*self.tree_users.get_children())
        for r in rows:
            self.tree_users.insert("", tk.END, values=r)

    def _create_user(self):
        nombre = simpledialog.askstring("Crear usuario", "Nombre:")
        if not nombre: return
        correo = simpledialog.askstring("Crear usuario", "Correo (opcional):")
        rol = simpledialog.askstring("Crear usuario", "Rol (cliente/artesano/administrador):", initialvalue="cliente")
        pwd = simpledialog.askstring("Crear usuario", "Contraseña:", show="*")
        pwd_hash = hash_text(pwd) if pwd else None
        sql = "INSERT INTO usuarios (nombre, correo, rol, password) VALUES (%s,%s,%s,%s)"
        try:
            run_query(sql, (nombre.strip(), correo, rol.strip(), pwd_hash))
            messagebox.showinfo("OK", "Usuario creado.")
            self._load_users()
        except Exception as e:
            messagebox.showerror("Error", f"No creado: {e}")

    def _delete_user(self):
        sel = self.tree_users.selection()
        if not sel:
            messagebox.showwarning("Seleccionar", "Selecciona un usuario.")
            return
        uid = self.tree_users.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", f"Eliminar usuario {uid}?"):
            run_query("DELETE FROM usuarios WHERE id=%s", (uid,))
            self._load_users()

    # ---- Material tab ----
    def _build_material_tab(self):
        frame = self.tab_material
        top = ttk.Frame(frame)
        top.pack(fill=tk.X, pady=6)
        ttk.Button(top, text="Agregar material", command=self._create_material).pack(side=tk.LEFT)
        cols = ("id","nombre","tipo")
        self.tree_material = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree_material.heading(c, text=c.capitalize())
            self.tree_material.column(c, width=200)
        self.tree_material.pack(fill=tk.BOTH, expand=True, pady=6)
        self._load_material()

    def _load_material(self):
        rows = run_query("SELECT id, nombre, tipo FROM material ORDER BY nombre", fetch=True)
        self.tree_material.delete(*self.tree_material.get_children())
        for r in rows:
            self.tree_material.insert("", tk.END, values=r)

    def _create_material(self):
        nombre = simpledialog.askstring("Material", "Nombre del material:")
        if not nombre: return
        tipo = simpledialog.askstring("Material", "Tipo (arcilla/pigmento/esmalte):", initialvalue="arcilla")
        run_query("INSERT INTO material (nombre, tipo) VALUES (%s,%s)", (nombre.strip(), tipo.strip()))
        messagebox.showinfo("OK", "Material agregado.")
        self._load_material()

    # ---- Piezas tab ----
    def _build_piezas_tab(self):
        frame = self.tab_piezas
        top = ttk.Frame(frame)
        top.pack(fill=tk.X, pady=6)
        ttk.Button(top, text="Agregar pieza base", command=self._create_pieza).pack(side=tk.LEFT)
        ttk.Button(top, text="Crear pieza personalizada desde seleccionada", command=self._create_pieza_personalizada_from_selected).pack(side=tk.LEFT, padx=6)

        cols = ("id","nombre","tipo","color","precio")
        self.tree_piezas = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree_piezas.heading(c, text=c.capitalize())
            self.tree_piezas.column(c, width=140)
        self.tree_piezas.pack(fill=tk.BOTH, expand=True, pady=6)
        self._load_piezas()

    def _load_piezas(self):
        rows = run_query("SELECT id, nombre, tipo, color, precio FROM pieza_ceramica ORDER BY nombre", fetch=True)
        self.tree_piezas.delete(*self.tree_piezas.get_children())
        for r in rows:
            self.tree_piezas.insert("", tk.END, values=r)

    def _create_pieza(self):
        nombre = simpledialog.askstring("Pieza", "Nombre:")
        if not nombre: return
        tipo = simpledialog.askstring("Pieza", "Tipo (Taza, Jarron, Plato...):")
        color = simpledialog.askstring("Pieza", "Color:")
        precio = simpledialog.askfloat("Pieza", "Precio base:", minvalue=0.0)
        run_query("INSERT INTO pieza_ceramica (nombre, color, tipo, precio) VALUES (%s,%s,%s,%s)", (nombre.strip(), color, tipo, precio or 0.0))
        messagebox.showinfo("OK", "Pieza creada.")
        self._load_piezas()

    def _create_pieza_personalizada_from_selected(self):
        sel = self.tree_piezas.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona una pieza base primero.")
            return
        pid = self.tree_piezas.item(sel[0])["values"][0]
        diseno = simpledialog.askstring("Personalizar", "Descripción del diseño del cliente:")
        material_extra = simpledialog.askstring("Personalizar", "Material extra (opcional):")
        precio_extra = simpledialog.askfloat("Personalizar", "Precio adicional:", minvalue=0.0, initialvalue=0.0)
        # create pieza_ceramica entry and then pieza_personalizada linked by id
        # We'll create a new pieza_ceramica copy to represent the customized piece
        # copy base info
        base = run_query("SELECT nombre, color, tipo, precio FROM pieza_ceramica WHERE id=%s", (pid,), fetch=True)[0]
        nombre_base = base[0] + " (personalizada)"
        precio_base = float(base[3]) + float(precio_extra)
        new_id = run_query("INSERT INTO pieza_ceramica (nombre, color, tipo, precio) VALUES (%s,%s,%s,%s)", (nombre_base, base[1], base[2], precio_base))
        run_query("INSERT INTO pieza_personalizada (id, diseno_cliente, material_extra) VALUES (%s,%s,%s)", (new_id, diseno, material_extra))
        messagebox.showinfo("OK", f"Pieza personalizada creada (id={new_id}).")
        self._load_piezas()

    # ---- Inventario tab ----
    def _build_inventario_tab(self):
        frame = self.tab_inventario
        top = ttk.Frame(frame)
        top.pack(fill=tk.X, pady=6)
        ttk.Button(top, text="Agregar/actualizar inventario", command=self._upsert_inventario).pack(side=tk.LEFT)
        cols = ("id","material","cantidad")
        self.tree_inventario = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree_inventario.heading(c, text=c.capitalize())
            self.tree_inventario.column(c, width=200)
        self.tree_inventario.pack(fill=tk.BOTH, expand=True, pady=6)
        self._load_inventario()

    def _load_inventario(self):
        rows = run_query("SELECT inv.id, m.nombre, inv.cantidad FROM inventario inv JOIN material m ON m.id = inv.material_id", fetch=True)
        self.tree_inventario.delete(*self.tree_inventario.get_children())
        for r in rows:
            self.tree_inventario.insert("", tk.END, values=r)

    def _upsert_inventario(self):
        rows = run_query("SELECT id, nombre FROM material", fetch=True)
        choices = {str(r[0]): r[1] for r in rows}
        mid = simpledialog.askstring("Inventario", f"ID del material:\n{choices}")
        if not mid:
            return
        try:
            qty = simpledialog.askfloat("Inventario", "Cantidad a establecer (ej. 20):", minvalue=0.0)
            # check if exists
            exist = run_query("SELECT id FROM inventario WHERE material_id=%s", (mid,), fetch=True)
            if exist:
                run_query("UPDATE inventario SET cantidad=%s WHERE material_id=%s", (qty, mid))
            else:
                run_query("INSERT INTO inventario (material_id, cantidad) VALUES (%s,%s)", (mid, qty))
            messagebox.showinfo("OK", "Inventario actualizado.")
            self._load_inventario()
        except Exception as e:
            messagebox.showerror("Error", f"No se actualizó: {e}")

    # ---- Pedidos tab (admin view) ----
    def _build_pedidos_tab(self):
        frame = self.tab_pedidos
        top = ttk.Frame(frame)
        top.pack(fill=tk.X, pady=6)
        ttk.Button(top, text="Asignar artesano a pedido", command=self._asignar_artesano).pack(side=tk.LEFT)
        ttk.Button(top, text="Ver historial seleccionado", command=self._ver_historial).pack(side=tk.LEFT, padx=6)

        cols = ("id","cliente","artesano","estado","fecha")
        self.tree_pedidos = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree_pedidos.heading(c, text=c.capitalize())
            self.tree_pedidos.column(c, width=150)
        self.tree_pedidos.pack(fill=tk.BOTH, expand=True, pady=6)
        self._load_pedidos()

    def _load_pedidos(self):
        rows = run_query("""
            SELECT p.id, u.nombre as cliente, a.nombre as artesano, p.estado, p.fecha
            FROM pedido p
            JOIN usuarios u ON u.id = p.cliente_id
            LEFT JOIN usuarios a ON a.id = p.artesano_id
            ORDER BY p.fecha DESC
        """, fetch=True)
        self.tree_pedidos.delete(*self.tree_pedidos.get_children())
        for r in rows:
            self.tree_pedidos.insert("", tk.END, values=r)

    def _asignar_artesano(self):
        sel = self.tree_pedidos.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un pedido.")
            return
        pid = self.tree_pedidos.item(sel[0])["values"][0]
        artesanos = run_query("SELECT id, nombre FROM usuarios WHERE rol='artesano'", fetch=True)
        choices = {str(r[0]): r[1] for r in artesanos}
        aid = simpledialog.askstring("Asignar", f"ID artesano:\n{choices}")
        if not aid:
            return
        run_query("UPDATE pedido SET artesano_id=%s, estado=%s WHERE id=%s", (aid, 'asignado', pid))
        run_query("INSERT INTO historial_estado_pedido (pedido_id, estado) VALUES (%s,%s)", (pid, 'asignado'))
        messagebox.showinfo("OK", "Artesano asignado.")
        self._load_pedidos()

    def _ver_historial(self):
        sel = self.tree_pedidos.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un pedido.")
            return
        pid = self.tree_pedidos.item(sel[0])["values"][0]
        rows = run_query("SELECT estado, fecha FROM historial_estado_pedido WHERE pedido_id=%s ORDER BY fecha DESC", (pid,), fetch=True)
        txt = "\\n".join([f"{r[1]} — {r[0]}" for r in rows])
        messagebox.showinfo("Historial", txt or "(sin historial)")

# ---------- Artesano Frame ----------
class ArtesanoFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=8)
        self.controller = controller
        top = ttk.Frame(self)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Panel Artesano", font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(top, text="Volver", command=lambda: controller.show_frame("DashboardFrame")).pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=("id","cliente","estado","fecha"), show="headings")
        for c in ("id","cliente","estado","fecha"):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=8)

        btns = ttk.Frame(self)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Actualizar estado seleccionado", command=self._actualizar_estado).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Ver piezas del pedido", command=self._ver_piezas).pack(side=tk.LEFT, padx=6)

    def refresh(self):
        # load pedidos asignados a este artesano
        uid = self.controller.current_user['id']
        rows = run_query("SELECT p.id, u.nombre, p.estado, p.fecha FROM pedido p JOIN usuarios u ON u.id=p.cliente_id WHERE p.artesano_id=%s ORDER BY p.fecha DESC", (uid,), fetch=True)
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", tk.END, values=r)

    def _actualizar_estado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un pedido.")
            return
        pid = self.tree.item(sel[0])["values"][0]
        nuevo = simpledialog.askstring("Estado", "Nuevo estado (moldeado/horneado/esmaltado/terminado):")
        if not nuevo:
            return
        run_query("UPDATE pedido SET estado=%s WHERE id=%s", (nuevo, pid))
        run_query("INSERT INTO historial_estado_pedido (pedido_id, estado) VALUES (%s,%s)", (pid, nuevo))
        messagebox.showinfo("OK", "Estado actualizado.")
        self.refresh()

    def _ver_piezas(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un pedido.")
            return
        pid = self.tree.item(sel[0])["values"][0]
        rows = run_query("""
            SELECT pc.nombre, pp.diseno_cliente
            FROM pedido_pieza ppz
            JOIN pieza_ceramica pc ON pc.id = ppz.pieza_id
            LEFT JOIN pieza_personalizada pp ON pp.id = ppz.pieza_id
            WHERE ppz.pedido_id = %s
        """, (pid,), fetch=True)
        txt = "\\n".join([f"{r[0]} — {r[1] or ''}" for r in rows])
        messagebox.showinfo("Piezas", txt or "(sin piezas)")

# ---------- Cliente Frame ----------
class ClienteFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=8)
        self.controller = controller
        top = ttk.Frame(self)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Panel Cliente", font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(top, text="Volver", command=lambda: controller.show_frame("DashboardFrame")).pack(side=tk.RIGHT)

        # top actions
        acts = ttk.Frame(self)
        acts.pack(fill=tk.X, pady=6)
        ttk.Button(acts, text="Crear pedido", command=self._crear_pedido).pack(side=tk.LEFT, padx=6)
        ttk.Button(acts, text="Ver mis pedidos", command=self.refresh).pack(side=tk.LEFT, padx=6)

        cols = ("id","estado","fecha","total")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=8)

    def refresh(self):
        uid = self.controller.current_user['id']
        rows = run_query("SELECT id, estado, fecha, total FROM pedido WHERE cliente_id=%s ORDER BY fecha DESC", (uid,), fetch=True)
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", tk.END, values=r)

    def _crear_pedido(self):
        # choose piece by list
        piezas = run_query("SELECT id, nombre, precio FROM pieza_ceramica ORDER BY nombre", fetch=True)
        choices = {str(r[0]): f"{r[1]} (precio {r[2]})" for r in piezas}
        pid = simpledialog.askstring("Pedido", f"ID de pieza a pedir:\n{choices}")
        if not pid:
            return
        cantidad = simpledialog.askinteger("Pedido", "Cantidad:", minvalue=1, initialvalue=1)
        # create pedido
        uid = self.controller.current_user['id']
        pid_new = run_query("INSERT INTO pedido (cliente_id, estado) VALUES (%s,%s)", (uid, 'registrado'))
        run_query("INSERT INTO pedido_pieza (pedido_id, pieza_id) VALUES (%s,%s)", (pid_new, pid))
        # update total as simple sum
        precio = run_query("SELECT precio FROM pieza_ceramica WHERE id=%s", (pid,), fetch=True)[0][0]
        total = float(precio) * int(cantidad)
        run_query("UPDATE pedido SET total=%s WHERE id=%s", (total, pid_new))
        run_query("INSERT INTO historial_estado_pedido (pedido_id, estado) VALUES (%s,%s)", (pid_new, 'registrado'))
        messagebox.showinfo("OK", f"Pedido creado (id={pid_new}).")
        self.refresh()

# ---------- Run ----------
def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
