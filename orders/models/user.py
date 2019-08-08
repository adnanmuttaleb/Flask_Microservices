from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(50), nullable=False)
    email = db.Column(db.VARCHAR(100), nullable=False)
    tags = db.relationship(
        'ProductModel',
        secondary='orders',
        lazy='subquery',
        backref=db.backref('tags', lazy=True)
    )

    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def find_user_by_id(cls, id_):
        return cls.query.filter_by(user_id=id_).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def jsonfy(self):
        return {
            'id': self.user_id,
            'name': self.name,
            'email': self.email
        }
