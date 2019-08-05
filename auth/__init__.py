import os 

from flask import Flask 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()
api = Api()
marshmallow = Marshmallow()
jwt  = JWTManager()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']

    from .models import BlockedTokens
    if BlockedTokens.query.filter_by(jti=jti).first():
        return True
    
    return False 


def create_app(test_config=None):
    app = app = Flask(__name__,)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'], 
        JWT_SECRET_KEY=os.environ['JWT_SECRET_KEY'])

    app.config.from_pyfile('config.py',)

    from .models import User, BlockedTokens

    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    jwt.init_app(app)

    from .views import UserLogin, UserLogout, UserRefreshLogin
   
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(UserRefreshLogin, '/refresh')
    api.init_app(app)
    
    return app


