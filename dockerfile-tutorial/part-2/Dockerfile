# Etapa 1: Construcción:
# En esta fase, utilizaremos la imagen de Golang,
# para construir y producir el ejecutable.
FROM golang:1.16 as builder
# Utilizamos el directorio de trabajo /app
WORKDIR /app
# Inicializamos el repositorio
RUN go mod init example.com/greetings
# Copiamos main.go desde nuestro host
COPY main.go .
# Compilamos go en el archivo app
RUN CGO_ENABLED=0 GOOS=linux go build -o app

# Etapa 2: Imagen mínima
# Partiremos de scratch, una imagen que no utiliza ningún recurso previo
FROM scratch
# Copiaremos desde la imagen builder, creada anteriormente, el ejecutable
COPY --from=builder /app/app /
# Por ultimo, definiremos el comandoa ejecutar como /app
CMD ["/app"]