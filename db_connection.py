import mysql.connector

def get_conn():
    # Conexion fija, sin variables de entorno
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234EsMeVg7-",  # tu contraseña real
        database="ceramica_db",
        autocommit=False
    )
    return conn
