from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
import bcrypt, os
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ["FLASK_SECRET_KEY"],
    JWT_SECRET_KEY=os.environ["JWT_SECRET_KEY"],
    JWT_ACCESS_TOKEN_EXPIRES=900,
    JWT_REFRESH_TOKEN_EXPIRES=2592000,
    JWT_ALGORITHM="HS256"
)
jwt = JWTManager(app)

@app.post("/api/auth/login")
def login():
    user = db.fetchone(
        "SELECT id, pwd_hash FROM users WHERE email=?",
        (request.json.get("email"),))
    pwd = request.json.get("password", "").encode()
    if not user or not bcrypt.checkpw(pwd, user["pwd_hash"]):
        return jsonify(error="invalid_credentials"), 401
 # Helper trả {"roles": [...], "scopes": [...]}.
    claims = load_permissions(user["id"])
    uid = str(user["id"])
    return jsonify(
        access=create_access_token(
        identity=uid, additional_claims=claims),
        refresh=create_refresh_token(
        identity=uid, additional_claims=claims)
    )

@app.get("/api/orders")
@jwt_required()
def list_orders():
    uid = get_jwt_identity()
    claims = get_jwt()
    if "orders:read" not in claims.get("scopes", []):
        return jsonify(error="insufficient_scope"), 403
    return jsonify(orders_by_owner(uid))

@app.post("/api/auth/refresh")
@jwt_required(refresh=True)
def refresh():
    
    claims = load_permissions(get_jwt_identity())
    return jsonify(access=create_access_token(
        identity=get_jwt_identity(), additional_claims=claims))