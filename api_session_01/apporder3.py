from flask import Flask, jsonify, request, make_response
app = Flask(__name__)

@app.route("/orders", methods=["GET"])
def list_orders():
    cursor = request.args.get("cursor")
    status = request.args.get("status")
    customer_id = request.args.get("customer_id")
    limit = request.args.get("limit", default=20, type=int)
    sort = request.args.get("sort")
    fields = request.args.get("fields")
    fields_arr = []
    if fields:
        fields_arr = fields.split(",")

    