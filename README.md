# Cerámica Artesanal - App de Escritorio (Tkinter + MySQL)

Proyecto de ejemplo adaptado desde un ejercicio de biblioteca para gestionar **piezas de cerámica**, pedidos, artesanos y clientes.

------------------------------------------------------------------
## Contenido del repositorio

- `db_connection.py` - helper para conectar a MySQL (usar variables de entorno o editar directamente).
- `create_tables.sql` - script para crear las tablas necesarias en MySQL.
- `models/` - clases que modelan `pieza`, `pieza_personalizada`, `usuario`, `pedido`, `inventario`.
- `app.py` - GUI principal (Tkinter) inspirada en tu ejemplo de biblioteca.
- `main.py` - lanzador de la aplicación.
- `README.md` - este archivo.

------------------------------------------------------------------
## Cómo configurar (local)

1. Instala MySQL (ej. MySQL 8) y crea una base de datos, por ejemplo `ceramica_db`.
2. Edita `db_connection.py` para indicar usuario/contraseña/host/DB o exporta env vars:`DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`.
3. Ejecuta el script SQL para crear tablas:
   ```bash
   mysql -u tu_usuario -p ceramica_db < create_tables.sql
   ```
4. Crea un entorno virtual e instala dependencia:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```
5. Inicia la app:
   ```bash
   python main.py
   ```

------------------------------------------------------------------
## Notas
- No subas archivos con contraseñas (usa `.env` o variables de entorno).
- El código está pensado como base para aprender y extender (autenticación más segura, validaciones, control de inventario por receta, etc.).
