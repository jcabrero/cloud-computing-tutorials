Build `docker` image:
```bash
docker build -t cc/mi-servidor-flask:latest .
```


Run `docker` image:


```bash
docker run -it --rm -p 8000:5000 cc/mi-servidor-flask:latest
```