from marshmallow import fields, Schema, validate

class ProductOut(Schema):
    id = fields.Int()
    sku = fields.Str()
    name = fields.Str()
    descprition = fields.Str(allow_none= True)
    price_cents = fields.Int()
    qty_in_stock = fields.Int()
    archived = fields.Bool()

class ProductIn(Schema):
    sku = fields.Str(required=True, 
                     validate= validate.Length(min=3, max= 32))
    name = fields.Str(required=True,
                      validate=validate.Length(min = 1,max=255))
    qty_in_stock = fields.Int(load_default=0,
                              validate=validate.Range(min=0))

class ProductPatch(Schema):
    name = fields.Str()
    price_cents = fields.Int(validate=validate.Range(min=0))
class ReserveIn(Schema):
    qty = fields.Int(required=True, 
                     validate=validate.Range(min=1))

class OrderItemIn(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True,
                            validate=validate.Range(min=1))

class OrderItemOut(Schema):
    id  =fields.Int()
    order_id = fields.Int()
    product_id = fields.Int()
    quantity = fields.Int()

class OrderIn(Schema):
    status = fields.String(required= True, allow_none=True)
    items = fields.List(
        fields.Nested(OrderItemIn),
        required=True,
        validate=validate.Length(min=1)
    )

class OrderOut(Schema):
    id = fields.Int()
    status = fields.Str(allow_none=True)
    items = fields.List(
        fields.Nested(OrderItemOut)

    )

