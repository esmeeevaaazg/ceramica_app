# inventario.py
from db_connection import get_conn

class Inventario:
    """
    Clase para manejar el inventario de materiales.
    Métodos estáticos para CRUD de inventario.
    """

    @staticmethod
    def create(material_id, stock_actual, stock_minimo):
        """
        Crea un registro de inventario para un material.
        :return: ID del nuevo registro
        """
        conn = get_conn()
        cur = conn.cursor()
        sql = """
        INSERT INTO inventario (material_id, stock_actual, stock_minimo)
        VALUES (%s, %s, %s)
        """
        cur.execute(sql, (material_id, stock_actual, stock_minimo))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        """
        Devuelve todos los registros de inventario con nombre de material.
        """
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
        SELECT inv.id, mat.nombre, inv.stock_actual, inv.stock_minimo
        FROM inventario inv
        JOIN material mat ON mat.id = inv.material_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def update(id, stock_actual, stock_minimo):
        """
        Actualiza el stock actual y mínimo de un inventario.
        """
        conn = get_conn()
        cur = conn.cursor()
        sql = """
        UPDATE inventario SET stock_actual=%s, stock_minimo=%s WHERE id=%s
        """
        cur.execute(sql, (stock_actual, stock_minimo, id))
        conn.commit()
        cur.close()
        conn.close()
