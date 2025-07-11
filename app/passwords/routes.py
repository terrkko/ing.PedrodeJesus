from passlib.hash import scrypt
from flask import render_template, request, redirect, url_for, session, flash
#from werkzeug.security import generate_password_hash, check_password_hash
#from app import app
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
        #if user_info and check_password_hash(user_info['password_hash'], password):
            session['logged_in'] = True
            session['username'] = username
            flash('Bienvenido!')
            return redirect(url_for('index'))
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
    return redirect(url_for('login'))

# =====================
# HOME (AGREGAR NUEVO)
# =====================
@passwords_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@passwords_bp.route('/add', methods=['POST'])
@login_required
def add():
    service = request.form['service'].strip()
    user = request.form['user'].strip()
    password = request.form['password'].strip()

    if not service or not user or not password:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index'))

    username = session['username']
    users = load_users()
    user_data = decrypt_data(users[username]['data'])

    if service in user_data:
        flash('El servicio ya existe.')
        return redirect(url_for('index'))

    user_data[service] = {
        "usuario": user,
        "password": password
    }

    users[username]['data'] = encrypt_data(user_data)
    save_users(users)
    log_action(username, 'ADD', service)
    flash(f'Servicio "{service}" agregado.')
    return redirect(url_for('passwords'))

# =====================
# VER CONTRASEÑAS (CON BUSCADOR)
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
# ELIMINAR
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
    return redirect(url_for('passwords'))

# =====================
# EDITAR
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
        return redirect(url_for('passwords'))

@passwords_bp.route('/update/<service>', methods=['POST'])
@login_required
def update(service):
    new_user = request.form['user'].strip()
    new_password = request.form['password'].strip()

    if not new_user or not new_password:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('edit', service=service))

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
    return redirect(url_for('passwords'))
