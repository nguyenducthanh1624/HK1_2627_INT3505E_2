from flask import Flask, jsonify, request, make_response
from werkzeug.exceptions import HTTPException 
app = Flask(__name__)

class ProblemError(Exception):
    def __init__(self, status, title, detail, type, instance):
        self.status = status
        self.title = title
        self.detail = detail
        self.type = type
        self.instance = instance

@app.errorhandler(ProblemError)
def handle_error(error):
    response_data = {"type":error.type, "title":error.title, "detail":error.detail, "status":error.status, "instance":error.instance}
    #return jsonify(response_data), error.status
    resp = make_response(jsonify(response_data), error.status)
    resp.headers["Content-Type"] = "application/problem+json"
    return resp

@app.errorhandler(HTTPException)
def handle_HTTP_exception(error):
    resp_data = {"type":"about:blank", "title":error.name, "detail":error.description, 
                 "status":error.code, "instance":request.path}
    resp = make_response(jsonify(resp_data), error.status)
    resp.headers["Content-Type"] = "application/problem+json"
    return resp

@app.errorhandler(Exception)
def handle_exception(e):
    resp_data = {"type":"about:blank", "title":"Internal Server Error", "detail":"Hệ thống gặp sự cố",
                 "status":500, "instance":request.path}
    app.logger.exception(e)
    resp = make_response(jsonify(resp_data), 500)
    resp.headers["Content-Type"] = "application/problem+json"
    return resp