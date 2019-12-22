from flask import current_app, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, jwt_refresh_token_required, 
    set_access_cookies, set_refresh_cookies, 
    unset_jwt_cookies, get_raw_jwt, get_jwt_identity)


from .models import User, BlockedTokens
from . import db, marshmallow

class UserLogin(Resource):

    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)

    
    def post(self):
        args = self.parser.parse_args()
        email = args.get('email')
        password = args.get('password')
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User does not exist'})

        if user.verify_hash(password):
         
            access_token = create_access_token(identity=user.email) 
            refresh_token = create_refresh_token(identity=user.email)
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp

        else:
            return jsonify({'message': 'Wrong credentials'})


class UserRefreshLogin(Resource):

    @jwt_refresh_token_required    
    def post(self):

        user_identity = get_jwt_identity()
        access_token = create_access_token(identity=user_identity)
        
        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access_token)

        return resp


class UserLogout(Resource):
    
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']        
        blocked_token = BlockedTokens(jti=jti) 
        db.session.add(blocked_token)
        db.session.commit()

        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp
        



