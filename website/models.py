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

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    organizer_name = db.Column(db.String(50), nullable=False)
    organizer_contact = db.Column(db.String(50))
    start_location = db.Column(db.String(50))
    comments = db.Column(db.String(None))
    pin = db.Column(db.String(50))
    signups = db.relationship('Signup', backref='event', lazy=True)