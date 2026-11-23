from flask import Blueprint, request
from .users_data import get_user, USERS
bp = Blueprint("v2", __name__)
@bp.route("/<int:uid>")
def get(uid):
    u = get_user(uid)
    if not u: return {"error": "nf"}, 404
    return {"id": uid,
    "first_name": u["first_name"],
    "last_name": u["last_name"],
    "email": u["email"]}

@bp.post("")
def post():
    data = request.get_json(silent = True)
    uid = max(USERS.keys(), default=0) + 1

    required = ["first_name", "last_name", "email"]
    
    user = {field: data[field] for field in required}
    USERS[uid] = user