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



def create_app(test_config=None):
    app = app = Flask(__name__,)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        JWT_SECRET_KEY=os.environ['JWT_SECRET_KEY'])
        
    app.config.from_pyfile('config.py',)

    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    jwt.init_app(app)


    from .views import UserDetails, UserList
    api.add_resource(UserDetails, '/users/<int:user_id>', endpoint='user_details')
    api.add_resource(UserList, '/users', endpoint='users_list')
    api.init_app(app)
    
    return app

