from flask import Flask, jsonify
import pyodbc
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from app.config import load_config

app = Flask(__name__)

load_dotenv()

# Update these values to match your SQL Server setup
# SQL_SERVER = "sqlserver"
SQL_SERVER = os.getenv("SQL_SERVER_CONTAINER_SERVICE", "sqlserver")
SQL_DATABASE = "master"
SQL_USERNAME = os.getenv("SQL_SERVER_USER")
SQL_PASSWORD = os.getenv("SQL_SERVER_PASSWORD")
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

