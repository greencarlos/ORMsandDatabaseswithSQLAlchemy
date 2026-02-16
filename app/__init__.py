from flask import Flask
from .extensions import ma
from .models import db
from .blueprints.members import members_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp 

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    ma.init_app(app)
    db.init_app(app)

    app.register_blueprint(members_bp, url_prefix="/members")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")

    return app
