from db_connection import get_conn
import mysql.connector

class Usuario:
    def __init__(self, id, nombre, correo, telefono, role, contraseña_hash):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.role = role
        self.contraseña_hash = contraseña_hash

    @staticmethod
    def create(nombre, correo, telefono, role, contraseña_hash):
        conn = get_conn()
        cur = conn.cursor()
        sql = """
            INSERT INTO usuario (nombre, correo, telefono, role, contraseña_hash)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(sql, (nombre, correo, telefono, role, contraseña_hash))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE id=%s", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def update(id, nombre, correo, telefono, role):
        conn = get_conn()
        cur = conn.cursor()
        sql = """
            UPDATE usuario SET nombre=%s, correo=%s, telefono=%s, role=%s
            WHERE id=%s
        """
        cur.execute(sql, (nombre, correo, telefono, role, id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete(id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuario WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()