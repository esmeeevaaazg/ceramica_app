import mysql.connector

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre

    @staticmethod
    def validar(usuario, password):
        try:
            # Conexión a MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234EsMeVg7-",  # tu contraseña de MySQL
                database="ceramica_db"
            )
            cursor = conn.cursor(dictionary=True)

            # BUSCAR POR NOMBRE Y PASSWORD
            query = "SELECT * FROM usuarios WHERE nombre=%s AND password=%s"
            cursor.execute(query, (usuario, password))

            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                return Usuario(result["nombre"])
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
                password="1234EsMeVg7-",  # tu contraseña de MySQL
                database="ceramica_db"
            )
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM usuarios")
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            # Lista de objetos Usuario usando "nombre"
            return [Usuario(r["nombre"]) for r in results]

        except mysql.connector.Error as err:
            print("Error MySQL:", err)
            return []
