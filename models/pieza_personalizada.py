# pieza_personalizada.py
from db_connection import get_conn

class PiezaPersonalizada:
    """
    Clase para manejar piezas personalizadas hechas a pedido del cliente.
    """

    @staticmethod
    def create(pieza_id, descripcion_personalizacion, precio_extra, diseño_cliente, material_extra):
        """
        Crea un registro de pieza personalizada.
        :return: ID de la pieza personalizada
        """
        conn = get_conn()
        cur = conn.cursor()
        sql = """
        INSERT INTO pieza_personalizada
        (pieza_id, descripcion_personalizacion, precio_extra, diseño_cliente, material_extra)
        VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(sql, (pieza_id, descripcion_personalizacion, precio_extra, diseño_cliente, material_extra))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id
