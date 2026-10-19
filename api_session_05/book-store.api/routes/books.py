from flask import Blueprint, request, jsonify
from sqlalchemy import select, func
from models import db, Book
import base64, json
DEFAULT, MAX_ = 20, 100

bp = Blueprint("books", __name__)

SORT = {"id": Book.id, "price": Book.price_vnd}
def parse_sort(raw):
    desc = raw.startswith("-")
    key = raw.lstrip("-")
    if key not in SORT:
        return None, "bad_sort", 400
    p = SORT[key]
    cols = [
    p.desc() if desc else p.asc(),
    Book.id.desc() if desc else Book.id.asc()
    ]
    return p, cols, desc

@bp.get("/books")
def list_books():
    """o = request.args.get("offset", 0, type=int)

    lim = min(request.args.get(
        "limit", DEFAULT, type=int), MAX_)

    total = db.session.scalar(
        select(func.count(Book.id)))
    
    rows = db.session.scalars(
        select(Book).order_by(Book.id)
        .offset(o).limit(lim)
    ).all()

    return jsonify({
        "data": [b.to_dict() for b in rows],
        "pagination": {
        "offset": o, "limit": lim,
        "total": total,
        "has_next": o + lim < total
        }
    })"""

    limit = min(request.args.get(
        "limit", 20, type=int), 100)
    after_id = request.args.get(
        "after_id", type=int)
    q = db.session.query(Book)

    if after_id is not None:
        q = q.filter(Book.id > after_id)

    q = q.order_by(Book.id.asc()).limit(limit + 1)
    rows = q.all() # +1 trick
    has_more = len(rows) > limit
    rows = rows[:limit]
    next_c = rows[-1].id if rows and has_more else None
    return jsonify({
        "data": [b.to_dict() for b in rows],
        "page_info": {
        "next_cursor": next_c,
        "has_more": has_more
        }
    })
 
