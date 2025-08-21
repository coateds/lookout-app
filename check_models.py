# check_models.py
from website import create_app
from website.extensions import db

app = create_app()
with app.app_context():
    print("Tables registered in metadata:")
    for table_name in db.metadata.tables:
        print(f" - {table_name}")