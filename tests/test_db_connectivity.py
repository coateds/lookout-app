import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from alembic.config import Config
# from alembic import command
from sqlalchemy import create_engine, text
from website import create_app
# from website.models import User  # adjust path if needed
# from website.extensions import db  # if you’ve modularized db setup
# import os


# def test_user_table_access():
#     app = create_app({"TESTING": True})  # no URI override

#     with app.app_context():
#         # Confirm we're using SQL Server
#         print("Using DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

#         # Patch Alembic config to use the same URI
#         alembic_cfg = Config()
#         alembic_cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), "..", "migrations"))
#         alembic_cfg.set_main_option("sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"])
#         command.upgrade(alembic_cfg, "head")

#         # Now query the User table
#         count = db.session.query(User).count()
#         assert count >= 0

def test_sql_server_connection_and_db_exists():
    app = create_app({"TESTING": True})
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    db_name = "lookout"

    # Connect to master DB
    master_uri = uri.replace(f"/{db_name}", "/master")
    engine = create_engine(master_uri, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT name FROM sys.databases WHERE name = '{db_name}'")).scalar()
        assert result == db_name, f"Database '{db_name}' not found in sys.databases"
