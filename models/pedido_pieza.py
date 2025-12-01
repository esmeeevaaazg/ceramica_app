from db_connection import get_conn

class PedidoPieza:
    @staticmethod
    def create(pedido_id, pieza_id, cantidad):
        conn = get_conn()
        cur = conn.cursor()
        sql = """
            INSERT INTO pedido_pieza (pedido_id, pieza_id, cantidad)
            VALUES (%s, %s, %s)
        """
        cur.execute(sql, (pedido_id, pieza_id, cantidad))
        conn.commit()
        cur.close()
        conn.close()
