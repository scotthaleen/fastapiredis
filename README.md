

# Sample FastAPI


[FastAPI](https://fastapi.tiangolo.com/)
[Poetry](https://python-poetry.org/)

### Install
```
poetry install
```

**Add new dependency**
```
poetry add <dependency>
```

### Format + Lint
```
poetry run format
poetry run lint
```

### Coverage
```
poetry run coverage
```

### Run Dev
```
poetry run dev
```

or

```
uvicorn app.main:api --reload --log-config logging.yaml
```




Run local redis with docker

```
docker run --rm --name some-redis -p 6379:6379 -d redis
```



TODO

- [ ] cookiecutter
