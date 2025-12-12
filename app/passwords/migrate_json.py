import json
from .models import User, PasswordEntry, encrypt
from .utils import make_hash
from . import db

def migrate_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for username, user_data in data.items():
        u = User(
            username=username,
            password_hash=make_hash("1234")   # puedes pedir nueva contraseña
        )
        db.session.add(u)
        db.session.commit()

        decrypted = user_data.get("data", {})

        for service, info in decrypted.items():
            entry = PasswordEntry(
                service=service,
                user_encrypted=encrypt(info["usuario"]),
                password_encrypted=encrypt(info["password"]),
                user_id=u.id
            )
            db.session.add(entry)

    db.session.commit()
