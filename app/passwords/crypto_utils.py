import json
import os
from cryptography.fernet import Fernet

USERS_FILE = '.users.json'
KEY_FILE = '.fernet.key'

def get_fernet():
    with open(KEY_FILE, 'r') as f:
        key = f.read().strip().encode()
    return Fernet(key)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

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
