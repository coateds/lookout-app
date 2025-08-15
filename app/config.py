import os

def load_config():
    env = os.getenv("ENV", "local")

    if env == "codespaces":
        return {
            "USER": os.getenv("SQL_SERVER_USER_CODESPACES"),
            "PASSWORD": os.getenv("SQL_SERVER_PASSWORD_CODESPACES"),
            "CONTAINER_SERVICE": os.getenv("SQL_SERVER_CONTAINER_SERVICE_CODESPACES"),
        }
    elif env == "local":
        return {
            "USER": os.getenv("SQL_SERVER_USER_LOCAL", "sa"),
            "PASSWORD": os.getenv("SQL_SERVER_PASSWORD_LOCAL", "yourStrong(!)Password"),
            "CONTAINER_SERVICE": os.getenv("SQL_SERVER_CONTAINER_SERVICE_LOCAL", "localhost"),
        }
    else:
        raise ValueError(f"Unknown ENV: {env}")