from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    recipients = db.relationship('Recipient', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)
    messages = db.relationship('Message', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    relationship = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))
    avatar = db.Column(db.String(200))

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'relationship': self.relationship,
            'email': self.email,
            'address': self.address,
            'avatar': self.avatar
        }


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    date = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String(200))
    template = db.Column(db.Text)
    recipients = db.Column(db.Text)  # Comma-separated recipient IDs


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    schedule_time = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    recipients = db.Column(db.Text)  # Comma-separated recipient IDs
