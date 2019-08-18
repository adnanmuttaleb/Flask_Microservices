
import json

from flask import current_app, jsonify
from flask_restful import Resource, reqparse
from flask_marshmallow import Marshmallow
from flask_jwt_extended import jwt_required, jwt_refresh_token_required

from .massengers import PikaMassenger
from .models import User
from users import db, marshmallow


class UserSchema(marshmallow.ModelSchema):
    class Meta:
        model = User

user_schema = UserSchema()

class UserList(Resource):

    def __init__(self, *args, **kwargs):
        self.massenger_class = PikaMassenger
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, nullable=False)
        self.parser.add_argument('username', type=str, nullable=False)
        self.parser.add_argument('password', type=str, nullable=False)

    @jwt_required
    def get(self):
        users = User.query.all()
        return jsonify(user_schema.dump(users, many=True).data)

    def post(self):
        args = self.parser.parse_args()
        email = args.get('email')
        username = args.get('username')
        password = args.get('password')
        
        user = User(email=email, username=username, password=User.generate_hash(password))
        db.session.add(user)
        db.session.commit()

       
        with self.massenger_class() as mass:
            mass.send(
                massege=json.dumps(user_schema.dump(user).data), 
                keys='user.created')
        
        return jsonify(user_schema.dump(user).data)


class UserDetails(Resource):

    def __init__(self, *args, **kwargs):
        self.massenger_class = PikaMassenger
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)

    
    @jwt_required
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first_or_404()
        return jsonify(user_schema.dump(user).data)

    @jwt_required
    def put(self, user_id):
        user =  User.query.filter_by(id=user_id).first_or_404()
        args = self.parser.parse_args()

        user.email = args.get('email', user.email)
        user.username = args.get('username', user.username)
        user.password = User.generate_hash(args['password']) if args['password'] else user.password

        db.session.commit()

        with self.massenger_class() as mass:
            mass.send(
                massege=json.dumps(user_schema.dump(user).data), 
                keys='user.updated')
        
        return jsonify(user_schema.dump(user).data)
    
    @jwt_required
    def delete(self, user_id):
        user =  User.query.filter_by(id=user_id).first_or_404()
        db.session.delete(user)
        db.session.commit()

        with self.massenger_class() as mass:
            mass.send(
                massege=json.dumps(user_schema.dump(user).data), 
                keys='user.deleted')
        
        return "", 204




