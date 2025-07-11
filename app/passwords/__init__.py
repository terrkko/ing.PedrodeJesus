from flask import Blueprint

passwords_bp = Blueprint('passwords', __name__, template_folder='templates')

from . import routes
