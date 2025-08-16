# Authentication per Environment

## Local

files:
root
- .env
- docker-compose.yml
- .devcontainer/devcontainer.json
- app/main.py
- app/config.py

.env file
```
SQL_SERVER_USER=sa
SQL_SERVER_PASSWORD=YourStrong!Passw0rd
SQL_SERVER_CONTAINER_SERVICE=sqlserver
```

docker-compose.yml
```yml
services:
  flask-app:
    build:
      context: .
      dockerfile: .devcontainer/Dockerfile

    volumes:
      - .:/workspaces/lookout-app
      - .:/app
      - ./.env:/app/.env  # 👈 Mount .env file

    ports:
      - "5000:5000"
    depends_on:
      - sqlserver
    command: python3 -m flask run --host=0.0.0.0 --port=5000

    environment:
      - FLASK_ENV=development
      - FLASK_APP=app.main
      - FLASK_DEBUG=1

    working_dir: /app

    sqlserver:
    .
    .
    .
```

devcontainer.json
```json
{
  "name": "Lookout Dev Container",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
"containerEnv": {
  "ENV": "codespaces",
  "PYTHONPATH": "/workspaces/lookout-app"
},
"features": {
  "ghcr.io/devcontainers/features/github-secrets:1": {
    "secrets": [
      "SQL_SERVER_USER_CODESPACES",
      "SQL_SERVER_PASSWORD_CODESPACES",
      "SQL_SERVER_CONTAINER_SERVICE_CODESPACES"
    ]
  }
},
.
.
.
```

main.py
```python
config = load_config()

SQL_SERVER = config["CONTAINER_SERVICE"]
SQL_USERNAME = config["USER"]
SQL_PASSWORD = config["PASSWORD"]

# pyODBC connection string
odbc_conn_str = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USERNAME};"
    f"PWD={SQL_PASSWORD};"
    f"TrustServerCertificate=yes;"
```

config.py
```python
def get_env(var_name, default=None):
    value = os.getenv(var_name)
    return value if value else default

def load_config():
    env = os.getenv("ENV", "local").lower()

    load_dotenv()

    config = {}

    if env == "codespaces":
        pass

    elif env == "local":
        print("Loading local config...")

        config["USER"] = get_env("SQL_SERVER_USER")
        config["PASSWORD"] = get_env("SQL_SERVER_PASSWORD")
        config["CONTAINER_SERVICE"] = get_env("SQL_SERVER_CONTAINER_SERVICE")

        print(config)
    else:
        raise ValueError(f"Unknown ENV: {env}")
    
    return config
```