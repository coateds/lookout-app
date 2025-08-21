from flask import Blueprint, jsonify, current_app
from website import db
from sqlalchemy import text

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

@views.route("/db-check")
def db_check():
    try:
        result = db.session.execute(text("SELECT 1")).scalar()
        return jsonify({"db_status": "connected", "result": result})
    except Exception as e:
        return jsonify({"db_status": "error", "message": str(e)})
