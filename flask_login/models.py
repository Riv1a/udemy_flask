from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

def to_json(self):
    return {
        "id" : self.id,
        "username" : self.username,
        "email" : self.email
    }