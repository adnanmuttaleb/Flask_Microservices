import os 

from flask import Flask 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = app = Flask(__name__,)
    app.config.from_mapping(SECRET_KEY=os.environ['SECRET_KEY'])
    app.config.from_pyfile('config.py',)

    db.init_app(app)
    migrate.init_app(app, db)

    return app



if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port='5000')