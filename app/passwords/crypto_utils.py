import json
import os
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(__file__)

USERS_FILE = os.path.join(BASE_DIR, 'users.json')  # ruta absoluta correcta
KEY_FILE = os.path.join(BASE_DIR, 'fernet.key')   # ruta absoluta correcta

def get_fernet():
    if not os.path.exists(KEY_FILE):
        # Si no existe la llave, la creamos
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return Fernet(key)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def encrypt_data(data):
    fernet = get_fernet()
    result = {}
    for service, creds in data.items():
        result[service] = {
            'usuario': fernet.encrypt(creds['usuario'].encode()).decode(),
            'password': fernet.encrypt(creds['password'].encode()).decode()
        }
    return result

def decrypt_data(data):
    if not data:
        return {}
    fernet = get_fernet()
    result = {}
    for service, creds in data.items():
        result[service] = {
            'usuario': fernet.decrypt(creds['usuario'].encode()).decode(),
            'password': fernet.decrypt(creds['password'].encode()).decode()
        }
    return result
