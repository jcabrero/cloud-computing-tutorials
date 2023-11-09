# Establecemos la imagen base con Python
# De esta manera, evitamos tener que instalar manualmente Python.
FROM python:latest

# Establecemos el directorio de trabajo en el contenedor,
# es decir, a partir de ahora, trabajaremos sobre este directorio.
# Debemos considerar que esto hará un cambio de directorio.
WORKDIR /app

# Instalamos las dependencias de la aplicacion
# En este caso, solo necesitaremos Flask y el conector a MySQL.
RUN pip install requests


# Copiamos el codigo fuente de la aplicacion al contenedor
# Esto incluye tanto el archivo app.py como formulario.html
COPY client.py app/

# Finalmente, declaramos el comando a ejecutar por defecto al lanzar, el contenedor.
# Comando por defecto al ejecutar el contenedor
CMD ["python", "app/client.py"]