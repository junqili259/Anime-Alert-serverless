# Anime-Alert-api
This api returns the required data such as every show in the current seasonal slot back to the Anime-Alert application.


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

### Tools
[Fastapi](https://github.com/tiangolo/fastapi)
