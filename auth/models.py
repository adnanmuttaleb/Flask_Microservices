
import json
from passlib.hash import pbkdf2_sha256 as sha256
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def verify_hash(self, password):
        return sha256.verify(password, self.password)

    def __repr__(self):
        return 'User(%r, %r)' % (self.id, self.email)

    @staticmethod
    def save_from_json(json_data):
        data = json.loads(json_data)
        cleaned_data = {}
        for col in User.__table__.columns:
            cleaned_data[col.name] = data[col.name]
            
        new_user = User(**cleaned_data)
        db.session.add(new_user)
        db.session.commit()
            
            
    @staticmethod
    def update_from_json(json_data):
        
        data = json.loads(json_data)
        user_id = data['id']
        user = User.query.filter_by(id=user_id).first()
        
        col_names = [col.name for col in User.__table__.columns]
        for attr, val in data.items():
            if attr in col_names:
                setattr(user, attr, val)
        
        db.session.commit()
    

    @staticmethod
    def delete_from_json(json_data):

        data = json.loads(json_data)
        user_id = data['id']
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        
    
            

class BlockedTokens(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(300))
