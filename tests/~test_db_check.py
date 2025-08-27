import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from website import create_app
from website.extensions import db

def test_db_check_logic():
    app = create_app({"TESTING": True})
    with app.app_context():
        try:
            # Basic connectivity check
            result = db.session.execute(text("SELECT 1")).scalar()
            assert result == 1

            # List all databases
            databases = db.session.execute(text("SELECT name FROM sys.databases")).fetchall()
            db_names = [row[0] for row in databases]
            assert "lookout" in db_names

            # Switch to lookout DB and list tables
            db.session.execute(text("USE lookout"))
            tables = db.session.execute(text("""
                SELECT TABLE_NAME FROM lookout.INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)).fetchall()
            lookout_tables = [row[0] for row in tables]

            # Assertions
            assert len(lookout_tables) > 0, "No tables found in 'lookout' database"
            assert "alembic_version" in lookout_tables, "'alembic_version' table missing"

        except SQLAlchemyError as e:
            assert False, f"DB check failed: {str(e)}"