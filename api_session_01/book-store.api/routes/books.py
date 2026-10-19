from flask import Blueprint, request, jsonify
from sqlalchemy import select, func, tuple_
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

def _enc(s):
    return base64.urlsafe_b64encode(
        json.dumps(s).encode()
    ).decode().rstrip("=")
def apply_cursor(q, raw, sort, p, desc):
    if not raw:
        return q, None, 200
    pad = "=" * (-len(raw) % 4)
    c = json.loads(base64.urlsafe_b64decode(raw + pad))
    if c.get("s") != sort:
        return None, "sort_chg", 400
    v, i = c["v"], c["i"]
    op = "<" if desc else ">"
    condition = tuple_(p, Book.id).op(op)((v, i))
    return q.filter(condition), None, 200


def build_response(items, lim, sort, p, more):
    nxt = None
    if items and more:
        last = items[-1]
        nxt = _enc({
            "s": sort,
            "v": getattr(last, p.key),
            "i": last.id
        })

    return jsonify({
        "data": [b.to_dict() for b in items],
        "page": {"next": nxt, "more": more}
    })


@bp.get("/books")
def list_books():

    strategy = request.args.get("strategy", "offset").lower()

    if strategy not in ("offset", "cursor"):
        return jsonify({
            "error": "bad_strategy",
            "allowed": ["offset", "cursor"]
        }), 400
    
    if strategy == "offset":
        o = request.args.get("offset", 0, type=int)

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
        })

    
    """limit = min(request.args.get(
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
    })"""

    raw = request.args.get("cursor")
    lim = min(request.args.get("limit", 20, type=int), 100)
    sort = request.args.get("sort", "-id")
    cat = request.args.get("category", type=int)
    p, cols, desc = parse_sort(sort)
    if p is None:
        return cols, 400
    q = select(Book).order_by(*cols)

    if cat:
        q = q.filter(Book.category_id == cat)

    q, err, code = apply_cursor(q, raw, sort, p, desc)

    if err:
        return {"e": err}, code
    rows = db.session.scalars(q.limit(lim + 1)).all()

    return build_response(rows[:lim], lim, sort, p, len(rows) > lim)

 
