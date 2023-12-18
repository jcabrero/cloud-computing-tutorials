FROM golang:1.16 as builder
WORKDIR /app
RUN go mod init example.com/greetings
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o app

# Etapa 2: Imagen final
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/app .
CMD ["./app"]