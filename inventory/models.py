import json
import bson
from mongoengine import *
from mongoengine.base import BaseDocument
import mongoengine_goodjson as gj

connect("inventory", host='inventory_db', port=27017)

class Category(gj.EmbeddedDocument):
    name = StringField(required=True, max_length=200)

class Product(gj.Document):
    name = StringField(required=True, max_length=200)
    price = FloatField(required=True)
    quantity = IntField(required=True)
    category = EmbeddedDocumentField(Category)
