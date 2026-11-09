from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    price = fields.Float()

class ProductInSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)