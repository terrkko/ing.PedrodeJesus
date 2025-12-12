from flask import Flask
from config import Config
from app.passwords import init_app, create_tables

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa passwords (DB + blueprint)
    init_app(app)
     
    # Registrar otros blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)

    # Crear tablas y admin
    with app.app_context():
        create_tables(app)

    return app



