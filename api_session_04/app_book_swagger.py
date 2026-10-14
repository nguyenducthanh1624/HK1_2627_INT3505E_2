from flask import Flask, jsonify, request, make_response, render_template_string


app = Flask(__name__)
BOOKS = []
_next_id = 1

# OpenAPI description for the existing Books API.
OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Books API",
        "version": "1.0.0",
        "description": "API for listing, creating, retrieving, updating, and deleting books."
    },
    "servers": [{"url": "http://127.0.0.1:5000", "description": "Local development server"}],
    "tags": [{"name": "Books", "description": "Manage books"}],
    "paths": {
        "/books": {
            "get": {
                "tags": ["Books"],
                "summary": "List all books",
                "responses": {
                    "200": {
                        "description": "Books returned successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["data", "total"],
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Book"}
                                        },
                                        "total": {"type": "integer", "example": 2}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Books"],
                "summary": "Create a book",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/CreateBook"},
                            "example": {"title": "Dune", "author": "Frank Herbert"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Book created",
                        "headers": {
                            "Locations": {
                                "description": "Path to the created book (as returned by the current app)",
                                "schema": {"type": "string", "example": "/books/1"}
                            }
                        },
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Book"}}}
                    },
                    "415": {"$ref": "#/components/responses/UnsupportedMediaType"},
                    "422": {"$ref": "#/components/responses/ValidationError"}
                }
            }
        },
        "/books/{bid}": {
            "parameters": [{
                "name": "bid",
                "in": "path",
                "required": True,
                "description": "ID of the book",
                "schema": {"type": "integer", "minimum": 1}
            }],
            "get": {
                "tags": ["Books"],
                "summary": "Get a book by ID",
                "responses": {
                    "200": {
                        "description": "Book found",
                        "headers": {
                            "Cache-Control": {
                                "description": "Caching directive",
                                "schema": {"type": "string", "example": "max-age=60"}
                            }
                        },
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Book"}}}
                    },
                    "404": {"$ref": "#/components/responses/NotFound"}
                }
            },
            "put": {
                "tags": ["Books"],
                "summary": "Replace a book",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ReplaceBook"},
                            "example": {"title": "Dune", "author": "Frank Herbert", "isbn": "9780441013593", "price": 12.5}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Book replaced", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Book"}}}},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    "422": {"$ref": "#/components/responses/ValidationError"}
                }
            },
            "patch": {
                "tags": ["Books"],
                "summary": "Update selected fields of a book",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PatchBook"},
                            "example": {"price": 9.99}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Book updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Book"}}}},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    "422": {"$ref": "#/components/responses/ValidationError"}
                }
            },
            "delete": {
                "tags": ["Books"],
                "summary": "Delete a book",
                "responses": {
                    "204": {"description": "Book deleted successfully; no response body"},
                    "404": {"$ref": "#/components/responses/NotFound"}
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Book": {
                "type": "object",
                "required": ["id", "title", "author"],
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "title": {"type": "string", "example": "Dune"},
                    "author": {"type": "string", "example": "Frank Herbert"},
                    "isbn": {"type": "string", "nullable": True, "example": "9780441013593"},
                    "price": {"type": "number", "format": "float", "nullable": True, "example": 12.5}
                }
            },
            "CreateBook": {
                "type": "object",
                "required": ["title", "author"],
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "author": {"type": "string", "minLength": 1}
                }
            },
            "ReplaceBook": {
                "type": "object",
                "required": ["title", "author"],
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "author": {"type": "string", "minLength": 1},
                    "isbn": {"type": "string", "nullable": True},
                    "price": {"type": "number", "format": "float", "nullable": True}
                }
            },
            "PatchBook": {
                "type": "object",
                "description": "Send one or more fields to update.",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "isbn": {"type": "string", "nullable": True},
                    "price": {"type": "number", "format": "float", "minimum": 0}
                }
            },
            "Error": {
                "type": "object",
                "properties": {"error": {"type": "string"}}
            }
        },
        "responses": {
            "NotFound": {
                "description": "No book exists with the given ID",
                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}, "example": {"error": "not found"}}}
            },
            "ValidationError": {
                "description": "Request validation failed",
                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}
            },
            "UnsupportedMediaType": {
                "description": "Request must use JSON",
                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}, "example": {"error": "expected JSON"}}}
            }
        }
    }
}


@app.get("/openapi.json")
def openapi_json():
    """Return the OpenAPI specification as JSON."""
    return jsonify(OPENAPI_SPEC)


@app.get("/docs")
def swagger_docs():
    """Render Swagger UI and load this app's OpenAPI document."""
    return render_template_string("""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Books API - Swagger UI</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.33.0/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.33.0/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => {
      window.ui = SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: "#swagger-ui",
        deepLinking: true
      });
    };
  </script>
</body>
</html>""")


@app.get("/books")
def list_books():
    return jsonify({
        "data": BOOKS,
        "total": len(BOOKS)
    }), 200


@app.post("/books")
def create_books():
    global _next_id
    if not request.is_json:
        return jsonify(error="expected JSON"), 415
    p = request.get_json(silent=True) or {}
    t = (p.get("title") or "").strip()
    a = (p.get("author") or "").strip()
    if not t or not a:
        return jsonify(error="title and author required"), 422

    book = {"id": _next_id, "title": t, "author": a}
    BOOKS.append(book)
    _next_id += 1

    resp = make_response(jsonify(book), 201)
    resp.headers["Locations"] = f"/books/{book['id']}"
    return resp


@app.get("/books/<int:bid>")
def fetch(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None:
        return jsonify(error="not found"), 404
    resp = make_response(jsonify(BOOKS[i]), 200)
    resp.headers["Cache-Control"] = "max-age=60"
    return resp


@app.put("/books/<int:bid>")
def put(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None:
        return jsonify(error="not found"), 404
    p = request.get_json(silent=True) or {}
    t = p.get("title")
    a = p.get("author")
    if not t or not a:
        return jsonify(error="need title+author"), 422

    BOOKS[i] = {
        "id": bid,
        "title": t.strip(),
        "author": a.strip(),
        "isbn": p.get("isbn"),
        "price": p.get("price")
    }
    return jsonify(BOOKS[i]), 200


@app.patch("/books/<int:bid>")
def patch(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None:
        return jsonify(error="not found"), 404
    p = request.get_json(silent=True) or {}
    if p.get("price", 0) < 0:
        return jsonify(error="price must be positive"), 422
    for k in "title author isbn price".split():
        if k in p:
            BOOKS[i][k] = p[k]

    return jsonify(BOOKS[i]), 200


@app.delete("/books/<int:bid>")
def delete(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None:
        return jsonify(error="not found"), 404

    BOOKS.pop(i)
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
