# Anime-Alert-api

### About
This api returns the required data such as every show in the current seasonal slot back to the [Anime-Alert](https://github.com/junqili259/Anime-Alert) application. 


## Run API locally
### Uvicorn
```
cd api
uvicorn main:app
```

### For hot reloads
```
uvicorn main:app --reload
```

### Docker

```
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
```

### Api docs
Open your browser to http://http://127.0.0.1:8000/docs while running the api

### Tools
[Fastapi](https://github.com/tiangolo/fastapi)
