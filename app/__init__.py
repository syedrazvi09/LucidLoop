from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from app.models import db
from app.config import Config
from app.views.auth import auth_bp
from app.views.dashboard import dashboard_bp
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def root_redirect():
        return redirect(url_for('auth.login_page'))



    return app