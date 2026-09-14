from flask import Flask, jsonify, request
app = Flask(__name__)
_next = 1
BOOKS = [{"id": 1, "title":"Clean Code", "author":"R. Martin"},
         
         ]

def find(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)

@app.route("/books", methods = ["GET"])
def list_books():
    query = request.args.get("q")
    sort_by = request.args.get("sort")
    res = []
    if query :
        
        for b in BOOKS:
            if b["id"] == q or b["title"] == q or b["author"] == q:
            
                res.append(b)
        #if len(res) > 0: return jsonify(res), 200
        return {"error":"not found"},404

    if sort_by:
        q = request.args.get('sort')
        if q == "title" or q == "id" or q == "author":
                
            sorted_books = sorted(res, key = lambda x: x[q])
            return jsonify(sorted_books), 200
        return {"error": "invalid request"}, 422 
    res = BOOKS
    n = int(request.args.get("Limit", 100))
    return jsonify(res[:n]), 200


@app.route("/books/<int:bid>" , methods = ["GET"])
def get_book(bid):
    book = find(bid)
    if not book: return {"error":"not found"},404
    return jsonify(book),200

@app.route("/books", methods = ["POST"])
def create_book():
    global _next
    body = request.get_json(silent = True) or {}
    t , a = body.get("title"), body.get("author")
    if not t or not a:
        return {"error":"need title + author"},400

    book = {"id":_next, "title":t, "author":a}
    _next += 1
    BOOKS.append(book)
    return jsonify(book), 201, {"Locations:" : f"/books/{book['id']}"}

@app.route("/books/<int:bid>", methods = ["PUT", "DELETE"])
def modify_book(bid):
    book = find(bid)
    if not book : return {"error":"not found"}, 404
    if request.method == "PUT":
        book.update(request.get_json(silent=True) or {})
        return jsonify(book), 200
    BOOKS.remove(book)
    return "", 204

if __name__ == "__main__":
    app.run(host = "localhost", port=5000, debug = True)