from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.user import UserModel
from models.product import ProductModel
from models.order import OrderModel

from dateutil.parser import parse


class OrderResource(Resource):
    @jwt_required
    def get(self):
        data = self.__get_order_query_string()
        user_id = data['user_id']
        product_id = data['product_id']
        order_date = data['order_date']

        if order_date:
            try:
                order_date = parse(order_date)
            except:
                return {'message': 'date time is not correct'}, 400

        orders = OrderModel.find_order_by(user_id, product_id, order_date)
        return {
            'order(s)': [
                {
                    'order_id': order.id,
                    'user_id': order.user_id,
                    'product_id': order.product_id,
                    'order_date': str(order.order_date)
                }
                for order in orders
            ],
        }

    @jwt_required
    def post(self):
        data = self.__post_order_parser()

        user = UserModel.find_user_by_id(data['user_id'])
        if not user:
            return {'message': 'This user doesnt exist'}, 404

        product = ProductModel.find_product_by_id(data['product_id'])
        if not product:
            return {'message': 'This product doesnt exist'}, 404

        order = OrderModel(user, product, data['quantity'])
        order.save_to_db()
        return {
                   'order': {
                       'id': order.id,
                       'quantity': order.quantity,
                       'user': {
                           'id': user.user_id,
                           'name': user.name
                       },
                       'product': {
                           'id': product.product_id,
                           'name': product.name
                       }
                   }
               }, 200

    def __post_order_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'user_id',
            type=int,
            help='user_id must be entered.',
            required=True
        )

        parser.add_argument(
            'product_id',
            type=int,
            help='product_id must be entered.',
            required=True
        )

        parser.add_argument(
            'quantity',
            type=int,
            help='quantity must be entered.',
            required=True
        )

        return parser.parse_args()

    def __get_order_query_string(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'user_id',
            type=int,
        )

        parser.add_argument(
            'product_id',
            type=int,
        )

        parser.add_argument(
            'order_date',
            type=str,
        )
        return parser.parse_args()
