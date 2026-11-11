"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""

from jsonschema import validate, ValidationError
import pytest
from tools import get_book_schema

def test_list_books_empty(client): 
    r = client.get("/books")
    assert r.status_code == 200
    assert r.content_type == "application/json"
    assert r.get_json() == []

"""def test_list_shape(client, sample_book): 
    data = client.get("/books").get_json()
    assert len(data) == 1 
    keys = {"id","title","author", "year","isbn"}
    assert set(data[0].keys()) == keys
    assert isinstance(data[0]["id"], int)"""


"""def test_post_persists(client, app): 
    payload = {"title":"DDIA","author":"Kleppmann", "year":2017}
    r = client.post("/books", json=payload)
    assert r.status_code == 201 
    bid = r.get_json()["id"]
    from models import Book
    with app.app_context():
        assert Book.query.get(bid).title == "DDIA"
        assert client.post("/books", json=payload).status_code == 409"""

def test_post_no_title(client, app): 
    payload = {"author":"Kleppmann", "year":2017}
    r = client.post("/books", json=payload)
    assert r.status_code == 400

def get_id_not_found(client, sample_book):
    r = client.get("/books/9900").get_json()
    assert r.status_code == 404
    assert r.get_json()["code"] == "NOT_FOUND"

def test_put_replaces(client, sample_book): 
    r = client.put(f"/books/{sample_book}", json={"title":"Renamed",
"author":"new",
"year":2025})
    assert r.get_json()["title"] == "Renamed"

def test_delete_404_after(client, sample_book):
    assert client.delete( f"/books/{sample_book}").status_code == 204
    assert client.get( f"/books/{sample_book}").status_code == 404

"""def test_delete_unknown_404(client):
    assert client.delete( "/books/9999").status_code == 404"""



