from app.extensions import db  # evitar circular import
from werkzeug.security import generate_password_hash
from cryptography.fernet import Fernet
from flask import current_app
from datetime import datetime


# ----------------------------
# FUNCIONES DE CIFRADO FERNET
# ----------------------------

def encrypt(text: str):
    key = current_app.config['FERNET_KEY']
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()


def decrypt(text: str):
    key = current_app.config['FERNET_KEY']
    f = Fernet(key)
    return f.decrypt(text.encode()).decode()


# ----------------------------
# MODELO DE USUARIO
# ----------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    entries = db.relationship("PasswordEntry", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

# ----------------------------
# CREAR ADMIN POR DEFECTO
# ----------------------------

def create_default_admin():
    admin_username = "admin"
    admin_password = "admin123"

    if not User.query.filter_by(username=admin_username).first():
        admin = User(username=admin_username)
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print("✔ Usuario admin creado: admin / admin123")
    else:
        print("✔ Usuario admin ya existe")



# ----------------------------
# MODELO DE ENTRADAS (CONTRASEÑAS)
# ----------------------------

class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(150), nullable=False)
    user_encrypted = db.Column(db.Text, nullable=False)
    password_encrypted = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# ----------------------------
# LOG DE ACCIONES
# ----------------------------

class ActionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    action = db.Column(db.String(20))
    service = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
