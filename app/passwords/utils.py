from passlib.hash import scrypt
from datetime import datetime
from . import db
from .models import ActionLog
from werkzeug.security import check_password_hash

def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)

def make_hash(password):
    return scrypt.hash(password)

def log_action(user, action, service):
    entry = ActionLog(
        user=user,
        action=action,
        service=service,
        timestamp=datetime.now()
    )
    db.session.add(entry)
    db.session.commit()
