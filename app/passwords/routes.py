from passlib.hash import scrypt
import os, json
from flask import render_template, request, redirect, url_for, session, flash
from .crypto_utils import load_users, save_users, encrypt_data, decrypt_data
from .logger_utils import log_action
from . import passwords_bp

# =====================
# DECORADOR LOGIN
# =====================
def login_required(f):
    def wrapped(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Debes iniciar sesión.')
            return redirect(url_for('passwords.login'))
        return f(*args, **kwargs)
    wrapped.__name__ = f.__name__
    return wrapped

# =====================
# LOGIN
# =====================
@passwords_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        users = load_users()
        user_info = users.get(username)
        
        if user_info and scrypt.verify(password, user_info['password_hash']):
            session['logged_in'] = True
            session['username'] = username
            flash('Bienvenido!')
            return redirect(url_for('passwords.index'))
        else:
            flash('Credenciales incorrectas.')
    return render_template('login.html')

# =====================
# LOGOUT
# =====================
@passwords_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.')
    return redirect(url_for('passwords.login'))

# =====================
# HOME (INDEX)
# =====================
@passwords_bp.route('/')
@login_required
def index():
   return redirect(url_for('passwords.passwords'))

# =====================
# AGREGAR NUEVO SERVICIO
# =====================
@passwords_bp.route('/add', methods=['POST'])
@login_required
def add():
    service = request.form['service'].strip()
    user = request.form['user'].strip()
    password = request.form['password'].strip()

    if not service or not user or not password:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('passwords.index'))

    username = session['username']
    users = load_users()
    user_data = decrypt_data(users[username]['data'])

    if service in user_data:
        flash('El servicio ya existe.')
        return redirect(url_for('passwords.index'))

    user_data[service] = {
        "usuario": user,
        "password": password
    }

    users[username]['data'] = encrypt_data(user_data)
    save_users(users)
    log_action(username, 'ADD', service)
    flash(f'Servicio "{service}" agregado.')
    return redirect(url_for('passwords.passwords'))

@passwords_bp.route('/add', methods=['GET'])
@login_required
def add_form():
    return render_template('new.html')  # plantilla con formulario
# =====================
# VER CONTRASEÑAS
# =====================
@passwords_bp.route('/passwords', methods=['GET', 'POST'])
@login_required
def passwords():
    username = session['username']
    users = load_users()
    user_data = decrypt_data(users[username]['data'])

    filtered = user_data
    if request.method == 'POST':
        query = request.form.get('query', '').lower().strip()
        filtered = {k: v for k, v in user_data.items() if query in k.lower()}

    return render_template('passwords.html', data=filtered)

# =====================
# ELIMINAR SERVICIO
# =====================
@passwords_bp.route('/delete/<service>', methods=['POST'])
@login_required
def delete(service):
    username = session['username']
    users = load_users()
    user_data = decrypt_data(users[username]['data'])

    if service in user_data:
        del user_data[service]
        users[username]['data'] = encrypt_data(user_data)
        save_users(users)
        log_action(username, 'DELETE', service)
        flash(f'Servicio "{service}" eliminado.')
    else:
        flash('Servicio no encontrado.')
    return redirect(url_for('passwords.passwords'))

# =====================
# EDITAR SERVICIO
# =====================
@passwords_bp.route('/edit/<service>')
@login_required
def edit(service):
    username = session['username']
    users = load_users()
    user_data = decrypt_data(users[username]['data'])

    if service in user_data:
        return render_template('edit.html',
                               service=service,
                               user=user_data[service]['usuario'],
                               password=user_data[service]['password'])
    else:
        flash('Servicio no encontrado.')
        return redirect(url_for('passwords.passwords'))

# =====================
# ACTUALIZAR SERVICIO
# =====================
@passwords_bp.route('/update/<service>', methods=['POST'])
@login_required
def update(service):
    new_user = request.form['user'].strip()
    new_password = request.form['password'].strip()

    if not new_user or not new_password:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('passwords.edit', service=service))

    username = session['username']
    users = load_users()
    user_data = decrypt_data(users[username]['data'])

    if service in user_data:
        user_data[service]['usuario'] = new_user
        user_data[service]['password'] = new_password
        users[username]['data'] = encrypt_data(user_data)
        save_users(users)
        log_action(username, 'UPDATE', service)
        flash(f'Servicio "{service}" actualizado.')
    else:
        flash('Servicio no encontrado.')
    return redirect(url_for('passwords.passwords'))

# =====================
# CARGAR USUARIOS (por si no lo importaste)
# =====================
def load_users():
    ruta = os.path.join(os.path.dirname(__file__), 'users.json')
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"No se encontró el archivo: {ruta}")
        return {}
