

def create_app(cfg=None): 
    app = Flask(__name__)
    app.config.update( DB=cfg or"books.db")
    db.init_app(app); db.create_all()
    return app