import os 

from flask import Flask 
from flask_jwt_extended import JWTManager
from flask_restful import Api

jwt  = JWTManager()
api = Api()

def create_app(test_config=None):
    app = app = Flask(__name__,)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        JWT_SECRET_KEY=os.environ['JWT_SECRET_KEY'])
        
    app.config.from_pyfile('config.py',)

    jwt.init_app(app)
    
    from .views import ProductDetails, ProductList
    api.add_resource(ProductList, '/products')
    api.add_resource(ProductDetails, '/products/<product_id>')

    api.init_app(app)
    
    return app

