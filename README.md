# Anime-Alert
This app displays all shows of the current season. The selected show is added to your watchlist and notifications will be sent whenever a new episode is released.


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
