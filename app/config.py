import os
from dotenv import load_dotenv

def get_env(var_name, default=None):
    value = os.getenv(var_name)
    return value if value else default

def load_config():
    env = os.getenv("ENV", "local").lower()

    print("ENV in load_config = " + env)

    # Load .env only for local dev
    # if env == "local":
    load_dotenv()

    config = {}

    if env == "codespaces":


        # config["USER"] = get_env("SQL_SERVER_USER_CODESPACES")
        # config["PASSWORD"] = get_env("SQL_SERVER_PASSWORD_CODESPACES")
        config["CONTAINER_SERVICE"] = get_env("SQL_SERVER_CONTAINER_SERVICE_CODESPACES", "sqlserver")
        config["USER"] = os.getenv("SQL_SERVER_USER_CODESPACES")
        config["PASSWORD"] = os.getenv("SQL_SERVER_PASSWORD_CODESPACES")



    elif env == "local":
        print("Loading local config...")

        config["USER"] = get_env("SQL_SERVER_USER")
        config["PASSWORD"] = get_env("SQL_SERVER_PASSWORD")
        config["CONTAINER_SERVICE"] = get_env("SQL_SERVER_CONTAINER_SERVICE")

        print(config)
    else:
        raise ValueError(f"Unknown ENV: {env}")
    
    return config
