from flask import Blueprint, jsonify, current_app, render_template
from website import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

views = Blueprint('views', __name__)

@views.route('/')
def home():

    # return "Welcome to the website!"
    return render_template("home.html")

@views.route('/about')
def about():
    # destroyed_since = 1
    
    # kari_visited = (db.session.query(Destination)
    #     .filter(Destination.kari_visited ==1)).count()
    # dave_visited = (db.session.query(Destination)
    #     .filter(Destination.dave_visited ==1)).count()
    # kari_visited_lo = (db.session.query(Destination)
    #     .filter(Destination.kari_visited ==1)
    #     .filter(Destination.has_fire_lookout_structure == 1)).count() + destroyed_since
    # dave_visited_lo = (db.session.query(Destination)
    #     .filter(Destination.dave_visited ==1)
    #     .filter(Destination.has_fire_lookout_structure == 1)).count() + destroyed_since

    return render_template(
        "about.html", 
        # kari_visited=kari_visited, 
        # dave_visited=dave_visited,
        # kari_visited_lo=kari_visited_lo,
        # dave_visited_lo=dave_visited_lo
    )

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

