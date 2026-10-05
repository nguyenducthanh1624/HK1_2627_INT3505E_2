from flask import Flask, request, make_response, jsonify, g
import sqlite3
app = Flask(__name__)

ORDERDB = "orders.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #print("aaaaaaaaaaaaaaa")
        db = g._database = sqlite3.connect(ORDERDB)
    db.row_factory = sqlite3.Row
    return db

@app.get("/orders")
def list_orders():
    limit = int(request.args.get("limit", 5))
    cursor = request.args.get("cursor", type=int)

    status = request.args.get("status")
    customer_id = request.args.get("customerId", type=int)

    fields = request.args.get("fields", "*")
    
    args = []

    query = f"""
        SELECT {fields} FROM orders WHERE 1=1
"""
    if status:
        args.append(status)
        query += " AND status = ? "

    if customer_id is not None:
        args.append(customer_id)
        query += " AND customerId = ? "

    conn = get_db()

    if cursor is not None:
        args.append(cursor)
        query += " AND orderId > ? "

    args.append(limit)
    query+= " ORDER BY orderId LIMIT ? "

    orders = conn.execute(query, args).fetchall()

    next_cursor = orders[-1]["orderId"] if orders else None
    conn.close()
    return make_response(jsonify({
        "data": [dict(order) for order in orders],
        "next_cursor": next_cursor
        }), 200)




if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000, debug = True)

    
    