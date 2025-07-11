from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importar y registrar blueprints
    from app.main import main_bp
    from app.passwords import passwords_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(passwords_bp, url_prefix='/passwords')

    return app



