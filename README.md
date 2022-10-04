# Document-Uploader
### Setup do projeto
```
virtualenv .venv -p python3.10
pip install -r requirements.txt
docker-compose up
```

### Start projeto
- Criar adm
```
python src/presentation/main.py adm \
    create
    <senha>
    <email>
    <nome>
```
- Iniciar api
```
python src/presentation/main.py api
```