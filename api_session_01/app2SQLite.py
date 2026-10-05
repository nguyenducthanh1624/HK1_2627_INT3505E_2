from flask import Flask, request, make_response, jsonify, g
import sqlite3
app = Flask(__name__)
BOOKS = []
_next_id = 1

DEFAULT_SIZE, MAX_SIZE = 20,100

BOOKDB = "books.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #print("aaaaaaaaaaaaaaa")
        db = g._database = sqlite3.connect(BOOKDB)
    db.row_factory = sqlite3.Row
    return db


"""
INSERT INTO table1 (column1,column2 ,..)
VALUES 
   (value1,value2 ,...),
   (value1,value2 ,...),
    ...
   (value1,value2 ,...);
"""

@app.post("/books")
def create_books():
    
    if not request.is_json:
        return jsonify(error = "expected JSON"), 415
    
    p = request.get_json(silent=True) or {}
    t = (p.get("title") or "").strip()
    a = (p.get("author") or "").strip()
    if not t or not a:
        return jsonify(error = "title and author required"), 422
    
    # book = {"id" : _next_id, "title": t, "author":a}
    #BOOKS.append(book); _next_id+=1

    insert_statement = '''INSERT INTO books (title, author) VALUES (?, ?)'''
    new_book = (t,a)
    cur = get_db().cursor()
    cur.execute(insert_statement, new_book)
    get_db().commit()

    resp = make_response(jsonify({"id" : cur.lastrowid, "title": t, "author":a}),201)
    resp.headers["Locations"] = f"/books/{cur.lastrowid}"
    return resp

@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))

    except ValueError:
        return jsonify(error = "page and size must be int"), 400
    
    page = max(page, 1); size = max(min(size ,MAX_SIZE), 1)

    #flt = BOOKS
    arg = []
    cond = []

    a = request.args.get("author")
    if a:
        arg.appned(a)
        cond.append("LOWER(author) = LOWER(?)")

    #if a: flt = [b for b in flt if b["author"].lower() == a.lower()]

    q = (request.args.get("q") or "").lower()
    if q:
        arg.append(q)
        cond.append("LOWER(title) LIKE LOWER(?)" )
    #if q: flt = [b for b in flt if q in b["title"].lower()]
    conditions = ""
    if cond:
        conditions += " AND ".join(cond)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM books WHERE{conditions}", arg)
    total = cur.fetchone()[0]

    start = (page-1)*size
    cur.execute(f"SELECT * FROM books WHERE{conditions} LIMIT ? OFFSET ?", arg + [size, start])
    rows = cur.fetchall()

    items = [dict(r) for r in rows]
    #paginate
    last = (total+size-1)//size
    end = start + len(items)
    #HATEOAS links
    def u(p): return f"/books?page={p}&size={size}"
    links = {"self": {"href":u(page)},
             "first":{"href":u(1)},
             "last": {"href":u(max(last,1))}
             }
    if page > 1: links["prev"] = {"href":u(page-1)}
    if end < total: links["next"] = {"href" : u(page+1)}
    body = {"data" : items, 
            "pagination":  {"page":page, "size":size, "total":total, "total_pages":last},
            "_links":links
            }
    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp


if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000, debug = True)