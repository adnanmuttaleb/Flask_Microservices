
import json

from flask import abort
from flask import current_app, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_refresh_token_required

from .massengers import PikaMassenger
from .models import Product, Category


class ProductList(Resource):

    def __init__(self, *args, **kwargs):
        self.massenger_class = PikaMassenger
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, nullable=False)
        self.parser.add_argument('quantity', type=int, nullable=False)
        self.parser.add_argument('price', type=float, nullable=False)
        self.parser.add_argument('category', type=str,)

    
    @jwt_required
    def get(self):
        return json.loads(Product.objects.to_json())

    def post(self):
        args = self.parser.parse_args()
        new_product = Product(**args)
        new_product = new_product.save()
        
        with self.massenger_class() as mass:
            mass.send(
                massege=new_product.to_json(), 
                keys='product.created')
        
        return json.loads(new_product.to_json())


class ProductDetails(Resource):

    def __init__(self, *args, **kwargs):
        self.massenger_class = PikaMassenger
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, nullable=False)
        self.parser.add_argument('quantity', type=int, nullable=False)
        self.parser.add_argument('price', type=float, nullable=False)
        self.parser.add_argument('category', type=str,)

    
    @jwt_required
    def get(self, product_id):
        product = Product.objects(pk=product_id).first()
        if not product:
            abort(404)
        return json.loads(product.to_json())

    @jwt_required
    def put(self, product_id):
      
        product = Product.objects(pk=product_id).first()
        if not product:
            abort(404)
        
        args = self.parser.parse_args()
        product.update(**args)

        with self.massenger_class() as mass:
            mass.send(
                massege=product.to_json(), 
                keys='product.updated')
        
        return json.loads(product.to_json())
    
    @jwt_required
    def delete(self, product_id):
        
        product = Product.objects(pk=product_id).first()
        if not product:
            abort(404)
        
        product.delete()    
        with self.massenger_class() as mass:
            mass.send(
                massege=product.to_json(), 
                keys='product.deleted')
        
        return "", 204




