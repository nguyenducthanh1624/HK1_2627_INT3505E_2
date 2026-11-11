from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

@app.get("/books")
def list_books(): 
    q = Book.query
    if a := request.args.get("author"): q = q.filter_by(author=a)
    items = q.limit(20).all()
    return jsonify([b.to_dict() for b in items])