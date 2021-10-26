from .extensions import db

class Student(db.Model):
    rollno = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    mobile = db.Column(db.String(10), unique=True, nullable=False)
    math_marks = db.Column(db.Integer())
    science_marks = db.Column(db.Integer())
    english_marks = db.Column(db.Integer())
