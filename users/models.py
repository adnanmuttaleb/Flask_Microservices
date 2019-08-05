

from passlib.hash import pbkdf2_sha256 as sha256
from users import db
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    def __repr__(self):
        return 'User(%r, %r)' % (self.email, self.username)

