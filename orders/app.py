import os

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from resources.order import OrderResource

app = Flask(__name__)
api = Api(app)
jwt = JWTManager()
migrate = Migrate()

app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

api.add_resource(OrderResource, '/order')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run()
