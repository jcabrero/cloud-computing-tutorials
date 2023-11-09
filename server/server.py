from flask import Flask, request, render_template
import logging as log
import mysql.connector

log.basicConfig(level=log.INFO)

app = Flask(__name__)

# Configura la conexion a la base de datos MySQL
db_config = {
    'host': 'mysql', # Definido en el docker-compose en seccion posterior
    'user': 'root',
    'password': 'ejemplo',
    'database': 'mydatabase'
}

def store_data_db(data):
    try:
        # Conecta a la base de datos MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Inserta los datos en la tabla forms
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s);", (data,))

        # Realiza commit y cierra la conexion
        conn.commit()
        conn.close()
        log.info("Succesfully registered")
    except:
        log.warning("Could not insert in database %s (Database may not be ready): " %(data))
@app.route('/')
def index():
    # Esta funcion se asocia a la ruta raiz "/"
    return "Bienvenido a mi aplicacion web!"

@app.route('/formulario', methods=[ 'POST'])
def formulario():
    # Esta funcion se asocia a la ruta "/formulario"
    if request.method == 'POST':
        # Si se envia el formulario, procesamos los datos
        nombre = request.form['nombre']

        # Llama a la funcion para almacenar datos en la base de datos
        store_data_db(nombre)

        mensaje = f"Hola, {nombre}. Bienvenido a mi app web."
        return mensaje


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)