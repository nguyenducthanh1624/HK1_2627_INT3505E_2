from flask import Flask
from .extensions import db, migrate
from .api.products import (products_bp)
from .api.orders import (orders_bp)
from .api.health import health_bp
from .config import (DefaultConfig)
from .models import *

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(
        config or DefaultConfig)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(
        products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(health_bp)
    return app