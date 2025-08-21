from .extensions import db


# class User(db.Model, UserMixin):
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    description = db.Column(db.String(1024))
    website = db.Column(db.String(255))
    fb_username = db.Column(db.String(100))
    fb_user_id = db.Column(db.String(100))