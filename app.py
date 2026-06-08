from flask import Flask
import psycopg2

app = Flask(__name__)
VERSION = "3.0.0"

@app.route("/")
def inicio():
    try:
        # Conexión a la base de datos de Docker
        conexion = psycopg2.connect(
            host="db",
            database="empresa",
            user="admin",
            password="admin123"
        )
        cursor = conexion.cursor()
        
        # Obtener versión de Postgres
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        # Lógica para listar clientes (Actividad 5)
        clientes_html = ""
        try:
            cursor.execute("SELECT id, nombre FROM clientes;")
            clientes = cursor.fetchall()
            if clientes:
                clientes_html = "<h3>Lista de Clientes:</h3><ul>"
                for cli in clientes:
                    clientes_html += f"<li>ID: {cli[0]} - Nombre: {cli[1]}</li>"
                clientes_html += "</ul>"
            else:
                clientes_html = "<p>No hay clientes registrados aún.</p>"
        except Exception:
            # Si la tabla no existe todavía, evita que la app falle
            conexion.rollback() 
            clientes_html = "<p>Tabla 'clientes' no creada o no encontrada.</p>"

        cursor.close()
        conexion.close()

        return f"""
        <h1>Aplicación Flask</h1>
        <h2>Versión {VERSION}</h2>
        <p>Conexión exitosa a PostgreSQL</p>
        <p><strong>BD Info:</strong> {db_version[0]}</p>
        {clientes_html}
        """

    except Exception as e:
        return f"<h1>Error de Conexión</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)