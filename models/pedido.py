from db_connection import get_conn

class Pedido:
    @staticmethod
    def create(cliente_id, estado="pendiente"):
        conn = get_conn()
        cur = conn.cursor()
        sql = """
            INSERT INTO pedido (cliente_id, estado)
            VALUES (%s, %s)
        """
        cur.execute(sql, (cliente_id, estado))
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
            SELECT p.id, u.nombre, p.estado, p.fecha_creacion
            FROM pedido p
            JOIN usuarios u ON u.id = p.cliente_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
