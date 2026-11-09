from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from flask import Flask, request, make_response, jsonify, g
from .schemas import ProductInSchema, ProductSchema
import sqlite3
app = Flask(__name__)
blp = Blueprint("products", __name__, url_prefix="/products")

PRODUCTS = []
_next_id = 1

@blp.route("/")
class ProductList(MethodView):

    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """return jsonify({
        "data" : PRODUCTS,
        "total":len(PRODUCTS)
        }), 200"""
        return PRODUCTS

    @blp.arguments(ProductInSchema) # validate POST body
    @blp.response(201, ProductSchema)
    def post(self, data):
        global _next_id
        
        
        t = data["name"]
        a = data["price"]
        if not t or not a:
            #return jsonify(error = "name and price required"), 422
            abort(422, message = "name and price required")
    
        product = {"id" : _next_id, "name": t, "price":a}
        PRODUCTS.append(product); _next_id+=1

        """resp = make_response(jsonify(product),201)
        resp.headers["Locations"] = f"/products/{product['id']}"
        return resp"""
        return product, {
            "Location": f"/products/{product['id']}"
        }
    
