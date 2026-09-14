from flask import Flask, jsonify, request
app = Flask(__name__)
_next = 1
BOOKS = [{"id": 1, "title":"Clean Code", "author":"R. Martin"}]

def find(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)

@app.route("/books", methods = ["GET"])
def list_books():
    n = int(request.args.get("Limit", 100))
    return jsonify(BOOKS[:n]), 200

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

#Bài 6 mở rộng
@app.route("/books/search", methods = ["GET"])
def search_book():
    q = request.args.get('q')
    #return all books with q in author, title, id
    #or return 404 if nothing is found
    res = []
    for b in BOOKS:
        if b["id"] == q or b["title"] == q or b["author"] == q:
            #return jsonify(b), 200
            res.append(b)
    if len(res) > 0: return jsonify(res), 200
    return {"error":"nothing is found"},400

#Bài 6 mở rộng
@app.route("/books/sort",methods = ["GET"])
def sort_by():
    q = request.args.get('q')
    #if q is title, id, author, then sort and return
    #else return error invalid request?
    if q == "title" or q == "id" or q == "author":
        #sort ?
        sorted_books= sorted(BOOKS, key = lambda x: x[q])
        return jsonify(sorted_books), 200
    return {"error": "invalid request"}, 400 

if __name__ == "__main__":
    app.run(host = "localhost", port=5000, debug = True)