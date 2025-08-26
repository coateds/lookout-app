import os
from dotenv import load_dotenv, find_dotenv

def get_env(var_name, default=None):
    value = os.getenv(var_name)
    return value if value else default

def load_env_config():
    env = os.getenv("ENV", "local").lower()

    # Load .env if present
    load_dotenv(find_dotenv())

    config = {}

    if env == "codespaces":
        config["CONTAINER_SERVICE"] = os.getenv("SQL_SERVER_CONTAINER_SERVICE")
        config["USER"] = os.getenv("SQL_SERVER_USER")
        config["PASSWORD"] = os.getenv("SQL_SERVER_PASSWORD")

    elif env == "local":
    # elif env in ["local", "ci"]:
        config["USER"] = get_env("SQL_SERVER_USER")
        config["PASSWORD"] = get_env("SQL_SERVER_PASSWORD")
        config["CONTAINER_SERVICE"] = get_env("SQL_SERVER_CONTAINER_SERVICE")

    else:
        raise ValueError(f"Unknown ENV: {env}")    

    # db_name = "master"
    db_name = "lookout"
    user = config["USER"]
    password = config["PASSWORD"]
    host = config["CONTAINER_SERVICE"]

    config["SQLALCHEMY_DATABASE_URI"] = (
        f"mssql+pyodbc://{user}:{password}@{host}:1433/{db_name}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&Encrypt=yes"
        "&TrustServerCertificate=yes"
    )
    config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return config