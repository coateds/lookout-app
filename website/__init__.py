from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from .views import views
from .env_config import load_env_config
from sqlalchemy import create_engine, text
from . import models
from .extensions import db, migrate


def ensure_database_exists(uri, db_name):
    master_uri = uri.replace(f"/{db_name}", "/master")
    engine = create_engine(master_uri, isolation_level="AUTOCOMMIT")  # 👈 key fix
    with engine.connect() as conn:
        exists = conn.execute(text(f"SELECT name FROM sys.databases WHERE name = '{db_name}'")).scalar()
        if not exists:
            conn.execute(text(f"CREATE DATABASE {db_name}"))

# db = SQLAlchemy()
# migrate = Migrate()

# config = load_env_config()

def create_app(config_override=None):
    app = Flask(__name__)

    config = load_env_config()

    if config_override:
        config.update(config_override)

    app.config.update(config)

    # Build the "lookout" database if it doesn't exist
    ensure_database_exists(app.config["SQLALCHEMY_DATABASE_URI"], "lookout")

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import User, Event

    from .views import views
    app.register_blueprint(views)

    print("Tables")
    print(db.Model.metadata.tables)

    return app