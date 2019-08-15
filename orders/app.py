import os

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from db import db
from resources.order import OrderResource

app = Flask(__name__)
api = Api(app)
migrate = Migrate()

app.secret_key = os.environ['SECRET_KEY']
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db)

api.add_resource(OrderResource, '/order')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run()
