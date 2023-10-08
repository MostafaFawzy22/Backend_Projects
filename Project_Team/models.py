# models.py

from app import db

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    bio = db.Column(db.Text)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20),  default='photos/default.png')
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User('{self.full_name}', '{self.email}', '{self.bio}', '{self.image_file})"

    def is_active(self):
        return True  # Assuming all users are active

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    type_video = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String(20),  default='photos/default.png')
    def __repr__(self):
        return f"Video('{self.name}', '{self.type_video}', '{self.image_file})"
    
class Video_Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_video = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String(20),  default='photos/default.png')

    def __repr__(self):
        return f"Video_Name('{self.type_video}', '{self.image_file})"
#     videos = db.relationship('Video', backref='video_name', lazy=True)
    