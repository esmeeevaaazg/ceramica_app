# pedido_pieza.py
from db_connection import get_conn

class PedidoPieza:
    """
    Clase para gestionar la relación entre pedidos y piezas.
    Permite asignar piezas a un pedido con la cantidad correspondiente.
    """

    @staticmethod
    def create(pedido_id, pieza_id, cantidad):
        """
        Crea un registro indicando que cierta pieza pertenece a un pedido.
        """
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
