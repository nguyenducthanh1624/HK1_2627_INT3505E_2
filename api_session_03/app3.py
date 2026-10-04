from flask import Flask, jsonify, request, make_response
app = Flask(__name__)
_next = 2
POSTS = [{"id": 1}]

def find(id):
    return next((p for p in POSTS if p["id"] == id), None)

@app.get("/posts")
def list_posts():
    n = int(request.args.get("limit", 100))
    return jsonify(POSTS[:n]), 200

@app.route("/posts/<int:pid>", methods=["GET"])
def get_post(pid):
    post = find(pid)
    if not post: return {"error":"not found"}, 404
    return jsonify(post), 200

@app.post("/posts")
def create_posts():
    global _next_id
    if not request.is_json:
        return jsonify(error = "expected JSON"), 415
    
    post = {"id" : _next_id}
    POSTS.append(post); _next_id+=1
    resp = make_response(jsonify(post),201)
    resp.headers["Locations"] = f"/posts/{post['id']}"
    return resp

@app.route("/posts/<int:pid>", methods=["PUT","DELETE"])
def modify_post(pid):
    post = find(pid)
    if not post : return {"error":"not found"}, 404
    if request.method == "PUT":
        post.update(request.get_json(silent=True) or {})
        return jsonify(post), 200
    POSTS.remove(post)
    return "", 204

