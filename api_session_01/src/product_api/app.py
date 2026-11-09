from flask import Flask
from flask_smorest import Api
from api.products import blp

app = Flask(__name__)

app.config["API_TITLE"] = "Product API"
app.config["API_VERSION"] = "1.0.0"
app.config["OPENAPI_VERSION"] = "3.0.3"

# 3. Configure Swagger UI
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
)

api = Api(app)
api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True)