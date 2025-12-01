# historial_estado_pedido.py
from db_connection import get_conn

class PedidoEstadoHistorial:
    """
    Clase para gestionar el historial de estados de los pedidos.
    Permite crear y consultar los estados de cada pedido.
    """

    @staticmethod
    def create(pedido_id, estado):
        """
        Inserta un nuevo estado en el historial de un pedido.
        :param pedido_id: ID del pedido
        :param estado: Estado a registrar (pendiente, en proceso, completado, etc.)
        """
        conn = get_conn()
        cur = conn.cursor()
        sql = """
        INSERT INTO pedido_estado_historial (pedido_id, estado) VALUES (%s, %s)
        """
        cur.execute(sql, (pedido_id, estado))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_by_pedido(pedido_id):
        """
        Devuelve todos los estados de un pedido ordenados por fecha descendente.
        :param pedido_id: ID del pedido
        :return: Lista de tuplas (estado, fecha)
        """
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
        SELECT estado, fecha FROM pedido_estado_historial
        WHERE pedido_id = %s
        ORDER BY fecha DESC
        """, (pedido_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
