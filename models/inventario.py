from db_connection import get_conn

class Inventario:
    @staticmethod
    def create(material_id, stock_actual, stock_minimo):
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
        conn = get_conn()
        cur = conn.cursor()
        sql = """
            UPDATE inventario
            SET stock_actual=%s, stock_minimo=%s
            WHERE id=%s
        """
        cur.execute(sql, (stock_actual, stock_minimo, id))
        conn.commit()
        cur.close()
        conn.close()
