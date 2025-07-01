from app import db

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50),nullable=False)
    day = db.Column(db.String(20),nullable=False)

class Assignment(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.String(50),nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(50),nullable=False)
    location = db.Column(db.String(100), nullable=False)

class StudyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50),nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False) #in Minutes