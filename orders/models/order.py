from datetime import datetime
from db import db


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)

    user = db.relationship('UserModel', backref=db.backref("orders"))
    product = db.relationship('ProductModel', backref=db.backref("orders"))

    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, user, product, quantity):
        self.user = user
        self.product = product
        self.quantity = quantity

    @classmethod
    def find_order_by(cls, user_id=None, product_id=None, order_date=None):
        query = cls.query
        if not user_id and not product_id and not order_date:
            return cls.query.all()

        if user_id:
            query = query.filter_by(user_id=user_id)
        if product_id:
            query = query.filter_by(product_id=product_id)
        if order_date:
            from dateutil.relativedelta import relativedelta
            query = query.filter(order_date.date() <= OrderModel.order_date).filter(
                OrderModel.order_date < order_date.date() + relativedelta(days=+1))

        return query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
