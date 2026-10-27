from functools import wraps
from flask import request, jsonify, g
import secrets, hashlib

def mint_key(prefix):
    raw = secrets.token_urlsafe(32) 
    body = raw
    digest = hashlib.sha256(raw.encode()).hexdigest()[:8]
    plain = f"{prefix}_{body}_{digest}" 
    store = hashlib.sha256(plain.encode()).hexdigest()
    return plain, store

def require_api_key(scopes=None):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            key = request.headers.get("X-Api-Key", "")
            if not key:
                return jsonify({"e": "missing"}), 401
            hashed = hashlib.sha256(key.encode()).hexdigest()
            row = db.fetchone(
                "SELECT id, owner_id, scopes, revoked_at, expires_at "
                "FROM api_keys WHERE hash=?", (hashed,))
            if (not row or row["revoked_at"] or
                (row["expires_at"] is not None and
                row["expires_at"] <= now_utc())):
                return jsonify({"e": "invalid"}), 401
            granted = set(row["scopes"].split(","))
            if scopes and not set(scopes).issubset(granted):
                return jsonify({"e": "scope"}), 403
            g.api_key_id = row["id"]
            g.owner_id = row["owner_id"]
            g.api_scopes = granted
            return fn(*a, **kw)
        return w
    return d


