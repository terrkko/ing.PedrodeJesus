from flask import Blueprint, request, session, redirect, render_template, flash, url_for
from . import db
from .models import User, PasswordEntry, encrypt, decrypt
from .utils import verify_password, make_hash, log_action



passwords_bp = Blueprint("passwords",__name__,  template_folder="templates",  static_folder="static" )

def login_required(func):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("passwords.login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# LOGIN
@passwords_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = User.query.filter_by(username=username).first()

        if not user or not verify_password(password, user.password_hash):
            flash("Credenciales incorrectas")
            return redirect(url_for("passwords.login"))

        session["user_id"] = user.id
        session["username"] = user.username
        return redirect(url_for("passwords.passwords"))

    return render_template("login.html")

# LOGOUT
@passwords_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("routes.login"))

# LISTADO
@passwords_bp.route("/")
@login_required
def passwords():
    user_id = session["user_id"]
    entries = PasswordEntry.query.filter_by(user_id=user_id).all()

    data = [{
        "id": e.id,
        "service": e.service,
        "user": decrypt(e.user_encrypted),
        "password": decrypt(e.password_encrypted)
    } for e in entries]

    return render_template("passwords.html", data=data)

# AGREGAR

@passwords_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        service = request.form["service"].strip()
        user = request.form["user"].strip()
        password = request.form["password"].strip()

        # Evitar duplicados
        if PasswordEntry.query.filter_by(service=service, user_id=session["user_id"]).first():
            flash("Servicio ya existe")
            return redirect(url_for("passwords.passwords"))

        entry = PasswordEntry(
            service=service,
            user_encrypted=encrypt(user),
            password_encrypted=encrypt(password),
            user_id=session["user_id"]
        )
        db.session.add(entry)
        db.session.commit()

        log_action(session["username"], "ADD", service)

        flash(f"Servicio {service} agregado.")
        return redirect(url_for("passwords.passwords"))

    # 👉 SI ES GET, simplemente muestra el formulario
    return render_template("new.html")

@passwords_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    entry = PasswordEntry.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if not entry:
        flash("Servicio no encontrado.")
        return redirect(url_for("passwords.passwords"))

    service_name = entry.service

    db.session.delete(entry)
    db.session.commit()

    log_action(session["username"], "DELETE", service_name)

    flash(f'Servicio "{service_name}" eliminado.')
    return redirect(url_for("passwords.passwords"))

@passwords_bp.route('/edit/<int:id>')
@login_required
def edit(id):
    entry = PasswordEntry.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if not entry:
        flash("Servicio no encontrado.")
        return redirect(url_for("passwords.passwords"))

    return render_template(
        "edit.html",
        id=entry.id,
        service=entry.service,
        user=decrypt(entry.user_encrypted),
        password=decrypt(entry.password_encrypted)
    )
    
@passwords_bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    entry = PasswordEntry.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if not entry:
        flash("Servicio no encontrado.")
        return redirect(url_for("passwords.passwords"))

    user = request.form["user"].strip()
    password = request.form["password"].strip()

    if not user or not password:
        flash("Todos los campos son obligatorios.")
        return redirect(url_for("passwords.edit", id=id))

    entry.user_encrypted = encrypt(user)
    entry.password_encrypted = encrypt(password)
    db.session.commit()

    log_action(session["username"], "UPDATE", entry.service)

    flash("Servicio actualizado correctamente.")
    return redirect(url_for("passwords.passwords"))
