from flask import Flask, jsonify
import pyodbc
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from app.config import load_config

app = Flask(__name__)

print("start main.py")

# load_dotenv()

# Map GitHub Secrets to expected env vars
# os.environ["SQL_SERVER_USER"] = os.getenv("SQL_SERVER_USER_CODESPACES", "")
# os.environ["SQL_SERVER_PASSWORD"] = os.getenv("SQL_SERVER_PASSWORD_CODESPACES", "")


config = load_config()
print(config)

SQL_SERVER = config["CONTAINER_SERVICE"]
SQL_USERNAME = config["USER"]
SQL_PASSWORD = config["PASSWORD"]

#Debug
print("👤 SQL_SERVER_USER =", SQL_USERNAME)
print("🔑 SQL_SERVER_PASSWORD =", SQL_PASSWORD)
#

# Update these values to match your SQL Server setup
# SQL_SERVER = "sqlserver"
# SQL_SERVER = os.getenv("SQL_SERVER_CONTAINER_SERVICE", "sqlserver")
SQL_DATABASE = "master"
# SQL_USERNAME = os.getenv("SQL_SERVER_USER")
# SQL_PASSWORD = os.getenv("SQL_SERVER_PASSWORD")
DRIVER = "ODBC Driver 18 for SQL Server"

print("🔍 SQL_SERVER_CONTAINER_SERVICE =", repr(SQL_SERVER))

# pyODBC connection string
odbc_conn_str = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USERNAME};"
    f"PWD={SQL_PASSWORD};"
    f"TrustServerCertificate=yes;"
)

@app.route("/ping")
def ping():
    try:
        conn = pyodbc.connect(odbc_conn_str, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases")
        databases = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jsonify({"status": "ok", "databases": databases})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/home")
def home():
    return "Welcome to the SQL Server API!!!??###&&&"

# @app.route("/config")
# def config_view():
#     return {
#         "ENV": os.getenv("ENV"),
#         "USER": config["USER"],
#         "PASSWORD": config["PASSWORD"],
#         "CONTAINER_SERVICE": config["CONTAINER_SERVICE"]
#     }

@app.route("/config")
def get_config():
    import os

    env = os.getenv("ENV")

    config = {}

    if env == "codespaces":
        config["USER"] = os.getenv("SQL_SERVER_USER_CODESPACES")
        config["PASSWORD"] = os.getenv("SQL_SERVER_PASSWORD_CODESPACES")
        config["CONTAINER_SERVICE"] = os.getenv("SQL_SERVER_CONTAINER_SERVICE_CODESPACES", "sqlserver")
    else:
        config["USER"] = os.getenv("SQL_SERVER_USER")
        config["PASSWORD"] = os.getenv("SQL_SERVER_PASSWORD")
        config["CONTAINER_SERVICE"] = os.getenv("SQL_SERVER_CONTAINER_SERVICE", "sqlserver")

    config["ENV"] = env

    return config

@app.route("/db-status")
def db_status():
    try:
        conn = pyodbc.connect(odbc_conn_str, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        return {"status": "connected", "result": result[0]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

