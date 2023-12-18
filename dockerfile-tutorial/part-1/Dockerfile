# Establecemos la imagen base con Python
# De esta manera, evitamos tener que instalar manualmente Python.
FROM python:latest

# Establecemos el directorio de trabajo en el contenedor,
# es decir, a partir de ahora, trabajaremos sobre este directorio.
# Debemos considerar que esto hará un cambio de directorio.
WORKDIR /app

# Instalamos las dependencias de la aplicacion
# En este caso, solo necesitaremos Flask. 
## Si fuera necesario, podríamos copiar requirements.txt, 
## y utilizarlo para instalar dependencias.
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
RUN pip install Flask

# Copiamos el codigo fuente de la aplicacion al contenedor
# Esto incluye tanto el archivo app.py como formulario.html
COPY app/ app/

# Exponemos el puerto 5000 para Flask
# Esto no abre el puerto, simplemente es una forma de documentacion,
# Explica que el puerto está abierto.
EXPOSE 5000

# Finalmente, declaramos el comando a ejecutar por defecto al lanzar, el contenedor.
# Comando por defecto al ejecutar el contenedor
CMD ["python", "app/app.py"]