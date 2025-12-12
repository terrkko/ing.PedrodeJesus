from flask import Blueprint
from app.extensions import db  # Usar SOLO la instancia global correcta

# Importar blueprint después de db para evitar circular imports
from .routes import passwords_bp
from .models import create_default_admin


def init_app(app):
    """Inicializa SQLAlchemy y registra el blueprint."""
    db.init_app(app)
    app.register_blueprint(passwords_bp, url_prefix="/passwords")


def create_tables(app):
    """Crea las tablas de SQLAlchemy dentro del contexto."""
    with app.app_context():
        db.create_all()
        create_default_admin()
