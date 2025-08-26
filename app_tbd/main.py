from flask import Flask, jsonify
import pyodbc
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import time
from app.config import load_config

# Wait for .env to be ready
while not os.path.exists("/workspaces/lookout-app/.env.ready"):
    print("Waiting for .env to be ready...")
    time.sleep(1)


app = Flask(__name__)

config = load_config()

# pulled from .env locally or from GH secrets in Codespaces
SQL_SERVER = config["CONTAINER_SERVICE"]
SQL_USERNAME = config["USER"]
SQL_PASSWORD = config["PASSWORD"]

# Constants for database connection
SQL_DATABASE = "master"
DRIVER = "ODBC Driver 18 for SQL Server"

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

@app.route("/config")
def config_view(): 
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

