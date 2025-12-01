# material.py
from db_connection import get_conn

class Material:
    """
    Clase para gestionar los materiales disponibles.
    Métodos CRUD: create, get_all, get_by_id, update, delete.
    """

    @staticmethod
    def create(nombre, proveedor, costo_unitario):
        """
        Crea un nuevo material.
        :return: ID del material creado
        """
        conn = get_conn()
        cur = conn.cursor()
        sql = """
        INSERT INTO material (nombre, proveedor, costo_unitario)
        VALUES (%s, %s, %s)
        """
        cur.execute(sql, (nombre, proveedor, costo_unitario))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        """Devuelve todos los materiales"""
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM material")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(id):
        """Devuelve un material según su ID"""
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM material WHERE id=%s", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def update(id, nombre, proveedor, costo_unitario):
        """Actualiza un material existente"""
        conn = get_conn()
        cur = conn.cursor()
        sql = """
        UPDATE material SET nombre=%s, proveedor=%s, costo_unitario=%s WHERE id=%s
        """
        cur.execute(sql, (nombre, proveedor, costo_unitario, id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete(id):
        """Elimina un material por ID"""
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM material WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
