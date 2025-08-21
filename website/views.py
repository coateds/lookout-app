from flask import Blueprint, jsonify, current_app
from website import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

views = Blueprint('views', __name__)

@views.route('/')
def home():

    return "Welcome to the website!"

@views.route("/env")
def show_env_config():
    config = current_app.config
    masked = {
        k: ("*****" if "PASSWORD" in k else v)
        for k, v in config.items()
        if k in ["USER", "PASSWORD", "CONTAINER_SERVICE"]
    }
    return jsonify(masked)

# @views.route("/db-check")
# def db_check():
#     try:
#         result = db.session.execute(text("SELECT 1")).scalar()
#         return jsonify({"db_status": "connected", "result": result})
#     except Exception as e:
#         return jsonify({"db_status": "error", "message": str(e)})

@views.route("/db-check")
def db_check():
    try:
        # Basic connectivity check
        result = db.session.execute(text("SELECT 1")).scalar()

        # List all databases
        databases = db.session.execute(text("SELECT name FROM sys.databases")).fetchall()
        db_names = [row[0] for row in databases]

        # Check if 'lookout' exists and list its tables
        lookout_tables = []
        if "lookout" in db_names:
            # Switch context to lookout DB
            db.session.execute(text("USE lookout"))
            tables = db.session.execute(text("""
                SELECT TABLE_NAME FROM lookout.INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)).fetchall()
            lookout_tables = [row[0] for row in tables]

        return jsonify({
            "db_status": "connected",
            "result": result,
            "available_databases": db_names,
            "lookout_tables": lookout_tables
        })

    except SQLAlchemyError as e:
        return jsonify({
            "db_status": "error",
            "message": str(e)
        })

