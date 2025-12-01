from db_connection import get_conn

class PedidoEstadoHistorial:
    @staticmethod
    def create(pedido_id, estado):
        conn = get_conn()
        cur = conn.cursor()
        sql = """
            INSERT INTO pedido_estado_historial (pedido_id, estado)
            VALUES (%s, %s)
        """
        cur.execute(sql, (pedido_id, estado))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_by_pedido(pedido_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT estado, fecha
            FROM pedido_estado_historial
            WHERE pedido_id = %s
            ORDER BY fecha DESC
        """, (pedido_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
