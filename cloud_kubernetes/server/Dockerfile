# Establecemos la imagen base con Python
# De esta manera, evitamos tener que instalar manualmente Python.
FROM python:latest

# Establecemos el directorio de trabajo en el contenedor,
# es decir, a partir de ahora, trabajaremos sobre este directorio.
# Debemos considerar que esto hará un cambio de directorio.
WORKDIR /app

# Instalamos las dependencias de la aplicacion
# En este caso, solo necesitaremos Flask y el conector a MySQL.

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt


# Exponemos el puerto 5000 para Flask
# Esto no abre el puerto, simplemente es una forma de documentacion,
# Explica que el puerto está abierto.
EXPOSE 5000

# Finalmente, declaramos el comando a ejecutar por defecto al lanzar, el contenedor.
# Comando por defecto al ejecutar el contenedor
CMD ["python", "server.py"]