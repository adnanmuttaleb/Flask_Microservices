from flask_restful import Resource, reqparse

from models.user import UserModel


class UserResource(Resource):
    def get(self):
        return {
            'users': [{
                'id': user.user_id,
                'name': user.name,
                'email': user.email,
            }
                for user in UserModel.get_all_users()]
        }

    def post(self):
        data = self.__user_parser()
        user = UserModel(data['name'], data['email'])
        user.save_to_db()
        return {'message': 'User created successfully!', 'user': user.jsonfy()}

    # def delete(self):
    #     # This is for dummy testing i made
    #     from models.product import ProductModel
    #     from models.order import OrderModel
    #
    #     product = ProductModel('Pen', True)
    #     user = UserModel('Adnnan', 'Ad@email.com')
    #     order = OrderModel(user, product, 1)
    #     user.save_to_db()
    #     product.save_to_db()
    #     order.save_to_db()

    def __user_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name',
            type=str,
            required=True,
            help='name shoud be provided.'
        )

        parser.add_argument(
            'email',
            type=str,
            required=True,
            help='email shoud be provided.'
        )

        return parser.parse_args()
