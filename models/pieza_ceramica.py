from db_connection import get_conn

class PiezaCeramica:
    @staticmethod
    def create(nombre, descripcion, precio_base, tipo, material_id):
        conn = get_conn()
        cur = conn.cursor()
        sql = """
            INSERT INTO pieza (nombre, descripcion, precio_base, tipo, material_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(sql, (nombre, descripcion, precio_base, tipo, material_id))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio_base, p.tipo, m.nombre
            FROM pieza p
            JOIN material m ON m.id = p.material_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
