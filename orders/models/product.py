from db import db


class ProductModel(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_product_by_id(cls, id_):
        return cls.query.filter_by(product_id=id_).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
