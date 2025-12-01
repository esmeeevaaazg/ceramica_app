import mysql.connector

class Usuario:
    def __init__(self, usuario):
        self.usuario = usuario

    @staticmethod
    def validar(usuario, password):
        try:
            # Conexión a MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # tu contraseña de MySQL
                database="ceramica_db"
            )
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE usuario=%s AND password=%s"
            cursor.execute(query, (usuario, password))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                return Usuario(result["usuario"])
            else:
                return None
        except mysql.connector.Error as err:
            print("Error MySQL:", err)
            return None

    @staticmethod
    def get_all():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # tu contraseña de MySQL
                database="ceramica_db"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios")
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return [Usuario(r["usuario"]) for r in results]
        except mysql.connector.Error as err:
            print("Error MySQL:", err)
            return []
